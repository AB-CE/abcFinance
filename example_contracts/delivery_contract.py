""" abcFinance specifies a contract API. This allows the user to use the full
    python language to specify contracts.

    Both / all contract parties get a copy of the contract.
"""


class Action:
    """ An action has to properties. The action to be executed and further information.
    This could be for example whether the action is obligatory or not.

    Example::

        Action(('pay', 50, 'UBS'), 'compulsory')

    The action property and more_info, can have any content the tuple
    ('pay', 50, 'UBV') is just and example.
    """
    def __init__(self, action, more_info=None):
        self.action = action
        """ self.action, action to be executed, """
        self.more_info = more_info
        """ self.more_info, further information """


class Contract:
    """ A contract is a tree or sequence of :class:`Action`s. A contract must implement :method:`get_action`, which
        gives the next action given the current time and relevant state. Further it must implement
        :method:`action_executed`, which is lets the contract know that an action has been is executed.

        Optionally is_terminated should return whether the contract is terminated.

        In order to use a contract with a book keeping system :method:`get_valuation` needs to return
        the valuation

    """
    def __init__(self, issuing_party, good, deliveries, payments):
        self._last_valuation = None
        self.issuing_party = issuing_party
        self.counter_party = None
        self.deliveries = {time: Action((good, delivery)) for time, delivery in deliveries.items()}
        self.payments = {time: Action(('money', delivery), 'conditional') for time, delivery in payments.items()}
        self.executed = set()

    def sign(self, party):
        """ Signs the contract and sets the self.counter_party property """
        self.counter_party = party

    def get_actions(self, party, time, *_, **__):
        """ Returns a list of actions that have to or could be executed now
        arguments are the current time and any state informations that are
        necessary to decide which actions have to could be taken.

        Example::

            if self.issuing_party == party:
                if self.num_excecuted_payments < self.number_of_payments_required:
                    return [Action(('pay', self.amount), 'at_least_3_times')]
            else:
                return []
        """
        if party == self.counter_party:
            if time in self.deliveries:
                return [self.deliveries[time]]
        elif party == self.issuing_party:
            if time in self.executed:
                if time in self.payments:
                    return [self.payments[time]]

        return []


    def action_executed(self, time):
        """ Let the contract know that a particular obligation has been executed.
        This is used by the agent that execute the obligation on his copy and by
        the receiving agent on his copy of the contract.

        Example::

            self.num_excecuted_payments += 1"""

        self.executed.add(time)

    def get_valuation(self, party, time, *_, **__):
        """ returns a valuation of the contract.
        Arguments:
            party, the party for whom the valuation is made
            time, current time
            other state variables necessary for the valuation
        """
        raise NotImplementedError

    def is_terminated(self):
        """ Whether the contract is terminated.

        Example::

            if.num_excecuted_payments >= self.number_of_payments_required:
                return True
            else:
                return False
        """
        raise NotImplementedError

    def get_last_valuation(self):
        return self._last_valuation
