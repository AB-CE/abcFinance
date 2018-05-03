""" abcFinance is an implementation of an double entry book keeping system

Initialize the accounting system with, the name of the residual_account::

    accounts = AccountingSystem(residual_account_name='equity')

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

class AccountingSystem:
    """ The main class to be initialized """
    def __init__(self, residual_account_name='equity'):
        self.stock_accounts = {}
        self.flow_accounts = {}
        self.accounts = {}
        self.residual_account = None
        self.profit_history = []
        self.booking_history = []
        self.residual_account_name = residual_account_name
        self._make_residual_account(residual_account_name)
        self.show_empty_flow_accounts = False
        self.show_empty_stock_accounts = False

    def __getitem__(self, item):
        return self.accounts[item]

    def make_stock_account(self, names):
        """ Create stock accounts.

        Args:
            names, list of names for the accounts
        """
        for name in names:
            account = Account()
            self.stock_accounts[name] = account
            self.accounts[name] = account

    def make_flow_account(self, names):
        """ Create flow accounts.

        Args:
            names, list of names for the accounts
        """
        for name in names:
            account = Account()
            self.flow_accounts[name] = account
            self.accounts[name] = account

    def _make_residual_account(self, name):
        account = Account()
        self.stock_accounts[name] = account
        self.accounts[name] = account
        self.residual_account = account

    def book(self, debit, credit, text=""):
        """ Book a transaction.

        Arguments:
            debit, list of tuples ('account', amount)

            credit, list of tuples ('account', amount)

            text, for booking history

        Example::

            accounts.book(debit=[('inventory',20)], credit=[('cash',20)], text="Purchase of equipment")
        """
        sum_debit = 0
        sum_credit = 0
        
        for _,value in debit:
            assert value >= 0
            sum_debit += value
        
        for _,value in credit:
            assert value >= 0
            sum_credit += value
        
        assert sum_debit == sum_credit
        
        if sum_debit > 0:
            for account, value in debit:
                self.accounts[account].debit.append(value)
    
            for account, value in credit:
                self.accounts[account].credit.append(value)
    
            self.booking_history.append((debit, credit, text))

    def make_end_of_period(self):
        """ Close flow accounts and credit/debit residual (equity) account """
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

        for account in self.flow_accounts:
            account = Account()

    def print_balance_sheet(self):
        """ Print a balance sheets """
        print('Asset accounts:')
        total_assets = 0
        for name, account in self.stock_accounts.items():
            side, balance = account.get_balance()
            if side == s.DEBIT:
                if name == self.residual_account_name:
                    equity = -balance
                else:
                    total_assets += balance
                    if balance != 0 or self.show_empty_stock_accounts:
                        print ("  ",name, ":", balance)
        print('Liability accounts:')
        for name, account in self.stock_accounts.items():
            side, balance = account.get_balance()
            if side == s.CREDIT:
                if name == self.residual_account_name:
                    equity = balance
                else:
                    if balance != 0 or self.show_empty_stock_accounts:
                        print ("  ",name, ":", balance)
        print('Equity: ',equity)
        print('Total Assets: ',total_assets)
        print('--')

    def print_profit_and_loss(self):
        """ Print profit and loss statement """
        profit = 0
        print('Flow accounts:')
        for name, account in self.flow_accounts.items():
            side, balance = account.get_balance()
            if balance != 0 or self.show_empty_flow_accounts:
                if side == s.DEBIT:
                    print ("  ",name, ":", -balance)
                    profit -= balance
                else:
                    print ("  ",name, ":", balance)
                    profit += balance
        print("Profit for period: ", profit)
        capital_actions = False
        for booking_statement in reversed(self.booking_history):
            debit, credit, text = booking_statement
            if text == "Period close":
                break
            for account, value in debit:
                if account == self.residual_account_name:
                    if not capital_actions:
                        print("Profit distribution and capital actions")
                        capital_actions = True
                    print("  ",text,":",-value)
            for account, value in credit:
                if account == self.residual_account_name:
                    if account == self.residual_account_name:
                        if not capital_actions:
                            print("Profit distribution and capital actions")
                            capital_actions = True
                    print("  ",text,":",value)
        print('--')
    
    def get_total_assets(self):
        """ Return total assets. """
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

class Account:
    """ An account has two lists of debit and credit bookings """
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

class s(Enum):
    """ Side which the balance of an account falls on """
    DEBIT = 0
    CREDIT = 1

    def __repr__(self):
        return self.name