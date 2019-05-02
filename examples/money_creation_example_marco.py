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
Step 1: 
Outside money: 150
Inside credit money: 0 
Inside non-credit money: 0 
Total money: 150
"""
private_agent.book(debit=[('Currency',100)],credit=[('Equity',100)])
bank.book(debit=[('Currency',50)],credit=[('Equity',50)])
central_bank.book(debit=[('Assets',150)],credit=[('Currency',150)])

""" ---------------------------------------------------------------------------
Step 2
Outside money: 150
Inside credit money: 0 
Inside non-credit money: 100 
Total money: 250
"""
private_agent.book(debit=[('Deposits',100)],credit=[('Currency',100)])
bank.book(debit=[('Currency',100)],credit=[('Deposits',100)])

bank.book(debit=[('Reserves',150)],credit=[('Currency',150)])
central_bank.book(debit=[('Currency',150)],credit=[('Reserves',150)])

""" ---------------------------------------------------------------------------
Step 3a
Outside money: 150
Inside credit money: 0 
Inside non-credit money: 100 
Total money: 250
"""
#bank.book(debit=[('Bonds',25)],credit=[('Reserves',25)])
#government.book(debit=[('Reserves',25)],credit=[('Bonds',25)])
#central_bank.book(debit=[('Reserves',25)],credit=[('Government Reserves',25)])

""" ---------------------------------------------------------------------------
Step 3b
Outside money: 150
Inside credit money: 0 
Inside non-credit money: 125 
Total money: 275
"""
government.book(debit=[('Deposits',25)],credit=[('Bonds',25)])

bank.book(debit=[('Bonds',25)],credit=[('Reserves',25)])
bank.book(debit=[('Reserves',25)],credit=[('Government Deposits',25)])
# is equivalent to:
#bank.book(debit=[('Bonds',25)],credit=[('Government Deposits',25)])

""" ---------------------------------------------------------------------------
Step 4
Outside money: 150
Inside credit money: 0 
Inside non-credit money: 100
Total money: 250
"""
private_agent.book(debit=[('Bonds',25)],credit=[('Deposits',25)])
bank.book(debit=[('Deposits',25)],credit=[('Bonds',25)])

""" ---------------------------------------------------------------------------
Step 5
Outside money: 150
Inside credit money: 125
Inside non-credit money: 100
Total money: 375
"""
private_agent.book(debit=[('Deposits',125)],credit=[('Loans',125)])
bank.book(debit=[('Loans',125)],credit=[('Deposits',125)])

private_agent.print_balance_sheet()
bank.print_balance_sheet()
central_bank.print_balance_sheet()
government.print_balance_sheet()