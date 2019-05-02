from abcFinance import Ledger, Account, AccountSide

""" ---------------------------------------------------------------------------
Initialize agents
"""
bank = Ledger(residual_account_name="equity")
household = Ledger(residual_account_name="equity")
bank_owner = Ledger(residual_account_name="equity")

bank.make_stock_accounts(['loans','reserves','deposits'])
household.make_stock_accounts(['money holdings','loan liabilities'])
bank_owner.make_stock_accounts(['money holdings','participations'])

bank.make_flow_accounts(['income','expenses'])
household.make_flow_accounts(['income','expenses'])
bank_owner.make_flow_accounts(['income','expenses'])

""" ---------------------------------------------------------------------------
Initialize balance sheets (outside money endowments)
"""
household.book(debit=[('money holdings',100)],credit=[('equity',100)],text='Initial endowment')
bank.book(debit=[('reserves',100)],credit=([('deposits',100)]),text='Initial endowment')
""" ---------------------------------------------------------------------------
Granting of a loan
"""
bank.book(debit=[('loans',100)],credit=[('deposits',100)],text='Loan granting')
household.book(debit=[('money holdings',100)],credit=[('loan liabilities',100)],text='Take out loan')
""" ---------------------------------------------------------------------------
Interest payment
"""
bank.book(debit=[('deposits',5)],credit=[('income',5)],text='Interest payment')
household.book(debit=[('expenses',5)],credit=[('money holdings',5)],text='Interest payment')
""" ---------------------------------------------------------------------------
Principal repayment
"""
bank.book(debit=[('deposits',100)],credit=[('loans',100)],text='Principal repayment')
household.book(debit=[('loan liabilities',100)],credit=[('money holdings',100)],text='Principal repayment')
""" ---------------------------------------------------------------------------
Dividend payment
"""
bank.book(debit=[('equity',5)],credit=[('deposits',5)],text='Dividend payout')
bank_owner.book(debit=[('money holdings',5)],credit=[('income',5)],text='Dividend income')

bank.book_end_of_period()
household.book_end_of_period()
bank_owner.book_end_of_period()




print('Bank initial balance sheet')
bank.print_balance_sheet()
print('Household initial balance sheet')
household.print_balance_sheet()
print('Bank owner initial balance sheet')
bank_owner.print_balance_sheet()


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


The bank would credit loans and debit deposits with 100

book CREDIT: Loans 100 // DEBIT: Deposits 100, giving the balance sheet shown in figure 1

bank = Ledger(residual_account_name="equity")
bank.make_stock_accounts(['loans','tangibles','reserves','deposits'])

bank.book(debit=[('reserves',100)],credit=([('equity',100)]))
bank.book(debit=[('loans',1000)],credit=([('deposits',1000)]))

bank.book(debit=[('tangibles',50)],credit=([('reserves',50)]))
bank.book(debit=[('reserves',50)],credit=([('deposits',50)]))

