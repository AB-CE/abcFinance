from enum import Enum


class s(Enum):
    DEBIT = 0
    CREDIT = 1


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


class AccountingSystem:
    def __init__(self, residual_account_name='equity'):
        self.stock_accounts = {}
        self.flow_accounts = {}
        self.accounts = {}
        self.residual_account = None
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

    def list_books(self):
        return list(self.accounts)

    def book(self, debit, credit):
        assert sum([value for _, value in debit]) == \
            sum([value for _, value in credit])

        for account, value in debit:
            self.accounts[account].debit.append(value)

        for account, value in credit:
            self.accounts[account].credit.append(value)

    def get_total_assets(self):
        balance = 0
        for account in self.stock_accounts.values():
            balance += sum(account.debit)
        return balance

    def _check_debit_eq_credit(self):
        debitsum = 0
        creditsum = 0
        for account in self.accounts.values():
            debitsum += sum(account.debit)
            creditsum += sum(account.credit)
        return debitsum == creditsum









accounts = AccountingSystem()


accounts.make_stock_account(['cash', 'claims', 'equity'])
accounts.make_flow_account(['expenditure'])

accounts.book(
    debit=[('cash', 50), ('claims', 50)],
    credit=[('equity', 100)])

assert accounts._check_debit_eq_credit()
assert accounts.get_total_assets() == 100

assert accounts['cash'].get_balance() == (s.DEBIT, 50)
assert accounts['claims'].get_balance() == (s.DEBIT, 50)
assert accounts['equity'].get_balance() == (s.CREDIT, 100)

accounts.book(debit=[('expenditure',20)], credit=[('cash',20)])

assert accounts.get_total_assets() == 80, accounts.get_total_assets()

assert accounts['equity'].get_balance() == 80
