# Economic agent-based models with financial accounting

abcFinance (short for 'agent-based computational Finance') provides tools for using standard double-entry bookkeeping methods either directly or within an agent-based modelling framework. It is a sister library to the [abcEconomics](https://github.com/AB-CE/abce) (agent-based computational Economics) library.

## Direct use of double-entry bookkeeping tools
The class `Ledger` implements an accounting system. Booking statements are recorded through the `book()` method. The basic syntax works as follows:

    accountingsystem = Ledger()
    accountingsystem.make_stock_accounts('Assets', 'Liabilities')
    accountingsystem.book(debit=[('Assets',100)], credit=[('Liabilities',100)]

where `debit` and `credit` are lists of tuples `('account', amount)` of accounts that should be booked by `amount` on the debit and credit side, respectively. The total sum of debits and credits in one booking statement needs to be equal in one booking statement. Accounts have to be declared as either stock or flow accounts before they can be booked. 

A profit and loss statement can be viewed using the `print_profit_and_loss()` statement. The profit or loss for the period can be booked against equity using the `book_end_of_period()` method. The balance sheet can be printed using the `print_balance_sheet()` method. `draw_balance_sheet()` returns the string representation of an SVG image of the balance sheet. Several other helpful methods are available.

Extensive examples can be found in the `examples\money_creation` folder.

## Use in an agent-based modelling system

The `Ledger` class can be used as an attribute for an `Agent` class in an agent-based modelling system, enabling the use of financial accounting within agent-based models. One implementation is provided in the form of the `AbcFinanceAgent` class, which inherits from the `Agent` class in the [abcEconomics](https://github.com/AB-CE/abce) library. abcEconomics is designed to be compatible with abcFinance and provides several methods to facilitate the use of abcFinance methods in agent-based models. The accounting system provided in abcFinance can in principle be used with any agent-based modelling system.