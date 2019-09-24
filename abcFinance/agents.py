import abcEconomics

class Accountant(abcEconomics.Agent):
    def __init__(self, *param, **kwparam):
        super().__init__(*param, **kwparam)

        self.accounts = Ledger(
            residual_account_name=kwparam.get('residual_account_name', 'Equity'))

    def _autobook(self, msg):
        self.accounts.book(**msg.content)
