# -*- coding: utf-8 -*-
"""
Created on Wed May  2 18:01:47 2018

@author: christoph
"""
import abce
from accounting import AccountingSystem,Account,s
import random

class SimpleHousehold(abce.Agent):
    def init(self,num_banks):
        self.accounts = AccountingSystem(residual_account_name='equity')
        self.accounts.make_stock_account(['money holdings','loan liabilities'])
        self.accounts.make_flow_account(['income','expenses'])
        self.housebank = self.id % num_banks
    
    def return_housebank(self):
        return self.housebank
    
    def return_money_holdings(self):
        _,amount =  self.accounts['money holdings'].get_balance()
        return amount
    
    def _autobook(self):
        for booking in self.get_messages('_autobook'):
            self.accounts.book(**booking.content)
        print(self.name)
        self.accounts.print_profit_and_loss()
        self.accounts.make_end_of_period()
        self.accounts.print_balance_sheet()
        self.log('total_assets_household',self.accounts.get_total_assets())
        
#    def transfer_money(self,amounts,recipients,housebank_indices):
#        amount = amounts[self.id]
#        if amount > 0:
#            recipient = recipients[self.id]
#            recipient_housebank = housebank_indices[recipient]
#            self.send(('bank',self.housebank),'Outtransfer',{'amount':amount,'recipient':recipient})
#            self.send(('bank',recipient_housebank),'Intransfer',{'amount':amount,'sender':self.id})
    
    def transfer_money(self,housebank_indices):
        recipient = random.randrange(len(housebank_indices))
        recipient_housebank = housebank_indices[recipient]
        _,amount = self.accounts['money holdings'].get_balance()
        amount = round(random.random() * amount)
        if amount > 0:
            self.send(('bank',self.housebank),'Outtransfer',{'amount':amount,'recipient':recipient})
            self.send(('bank',recipient_housebank),'Intransfer',{'amount':amount,'sender':self.id})
    
    def get_outside_money(self,amount):
        self.send(('bank',self.housebank),'_autobook',dict(debit=[('claims',amount)], credit=[('deposits',amount)],text='Outside money endowment'))
        self.accounts.book(debit=[('money holdings',amount)],credit=([('equity',amount)]),text='Outside money endowment')
        
    def take_loan(self,amount):
        self.send(('bank',self.housebank),'loan_request',{'amount': amount})
        
class SimpleBank(abce.Agent):
    def init(self):
        self.accounts = AccountingSystem(residual_account_name='equity')
        self.accounts.make_stock_account(['reserves','claims','deposits','wholesale refinancing'])
        self.accounts.make_flow_account(['interest income','interest expense'])
    
    def _autobook(self):
        for booking in self.get_messages('_autobook'):
            self.accounts.book(**booking.content)
        print(self.name)
        self.accounts.print_profit_and_loss()
        self.accounts.make_end_of_period()
        self.accounts.print_balance_sheet()
        self.log('total_assets_bank',self.accounts.get_total_assets())
        
    def handle_transfers(self,num_banks,housebank_indices):
        intransfers = self.get_messages('Intransfer')
        outtransfers = self.get_messages('Outtransfer')
        
        # First, compute net transfers to each other bank
        amounts_transfers = [0] * num_banks
        
        for intransfer in intransfers:
            sender = intransfer.content['sender']
            sender_housebank = housebank_indices[sender]
            if sender_housebank != self.id:
                amount = intransfer.content['amount']
                amounts_transfers[sender_housebank] += amount
        
        for outtransfer in outtransfers:
            recipient = outtransfer.content['recipient']
            recipient_housebank = housebank_indices[recipient]
            amount = outtransfer.content['amount']
            # Directly book transfers between own clients
            if recipient_housebank == self.id:
                self.send(outtransfer.sender,'_autobook',dict(debit=[('expenses',amount)],credit=[('money holdings',amount)],text='Transfer'))
                self.send(('household',recipient),'_autobook',dict(debit=[('money holdings',amount)],credit=[('income',amount)],text='Transfer'))
            else:
                amounts_transfers[recipient_housebank] -= amount
        
        # Compute net funding needs
        _,reserves = self.accounts['reserves'].get_balance()
        funding_need = -min(0,sum(amounts_transfers)+reserves)
        
        # >> could be in separate function after checking if funding needs can be met
        # Book transfers on clients' accounts
        for outtransfer in outtransfers:
            recipient = outtransfer.content['recipient']
            sender = outtransfer.sender
            recipient_housebank = housebank_indices[recipient]
            amount = outtransfer.content['amount']
            if recipient_housebank != self.id:
                self.send(outtransfer.sender,'_autobook',dict(debit=[('expenses',amount)],credit=[('money holdings',amount)],text='Transfer'))
                self.send(('household',recipient),'_autobook',dict(debit=[('money holdings',amount)],credit=[('income',amount)],text='Transfer'))
        
        # Only book net transfers between banks (net settlement system)
        for i in range(num_banks):
            amount = -amounts_transfers[i]
            if amount > 0:
                self.accounts.book(debit=[('deposits',amount)],credit=[('reserves',amount)],text='Client transfer')
                self.send(('bank',recipient_housebank),'_autobook',dict(debit=[('deposits',amount)],credit=[('reserves',amount)],text='Client transfer'))

        return funding_need
    
    def give_loan(self):
        for loan_request in self.get_messages('loan_request'):
            amount = loan_request.content['amount']
            self.accounts.book(debit=[('claims',amount)],credit=[('deposits',amount)],text='Loan')
            self.send(loan_request.sender,'_autobook',dict(debit=[('money holdings',amount)],credit=[('loan liabilities',amount)],text='Loan'))

sim = abce.Simulation()
num_banks = 3
num_households = 5
spending_probability = 0.3

banks = sim.build_agents(SimpleBank,'bank', num_banks)
households = sim.build_agents(SimpleHousehold,'household',num_households,num_banks=num_banks)

housebank_indices = list(households.return_housebank())
households.get_outside_money(100)

for r in range(4):
    households.take_loan(100)
    households.transfer_money(housebank_indices)
#    recipients = random.randrange(num_households)
#    amounts = [amount*int(random.random() < spending_probability) for amount in households.return_money_holdings()]
#    households.transfer_money(amounts,recipients,housebank_indices)
    households.transfer_money(housebank_indices)
    banks.handle_transfers(num_banks,housebank_indices)
#    banks.give_loan()
    households._autobook()
    banks._autobook()

#sim.graphs()

