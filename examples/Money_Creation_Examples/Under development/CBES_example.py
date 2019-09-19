""" ---------------------------------------------------------------------------
Implementation of the booking process described in:
https://www.treasurydirect.gov/instit/auctfund/held/cbes/cbes.htm
"""

from abcFinance import Ledger, Account, AccountSide

""" ---------------------------------------------------------------------------
Declare agents
"""
fed = Ledger(residual_account_name="Equity")
depository_A = Ledger(residual_account_name="Equity")
depository_B = Ledger(residual_account_name="Equity")
broker_M = Ledger(residual_account_name="Equity")
fi_J = Ledger(residual_account_name="Equity")

fed.make_stock_accounts(['Securities Holdings','Securities belonging to Depository A','Securities belonging to Depository B','Reserves Depository A','Reserves Depository B','Assets'])
depository_A.make_stock_accounts(['Securities Holdings','Securities belonging to Broker M','Reserves','Deposits by Broker M'])
depository_B.make_stock_accounts(['Securities Holdings','Securities belonging to Financial Institution J','Reserves','Deposits by Financial Institution J'])
broker_M.make_stock_accounts(['Securities Holdings','Securities belonging to Customers','Reserves with Depository A','Customer Deposits'])
fi_J.make_stock_accounts(['Securities Holdings','Securities belonging to Customers','Reserves with Depository B','Customer Deposits'])


""" ---------------------------------------------------------------------------
Initialize balance sheets (all symmetric balance sheets with 0 equity, for simplicity)
"""
fed.book(debit=[('Securities Holdings',1000)],credit=[('Securities belonging to Depository A',500),('Securities belonging to Depository B',500)])
fed.book(debit=[('Assets',2000)],credit=[('Reserves Depository A',1000),('Reserves Depository B',1000)])
depository_A.book(debit=[('Securities Holdings',1000)],credit=[('Securities belonging to Broker M',1000)])
depository_A.book(debit=[('Reserves',1000)],credit=[('Deposits by Broker M',1000)])
depository_B.book(debit=[('Securities Holdings',1000)],credit=[('Securities belonging to Financial Institution J',1000)])
depository_B.book(debit=[('Reserves',1000)],credit=[('Deposits by Financial Institution J',1000)])
broker_M.book(debit=[('Securities Holdings',1000)],credit=[('Securities belonging to Customers',1000)])
broker_M.book(debit=[('Reserves with Depository A',1000)],credit=[('Customer Deposits',1000)])
fi_J.book(debit=[('Securities Holdings',1000)],credit=[('Securities belonging to Customers',1000)])
fi_J.book(debit=[('Reserves with Depository B',1000)],credit=[('Customer Deposits',1000)])

print('Initial balance sheets:')
fed.print_balance_sheet()
depository_A.print_balance_sheet()
depository_B.print_balance_sheet()
broker_M.print_balance_sheet()
fi_J.print_balance_sheet()

""" ---------------------------------------------------------------------------
Transfer of a security from a customer of Broker M to a customer of Financial Institution J
The booking statements on the customers' balance sheet are left out for brevity, they would be completely analogous
"""
broker_M.book(debit=[('Securities belonging to Customers',500)],credit=[('Securities Holdings',500)])
depository_A.book(debit=[('Securities belonging to Broker M',500)],credit=[('Securities Holdings',500)])
fed.book(debit=[('Securities belonging to Depository A',500)],credit=[('Securities belonging to Depository B',500)])
depository_B.book(debit=[('Securities Holdings',500)],credit=[('Securities belonging to Financial Institution J',500)])
fi_J.book(debit=[('Securities Holdings',500)],credit=[('Securities belonging to Customers',500)])

""" ---------------------------------------------------------------------------
Transfer of the payment in the opposite direction
"""
fi_J.book(debit=[('Customer Deposits',500)],credit=[('Reserves with Depository B',500)])
depository_B.book(debit=[('Deposits by Financial Institution J',500)],credit=[('Reserves',500)])
fed.book(debit=[('Reserves Depository B',500)],credit=[('Reserves Depository A',500)])
depository_A.book(debit=[('Reserves',500)],credit=[('Deposits by Broker M',500)])
broker_M.book(debit=[('Reserves with Depository A',500)],credit=[('Customer Deposits',500)])

print('Final balance sheets:')
fed.print_balance_sheet()
depository_A.print_balance_sheet()
depository_B.print_balance_sheet()
broker_M.print_balance_sheet()
fi_J.print_balance_sheet()
