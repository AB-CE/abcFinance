# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 18:29:14 2018

@author: christoph
"""

""" ---------------------------------------------------------------------------
Set up the system
"""
from abcFinance import Ledger, Account, AccountSide

def test_banking():
    bank = Ledger(residual_account_name="equity")
    household = Ledger(residual_account_name="equity")

    bank.make_stock_accounts(['reserves','claims','security holdings','deposits','wholesale refinancing'])
    household.make_stock_accounts(['money holdings','loan liabilities'])
    bank.make_flow_accounts(['interest income','interest expense'])
    household.make_flow_accounts(['income','expenses'])

    """ ---------------------------------------------------------------------------
    Initialize balance sheets (outside money endowments)
    """
    household.book(debit=[('money holdings',100)],credit=[('equity',100)],text='Initial endowment')
    bank.book(debit=[('reserves',100)],credit=([('deposits',100)]),text='Initial endowment')
    print('Bank initial balance sheet')
    bank.print_balance_sheet()
    print('Household initial balance sheet')
    household.print_balance_sheet()

    """ ---------------------------------------------------------------------------
    Granting of a loan
    """
    bank.book(debit=[('claims',10)],credit=[('deposits',10)],text='Loan')
    household.book(debit=[('money holdings',10)],credit=[('loan liabilities',10)],text='Loan')
    print('Bank balance sheet after granting a loan')
    bank.print_balance_sheet()
    print('Household balance sheet after granting a loan')
    household.print_balance_sheet()

    """ ---------------------------------------------------------------------------
    Interest payment
    """
    bank.book(debit=[('deposits',1)],credit=[('interest income',1)],text='Interest payment')
    household.book(debit=[('expenses',1)],credit=[('money holdings',1)],text='Interest payment')
    print('Bank PnL after interest payment')
    bank.print_profit_and_loss()
    print('Household PnL after interest payment')
    household.print_profit_and_loss()
    bank.book_end_of_period()
    household.book_end_of_period()

    print('Bank balance sheet after interest payment')
    bank.print_balance_sheet()
    print('Household balance sheet after interest payment')
    household.print_balance_sheet()

    """ ---------------------------------------------------------------------------
    Principal repayment
    """
    bank.book(debit=[('deposits',10)],credit=[('claims',10)],text='Principal repayment')
    household.book(debit=[('loan liabilities',10)],credit=[('money holdings',10)],text='Principal repayment')
    print('Bank balance sheet after principal repayment')
    bank.print_balance_sheet()
    print('Household balance sheet after principal repayment')
    household.print_balance_sheet()

    """ ---------------------------------------------------------------------------
    Dividend payment
    """
    bank.book(debit=[('equity',1)],credit=[('deposits',1)],text='Dividend payment')
    household.book(debit=[('money holdings',1)],credit=[('income',1)],text='Dividend payment')
    print('Bank PnL after interest payment')
    bank.print_profit_and_loss()
    print('Household PnL after interest payment')
    household.print_profit_and_loss()
    bank.book_end_of_period()
    household.book_end_of_period()
    print('Bank balance sheet after dividend payment')
    bank.print_balance_sheet()
    print('Household balance sheet after dividend payment')
    household.print_balance_sheet()
test_banking()