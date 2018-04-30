""" Project pastis is a simples implementation of an double entry book keeping system

Initialize the accounting system with, the name of the residual_account::

    accounts = AccountingSystem('equity')

Create stock and flow account:

    accounts.make_stock_account(['cash', 'claims'])
    accounts.make_flow_account(['expenditure'])

In order to book give a list of credit and debit tuples. Each tuple should be
an account and a value::

    accounts.book(
        debit=[('cash', 50), ('claims', 50)],
        credit=[('equity', 100)])

get balance gives you the balance of an account:

    assert accounts['cash'].get_balance() == (s.DEBIT, 50)

Balance sheet

    accounts.book(debit=[('expenditure', 20)], credit=[('cash', 20)])

    assert accounts.get_total_assets() == 80, accounts.get_total_assets()

    accounts.print_profit_and_loss()
    print('--')
    accounts.make_end_of_period()

    accounts.print_profit_and_loss()

    accounts.print_balance_sheet()

    assert accounts['equity'].get_balance() == (s.CREDIT, 80)


"""
from enum import Enum


class s(Enum):
    DEBIT = 0
    CREDIT = 1

    def __repr__(self):
        return self.name


class Account:
    def __init__(self):
        self.debit = []
        self.credit = []

    def get_balance(self):
        debitsum = sum(self.debit)
        creditsum = sum(self.credit)
        if debitsum > creditsum:
            return (s.DEBIT, debitsum - creditsum)
        else:
            return (s.CREDIT, creditsum - debitsum)

    def print_balance(self):
        print('debit', self.debit)
        print('credit', self.credit)


class AccountingSystem:
    def __init__(self, residual_account_name='equity'):
        self.stock_accounts = {}
        self.flow_accounts = {}
        self.accounts = {}
        self.residual_account = None
        self.profit_history = []
        self.booking_history = []
        self.residual_account_name = residual_account_name
        self.make_residual_account(residual_account_name)

    def __getitem__(self, item):
        return self.accounts[item]

    def make_stock_account(self, names):
        for name in names:
            account = Account()
            self.stock_accounts[name] = account
            self.accounts[name] = account

    def make_flow_account(self, names):
        for name in names:
            account = Account()
            self.flow_accounts[name] = account
            self.accounts[name] = account

    def make_residual_account(self, name):
        account = Account()
        self.stock_accounts[name] = account
        self.accounts[name] = account
        self.residual_account = account

    def print_balance_sheet(self):
        print('Stock accounts:')
        for name, account in self.stock_accounts.items():
            print (name, ":", account.get_balance())
        print('--')

    def print_profit_and_loss(self):
        profit = 0
        print('Flow accounts:')
        for name, account in self.flow_accounts.items():
            side, balance = account.get_balance()
            if balance != 0:
                print (name, ":", side, balance)
                if side == s.DEBIT:
                    profit -= balance
                else:
                    profit += balance
        print("Profit for period: ", profit)
        print('--')

    def book(self, debit, credit, text=""):
        assert sum([value for _, value in debit]) == \
            sum([value for _, value in credit])

        for account, value in debit:
            self.accounts[account].debit.append(value)

        for account, value in credit:
            self.accounts[account].credit.append(value)

        self.booking_history.append((text, debit, credit))

    def get_total_assets(self):
        total_assets = 0
        for account in self.stock_accounts.values():
            side, balance = account.get_balance()
            if side == s.DEBIT:
                total_assets += balance
        return total_assets

    def _check_debit_eq_credit(self):
        debitsum = 0
        creditsum = 0
        for account in self.accounts.values():
            debitsum += sum(account.debit)
            creditsum += sum(account.credit)
        return debitsum == creditsum

    def make_end_of_period(self):
        profit = 0
        debit_accounts = []
        credit_accounts = []
        for name, account in self.flow_accounts.items():
            side, balance = account.get_balance()
            if balance > 0:
                if side == s.DEBIT:
                    profit -= balance
                    credit_accounts.append((name, balance))
                else:
                    profit += balance
                    debit_accounts.append((name, balance))

        self.profit_history.append((debit_accounts, credit_accounts))

        if profit > 0:
            credit_accounts.append((self.residual_account_name, profit))
        else:
            debit_accounts.append((self.residual_account_name, -profit))

        self.book(debit=debit_accounts, credit=credit_accounts, text='Period close')
        self.booking_history.append('end of period')

        for account in self.flow_accounts:
            account = Account()


accounts = AccountingSystem('equity')


accounts.make_stock_account(['cash', 'claims', 'inventory'])
accounts.make_flow_account(['expenditure', 'revenue', 'cost of goods sold', 'depreciation'])

accounts.book(
    debit=[('cash', 50), ('claims', 50)],
    credit=[('equity', 100)],
    text="Start with owners' equity, partially paid in")

assert accounts._check_debit_eq_credit()
assert accounts.get_total_assets() == 100

assert accounts['cash'].get_balance() == (s.DEBIT, 50)
assert accounts['claims'].get_balance() == (s.DEBIT, 50)
assert accounts['equity'].get_balance() == (s.CREDIT, 100)

print('Initial balance')
accounts.print_balance_sheet()

print('Some purchases and operating expenses')
accounts.book(debit=[('expenditure', 20)], credit=[('cash', 20)],text="General expenses")
assert accounts.get_total_assets() == 80, accounts.get_total_assets()
accounts.book(debit=[('inventory',20)],credit=[('cash',20)],text="Purchase of equipment")
accounts.book(debit=[('depreciation',2)],credit=[('inventory',2)],text="Depreciation")
accounts.print_profit_and_loss()

print('Balance sheet after first period')
accounts.make_end_of_period()
accounts.print_balance_sheet()
assert accounts['equity'].get_balance() == (s.CREDIT, 78)
assert accounts['cash'].get_balance() == (s.DEBIT, 10),accounts['cash'].get_balance()

print('Profitable sale')
accounts.book(debit=[('cash',40)],credit=[('revenue',40)],text="Sale of goods")
accounts.book(debit=[('cost of goods sold',10)],credit=[('inventory',10)],text="Sale of goods")
accounts.print_profit_and_loss()
assert accounts['inventory'].get_balance() == (s.DEBIT, 8)

print('Balance sheet after second period')
accounts.make_end_of_period()
accounts.print_balance_sheet()
assert accounts['equity'].get_balance() == (s.CREDIT, 108)
