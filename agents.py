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
    
    def _autobook(self):
        for booking in self.get_messages('_autobook'):
            self.accounts.book(**booking.content)
        print(self.name)
        self.accounts.print_profit_and_loss()
        self.accounts.make_end_of_period()
        self.accounts.print_balance_sheet()
    
    def transfer_money(self,housebank_indices):
        recipient = random.randrange(len(housebank_indices))
        recipient_housebank = housebank_indices[recipient]
        _,amount = self.accounts['money holdings'].getBalance()
        amount = random.random() * amount
        self.accounts.book(debit=[('expenses',amount)],credit=[('money holdings',amount)],text='Transfer')
        self.send(('bank',self.housebank),'Outtransfer',{'amount':amount,'recipient':recipient})
        self.send(('bank',recipient_housebank),'Intransfer',{'amount':amount,'sender':self.id})
    
    def get_outside_money(self,amount):
        self.send(('bank',self.housebank),'_autobook',dict(debit=[('claims',amount)], credit=[('deposit',amount)],text='Outside money endowment'))
        self.accounts.book(debit=['money holdings',amount],credit=(['money holdings',amount]),text='Outside money endowment')
        
    def take_loan(self,amount):
        self.send(('bank',self.housebank),'loan_request',{'amount': amount})
        
class SimpleBank(abce.Agent):
    def init(self):
        self.accounts = AccountingSystem(residual_account_name='equity')
        self.accounts.make_stock_account(['reserves','claims','security holdings','deposits','wholesale refinancing'])
        self.accounts.make_flow_account(['interest income','interest expense'])
    
    def _autobook(self):
        for booking in self.get_messages('_autobook'):
            self.accounts.book(**booking.content)
        print(self.name)
        self.accounts.print_profit_and_loss()
        self.accounts.make_end_of_period()
        self.accounts.print_balance_sheet()
        
    def handle_transfers(self,housebank_indices):
        banks = list(set(housebank_indices))
        intransfers = self.get_messages('Intransfer')
        outtransfers = self.get_messages('Outtransfer')
        
        sum_intransfers = 0
        sum_outtransfers = 0
        
        for intransfer in intransfers:
            recipient = intransfer.content['recipient']
            amount = intransfer.content['amount']
        
        
    def give_loan(self):
        for loan_request in self.get_messages('loan_request'):
            amount = loan_request.content['amount']
            self.accounts.book(debit=[('claims',amount)],credit=[('deposits',amount)],text='Loan')
            self.send(loan_request.sender,'_autobook',dict(debit=[('money holdings',amount)],credit=[('loan liabilities',amount)],text='Loan'))



sim = abce.Simulation()
num_banks = 2
num_households = 10

banks = sim.build_agents(SimpleBank,'bank', num_banks)
households = sim.build_agents(SimpleHousehold,'household',num_households,num_banks=num_banks)

housebank_indices = list(households.return_housebank())

for r in range(2):
    households.take_loan(100)
    banks.give_loan()
    households._autobook()
    banks._autobook()

        

