# -*- coding: utf-8 -*-
"""
Created on Wed May  2 18:01:47 2018

@author: christoph
"""
import abce
import abcFinance
import random


class Household(abcFinance.Agent):
    def init(self, config):
        self.config = config
        self.accounts.make_asset_accounts(['money holdings'])
        self.accounts.make_liability_accounts(['loan liabilities'])
        self.accounts.make_flow_accounts(['income', 'expenses'])
        self.housebank = self.id % config.num_banks

    def return_housebank(self):
        return self.housebank

    def return_money_holdings(self):
        _, amount = self.accounts['money holdings'].get_balance()
        return amount

    def transfer_money(self):
        recipient = random.randrange(self.config.num_households)
        recipient_housebank = self.config.housebank_indices[recipient]
        _, amount = self.accounts['money holdings'].get_balance()
        amount = round(random.random() * amount)
        if amount > 0:
            self.send(('bank', self.housebank), 'Outtransfer',
                      {'amount': amount, 'recipient': recipient})
            self.send(('bank', recipient_housebank), 'Intransfer',
                      {'amount': amount, 'sender': self.id})

    def get_outside_money(self):
        self.send(('bank', self.housebank), '_autobook', dict(
            debit=[('reserves', self.config.loan_size)],
            credit=[('deposits', self.config.loan_size)],
            text='Outside money endowment'))
        self.accounts.book(debit=[('money holdings', self.config.loan_size)],
                           credit=([('equity', self.config.loan_size)]),
                           text='Outside money endowment')

    def request_loan(self):
        self.send(('bank', self.housebank), 'loan_request', {'amount': self.config.loan_size})


class Bank(abcFinance.Agent):
    def init(self, config):
        self.config = config
        self.accounts.make_asset_accounts(['reserves', 'claims'])
        self.accounts.make_liability_accounts(['deposits', 'refinancing'])
        self.accounts.make_flow_accounts(['interest income', 'interest expense'])

    def handle_transfers(self):
        num_banks = self.config.num_banks
        housebank_indices = self.config.housebank_indices
        intransfers = self.get_messages('Intransfer')
        outtransfers = self.get_messages('Outtransfer')

        # First, compute net transfers to each other bank
        amounts_transfers = [0] * num_banks
        sum_transfers = 0

        for intransfer in intransfers:
            sender = intransfer.content['sender']
            sender_housebank = housebank_indices[sender]
            if sender_housebank != self.id:
                amount = intransfer.content['amount']
                amounts_transfers[sender_housebank] += amount
                sum_transfers += amount

        for outtransfer in outtransfers:
            recipient = outtransfer.content['recipient']
            recipient_housebank = housebank_indices[recipient]
            amount = outtransfer.content['amount']
            # Directly book transfers between own clients
            if recipient_housebank == self.id:
                self.send(outtransfer.sender, '_autobook', dict(
                    debit=[('expenses', amount)],
                    credit=[('money holdings', amount)],
                    text='Transfer'))
                self.send(('household', recipient), '_autobook', dict(
                    debit=[('money holdings', amount)],
                    credit=[('income', amount)],
                    text='Transfer'))
            else:
                amounts_transfers[recipient_housebank] -= amount
                sum_transfers -= amount

        # Compute net funding needs
        _, reserves = self.accounts['reserves'].get_balance()
        funding_need = - min(0, sum(amounts_transfers) + reserves)

        # >> could be in separate function after checking if funding needs can be met
        # Book transfers on clients' accounts
        for outtransfer in outtransfers:
            recipient = outtransfer.content['recipient']
            sender = outtransfer.sender
            recipient_housebank = housebank_indices[recipient]
            amount = outtransfer.content['amount']
            if recipient_housebank != self.id:
                self.send(outtransfer.sender, '_autobook', dict(
                    debit=[('expenses', amount)],
                    credit=[('money holdings', amount)],
                    text='Transfer'))
                self.send(('household', recipient), '_autobook', dict(
                    debit=[('money holdings', amount)],
                    credit=[('income', amount)],
                    text='Transfer'))

        # Only book net transfers between banks (net settlement system)
        for i in range(num_banks):
            amount = -amounts_transfers[i]
            if amount > 0:
                self.accounts.book(debit=[('deposits', amount)],
                                   credit=[('reserves', amount)],
                                   text='Client transfer')
                self.send(('bank', recipient_housebank), '_autobook', dict(
                    debit=[('reserves', amount)],
                    credit=[('deposits', amount)],
                    text='Client transfer'))

        return funding_need

    def get_funding(self, funding_needs):
        self.accounts.book(debit=[('reserves', funding_needs[self.id])],
                           credit=[('refinancing', funding_needs[self.id])])

    def give_loan(self):
        for loan_request in self.get_messages('loan_request'):
            amount = loan_request.content['amount']
            self.accounts.book(debit=[('claims', amount)],
                               credit=[('deposits', amount)],
                               text='Loan')

            self.send(loan_request.sender, '_autobook', dict(
                debit=[('money holdings', amount)],
                credit=[('loan liabilities', amount)],
                text='Loan'))


class Config:
    num_banks = 2
    num_households = 3
    spending_probability = 0.3
    loan_size = 100


sim = abce.Simulation(check_unchecked_msgs=True)

banks = sim.build_agents(Bank, 'bank', Config.num_banks, config=Config)
households = sim.build_agents(Household, 'household', Config.num_households, config=Config)

Config.housebank_indices = list(households.return_housebank())
households.get_outside_money()

for r in range(4):
    sim.advance_round(r)
    households.transfer_money()
    funding_needs = list(banks.handle_transfers())
    banks.get_funding(funding_needs)
    households.request_loan()
    banks.give_loan()
    households.book_end_of_period()
    banks.book_end_of_period()
    print('Households')
    households.print_balance_sheet()
    print('Banks')
    banks.print_balance_sheet()

sim.finalize()

