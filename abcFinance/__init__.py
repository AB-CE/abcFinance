# -*- coding: utf-8 -*-
"""
Created on Sun May  6 18:59:39 2018

@author: christoph
"""

import abcEconomics as abce
from .ledger import Ledger
from .account import Account, AccountSide


class Agent(abce.Agent):
    def __init__(self, *param, **kwparam):
        super().__init__(*param, **kwparam)

        self.accounts = Ledger(
            residual_account_name=kwparam.get('residual_account_name', 'equity'))

    def __getattr__(self, attribute):
        if attribute in ['book_end_of_period', 'book', 'make_stock_accounts', 'make_flow_accounts',
                         'make_asset_accounts', 'make_liability_accounts', 'print_profit_and_loss',
                         'print_balance_sheet']:
            return getattr(self.accounts, attribute)
        else:
            raise AttributeError("%s not in agent %s" % (attribute, self.name))

    def _autobook(self, msg):
        self.accounts.book(**msg)


print("HERE")
