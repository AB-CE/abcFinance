# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:26:31 2018

@author: christoph
"""

from enum import Enum


class s(Enum):
    """ Side which the balance of an account falls on """
    DEBIT = 1
    CREDIT = -1
    BALANCED = 0

    def __repr__(self):
        return self.name

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
        elif debitsum == creditsum:
            return(s.BALANCED, 0)
        else:
            return (s.CREDIT, creditsum - debitsum)

    def print_balance(self):
        print('debit', self.debit)
        print('credit', self.credit)
