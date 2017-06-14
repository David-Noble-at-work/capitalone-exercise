# Copyright © David Noble. All Rights Reserved.

from typing import Dict, Iterator, Mapping, Tuple
from datetime import datetime

from ._income_and_expense import IncomeAndExpense
from ._transaction import Transaction


def compute_income_and_expenses(transactions: Iterator[Transaction]) -> Mapping[str, Mapping[str, str]]:
    """ Computes income and expenses by month for the current transaction iterator

    Missing months are not represented, but are factored into the average for the period of time covered by the
    current transaction collection. For example, if the period starts in January of one year and ends in December
    of the following year, the period covers 24 months. 24 is  used as the denominator for the average for this
    two year period even when months are missing. This might happen for example when a customer decides not to use
    their account in some months.

    :return: Monthly income and expense items including an `"average"` over the full period. Income and expense
    items are ordered and keyed by date strings of the form `'YYYY-DD'`. Income and expense items are represented
    as mappings of the form `{"spent": "$<dollars>.<cents>", "income": "$<dollars>.<cents>"}`.

    Example

    """

    start = (datetime.max.year, datetime.max.month)
    end = (datetime.min.year, datetime.min.month)
    total = IncomeAndExpense(spent=0, income=0)
    table: Dict[Tuple[int, int]] = {}

    for transaction in transactions:

        period = (transaction.transaction_time.year, transaction.transaction_time.month)
        amount = transaction.amount

        try:
            value = table[period]
        except KeyError:
            value = IncomeAndExpense(spent=0, income=0)

        if amount >= 0:
            value = IncomeAndExpense(spent=value.spent, income=value.income + amount)
            total = IncomeAndExpense(spent=total.spent, income=total.income + amount)
        else:
            value = IncomeAndExpense(spent=value.spent + amount, income=value.income)
            total = IncomeAndExpense(spent=total.spent + amount, income=total.income)

        table[period] = value

        if period < start:
            start = period
        elif period > end:
            end = period

    report = {f'{format(period[0], "04")}-{format(period[1], "02")}': table[period].to_dict() for period in table}
    months = 12 * (end[0] - start[0]) + (start[1] - end[1])
    report['average'] = IncomeAndExpense(spent=total.spent // months, income=total.income // months).to_dict()

    return report
