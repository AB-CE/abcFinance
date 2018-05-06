# -*- coding: utf-8 -*-
"""
Created on Sun May  6 18:59:39 2018

@author: christoph
"""

from accounting import AccountingSystem,Account,s
import abce

class AccountingAgent(abce.Agent):
    def __init__(self, *param, **kwparam):
        super().__init__(*param,**kwparam)
        
        if 'residual_account_name' in kwparam['agent_arguments']:
            residual_account_name = kwparam['agent_arguments']['residual_account_name']
            self.accounts = AccountingSystem(residual_account_name = residual_account_name)
        else:
            self.accounts = AccountingSystem()