# -*- coding: utf-8 -*-
"""
Created on Sun May  6 18:59:39 2018

@author: christoph
"""

import abce
from accountingsystem import AccountingSystem


class Agent(abce.Agent):
    def __init__(self, *param, **kwparam):
        super().__init__(*param, **kwparam)

        if 'residual_account_name' in kwparam:
            self.accounts = AccountingSystem(
                residual_account_name=kwparam['residual_account_name'])
        else:
            self.accounts = AccountingSystem()

    def book_end_of_period(self):
        self.accounts.book_end_of_period()

    def book(self, debit, credit, text=''):
        self.accounts.book(debit, credit, text)

    def make_stock_accounts(self, names):
        self.accounts.make_stock_accounts(names)

    def make_flow_accounts(self, names):
        self.accounts.make_flow_accounts(names)

    def make_asset_accounts(self, names):
        self.accounts.make_stock_accounts(names)

    def make_liability_accounts(self, names):
        self.accounts.make_liability_accounts(names)

    def print_profit_and_loss(self, show_empty_accounts=False):
        self.accounts.print_profit_and_loss(show_empty_accounts)

    def print_balance_sheet(self, show_empty_accounts=False):
        self.accounts.print_balance_sheet(show_empty_accounts)

    def _autobook(self, msg):
        self.accounts.book(**msg.content)
