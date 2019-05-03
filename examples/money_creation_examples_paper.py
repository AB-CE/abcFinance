from abcFinance import Ledger, Account, AccountSide

""" ---------------------------------------------------------------------------
Declare agents
"""
bank = Ledger(residual_account_name="Equity")
private_agent = Ledger(residual_account_name="Equity")
central_bank = Ledger(residual_account_name="Equity")
government = Ledger(residual_account_name="Equity")

bank.make_stock_accounts(['Currency','Loans','Reserves','Bonds','Deposits','Government Deposits','Wholesale Deposits'])
private_agent.make_stock_accounts(['Currency','Deposits','Loans','Bonds'])
central_bank.make_stock_accounts(['Assets','Reserves','Government Reserves','Currency'])
government.make_stock_accounts(['Deposits','Bonds','Reserves'])

""" ---------------------------------------------------------------------------
Initialize agents' balance sheets
"""
private_agent.book(debit=[('Currency',500)],credit=[('Equity',500)])
bank.book(debit=[('Currency',50)],credit=[('Equity',50)])
central_bank.book(debit=[('Assets',550)],credit=[('Currency',550)])

private_agent.book(debit=[('Deposits',500)],credit=[('Currency',500)])
bank.book(debit=[('Currency',500)],credit=[('Deposits',500)])

bank.book(debit=[('Reserves',550)],credit=[('Currency',550)])
central_bank.book(debit=[('Currency',550)],credit=[('Reserves',550)])

""" ---------------------------------------------------------------------------
Bank buys a government bond
"""
government.book(debit=[('Reserves',400)],credit=[('Bonds',400)])
bank.book(debit=[('Bonds',400)],credit=[('Reserves',400)])
central_bank.book(debit=[('Reserves',400)],credit=[('Government Reserves',400)])

""" ---------------------------------------------------------------------------
Private agent buys the bond from the bank
"""
private_agent.book(debit=[('Bonds',100)],credit=[('Deposits',100)])
bank.book(debit=[('Deposits',100)],credit=[('Bonds',100)])

""" ---------------------------------------------------------------------------
Take out a loan
"""
private_agent.book(debit=[('Deposits',550)],credit=[('Loans',550)])
bank.book(debit=[('Loans',550)],credit=[('Deposits',550)])

private_agent.print_balance_sheet()
bank.print_balance_sheet()
central_bank.print_balance_sheet()
government.print_balance_sheet()