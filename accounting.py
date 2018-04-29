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
        for name, account in self.stock_accounts.items():
            print (name, account.get_balance())

    def print_profit_and_loss(self):
        for name, account in self.flow_accounts.items():
            print (name, account.get_balance())

    def book(self, debit, credit):
        assert sum([value for _, value in debit]) == \
            sum([value for _, value in credit])

        for account, value in debit:
            self.accounts[account].debit.append(value)

        for account, value in credit:
            self.accounts[account].credit.append(value)

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
            if side == s.DEBIT:
                profit -= balance
                credit_accounts.append((name,balance))
            else:
                profit += balance
                debit_accounts.append((name,balance))

        if profit > 0:
            credit_accounts.append((self.residual_account_name,profit))
        else:
            debit_accounts.append((self.residual_account_name,-profit))

        self.book(debit=debit_accounts, credit=credit_accounts)

        for account in self.flow_accounts:
            account = Account()

accounts = AccountingSystem('equity')


accounts.make_stock_account(['cash', 'claims'])
accounts.make_flow_account(['expenditure'])

accounts.book(
    debit=[('cash', 50), ('claims', 50)],
    credit=[('equity', 100)])

assert accounts._check_debit_eq_credit()
assert accounts.get_total_assets() == 100

assert accounts['cash'].get_balance() == (s.DEBIT, 50)
assert accounts['claims'].get_balance() == (s.DEBIT, 50)
assert accounts['equity'].get_balance() == (s.CREDIT, 100)

accounts.book(debit=[('expenditure', 20)], credit=[('cash', 20)])

assert accounts.get_total_assets() == 80, accounts.get_total_assets()

accounts.print_profit_and_loss()
print('--')
accounts.make_end_of_period()

accounts.print_profit_and_loss()

accounts.print_balance_sheet()

assert accounts['equity'].get_balance() == (s.CREDIT, 80)
