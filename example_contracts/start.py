import abce
from delivery_contract import Contract as DeliveryContract


class Buyer(abce.Agent):
    def init(self):
        self.create('money', 1000)
        self.contracts = set()

    def issue_contract(self):
        contract = DeliveryContract(self.name, 'cookies', {10: 10, 11: 10, 12: 10, 13: 10}, {10:5, 11:5, 12:5, 13:100})
        self.contracts.add(contract)
        self.send(('seller', 0), 'contract', contract)

    def pay_contracts(self):
        print(self['money'], self['cookies'])
        for contract in self.contracts:
            for action in contract.get_actions(self.name, self.time):
                self.give(contract.counter_party, good=action.action[0], quantity=action.action[1])
                contract.action_executed(self.time)


class Seller(abce.Agent):
    def init(self):
        self.create('cookies', 1000)
        self.contracts = set()

    def accept_contracts(self):
        contracts = self.get_messages('contract')
        for contract in contracts:
            contract.sign(self.name)
            self.contracts.add(contract)

    def deliver_contracts(self):
        for contract in self.contracts:
            for action in contract.get_actions(self.name, self.time):
                self.give(contract.issuing_party, good=action.action[0], quantity=action.action[1])
                contract.action_executed(self.time)


sim = abce.Simulation()

buyers = sim.build_agents(Buyer, 'buyer', number=1)
sellers = sim.build_agents(Seller, 'seller', number=1)



for i in range(20):
    sim.time = i
    if i == 0:
        buyers.issue_contract()
    sellers.accept_contracts()
    sellers.deliver_contracts()
    buyers.pay_contracts()

sim.finalize()


