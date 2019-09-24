""" Simple example of a firm with for TDD of accounting.py


"""
from abcFinance import Ledger, Account, AccountSide

def test_tdd():
    accounts = Ledger('equity')

    accounts.make_stock_accounts(['cash', 'claims', 'inventory'])
    accounts.make_flow_accounts(['expenditure', 'revenue', 'cost of goods sold', 'depreciation'])

    accounts.book(
        debit=[('cash', 50), ('claims', 50)],
        credit=[('equity', 100)],
        text="Start with owners' equity, partially paid in")

    assert accounts._check_debit_eq_credit()
    assert accounts.get_total_assets() == 100

    assert accounts['cash'].get_balance() == (AccountSide.DEBIT, 50)
    assert accounts['claims'].get_balance() == (AccountSide.DEBIT, 50)
    assert accounts['equity'].get_balance() == (AccountSide.CREDIT, 100)

    #print('Initial balance')
    #accounts.print_balance_sheet()

    #print('Some purchases and operating expenses')
    accounts.book(debit=[('expenditure', 20)], credit=[('cash', 20)],text="General expenses")
    assert accounts.get_total_assets() == 80, accounts.get_total_assets()
    accounts.book(debit=[('inventory',20)],credit=[('cash',20)],text="Purchase of equipment")
    accounts.book(debit=[('depreciation',2)],credit=[('inventory',2)],text="Depreciation")
    #accounts.print_profit_and_loss()

    #print('Balance sheet after first period')
    accounts.book_end_of_period()
    #accounts.print_balance_sheet()
    assert accounts['equity'].get_balance() == (AccountSide.CREDIT, 78)
    assert accounts['cash'].get_balance() == (AccountSide.DEBIT, 10),accounts['cash'].get_balance()

    #print('Profitable sale')
    accounts.book(debit=[('cash',40)],credit=[('revenue',40)],text="Sale of goods")
    accounts.book(debit=[('cost of goods sold',10)],credit=[('inventory',10)],text="Sale of goods")
    #accounts.print_profit_and_loss()
    assert accounts['inventory'].get_balance() == (AccountSide.DEBIT, 8)

    #print('Balance sheet after second period')
    accounts.book_end_of_period()
    #accounts.print_balance_sheet()
    assert accounts['equity'].get_balance() == (AccountSide.CREDIT, 108)
