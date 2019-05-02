from abcFinance import Ledger, Account, AccountSide

""" ---------------------------------------------------------------------------
Declare agents
"""
bank = Ledger(residual_account_name="Equity")
private_agent = Ledger(residual_account_name="Equity")
central_bank = Ledger(residual_account_name="Equity")
government = Ledger(residual_account_name="Equity")

bank.make_stock_accounts(['Currency','Loans','Reserves','Bonds','Deposits','Government Deposits','Wholesale Deposits'])
private_agent.make_stock_accounts(['Currency','Deposits','Loans'])
central_bank.make_stock_accounts(['Assets','Reserves','Government Reserves','Currency'])
government.make_stock_accounts(['Deposits','Bonds','Reserves'])

""" ---------------------------------------------------------------------------
Initialize agents' balance sheets
"""
private_agent.book(debit=[('Currency',100)],credit=[('Equity',100)],text='(1)')
bank.book(debit=[('Currency',50)],credit=[('Equity',50)],text='(1)')
central_bank.book(debit=[('Assets',150)],credit=[('Currency',150)],text='(1)')

private_agent.book(debit=[('Deposits',100)],credit=[('Currency',100)],text='(2)')
bank.book(debit=[('Currency',100)],credit=[('Deposits',100)],text='(2)')

bank.book(debit=[('Reserves',150)],credit=[('Currency',150)],text='(3)')
central_bank.book(debit=[('Currency',150)],credit=[('Reserves',150)],text='(2)')

""" ---------------------------------------------------------------------------
Take out a loan
"""
private_agent.book(debit=[('Deposits',850)],credit=[('Loans',850)],text='(3)')
bank.book(debit=[('Loans',850)],credit=[('Deposits',850)],text='(4)')

""" ---------------------------------------------------------------------------
Bank buys a government bond
"""
government.book(debit=[('Reserves',100)],credit=[('Bonds',100)],text='(1)')
bank.book(debit=[('Bonds',100)],credit=[('Reserves',100)],text='(5)')
government.book(debit=[('Deposits',100)],credit=[('Reserves',100)],text='(1)')
bank.book(debit=[('Reserves',100)],credit=[('Deposits',100)],text='(5)')

government.book(debit=[('Deposits',100)],credit=[('Bonds',100)],text='(1)')
bank.book(debit=[('Bonds',100)],credit=[('Deposits',100)],text='(5)')



private_agent.print_balance_sheet()
bank.print_balance_sheet()
central_bank.print_balance_sheet()
government.print_balance_sheet()