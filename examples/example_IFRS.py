# -*- coding: utf-8 -*-
"""
Created on Wed May  2 15:23:48 2018

@author: christoph
"""

from accounting import AccountingSystem,Account,s

corporation = AccountingSystem(residual_account_name='Retained earnings')
bank = AccountingSystem(residual_account_name='Retained earnings')

corporation.make_stock_account([
        # Non-current assets
        'Property, plant and equipment',
        'Investment properties',
        'Intangible assets',
        'Deferred tax assets',
        'At-equity-accounted investments',
        'Held-to-maturity investments',
        'Available-for-sale financial assets',
        # Current assets
        'Inventories',
        'Receivables',
        'Derivative financial instruments assets',
        'Financial assets at fair value through profit or loss',
        'Cash and cash equivalents',
        'Assets classified as held for sale',
        # Non-current liabilities
        'Borrowings',
        'Deferred tax liabilities',
        'Employee benefit obligations',
        'Provisions',
        # Current liabilities
        'Payables',
        'Current tax liabilities',
        'Derivative financial instruments liabilities',
        'Provisions',
        'Deferred revenue',
        'Liabilities associated with assets classified as held for sale',
        # Equity
        'Share capital'
        ])

corporation.make_flow_account([
        # Continuing operations
        'Revenue',
        'Cost of goods sold',
        'Cost of services provided',
        # = Gross profit
        'Depreciation and amortisation',
        'Administrative expenses',
        'Other income',
        'Other gains/losses',
        # = Operationg profit
        'Finance income',
        'Finance costs',
        'Net income from at-equity investments',
        # = Profit before income tax
        'Income tax expense',
        # = Profit from continuing operations
        'Net income from discontinued operations'
        # Profit for the period
        ])

bank.make_stock_account([
        # Assets
        'Cash and central bank reserves',
        'Loans and advances to banks',
        'Loans and advances to customers',
        'Central bank funds sold and securities purchased under resale agreements',
        'Securities borrowed',
        'FV through PnL assets - Trading assets',
        'FV through PnL assets - Positive market values from derivatives',
        'FV through PnL assets - Financial assets',
        'Financial assets available for sale',
        'At-equity-accounted investments',
        'Held-to-maturity investments',
        'Property, plant and equipment',
        'Goodwill and other intangible assets',
        'Deferred tax assets',
        'Other assets',
        # Liabilities
        'Deposits from customers',
        'Deposits from banks',
        'Central bank funds purchased and securities sold under repurchase agreements',
        'Securities loaned',
        'FV through PnL liabilities - Trading liabilities',
        'FV through PnL liabilities - Negative market values from derivatives',
        'FV through PnL liabilities - Financial liabilities',
        'FV through PnL liabilities - Investment contract liabilities',
        'Other short-term borrowings',
        'Provisions',
        'Deferred tax liabilities',
        'Long-term debt',
        'Other liabilities',
        # Equity
        'Share capital'
        ])

bank.make_flow_account([
        'Interest income',
        'Interest expenses',
        'Fee and commission income',
        'Fee and commission expenses',
        'Trading income',
        'Trading expenses',
        'Net income from financial instruments at fair value through profit or loss',
        'Net income from financial assets available for sale',
        'Net income from at-equity investments',
        'Other operating income',
        'Other operating expenses',
        # = Operating result
        'Compensation and benefits',
        'Administrative expenses',
        'Impairment of goodwill',
        'Depreciation and amortisation',
        'Provisions',
        'Impairments',
        # = Profit before taxes
        'Income tax expense'
        # = Profit from continuing operations
        'Net income from discontinued operations'
        # Profit for the period
        ])