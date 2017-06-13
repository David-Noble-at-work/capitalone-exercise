# Copyright © David Noble. All Rights Reserved.

from typing import Any, Dict, Sequence, Tuple
from datetime import datetime
from ._income_and_expense import IncomeAndExpense
from ._transaction import Transaction


class TransactionCollection(Sequence[Transaction]):

    __slots__ = ('_transactions',)

    def __init__(self, transactions: Sequence[Any]) -> None:
        self._transactions = transactions

    def __getitem__(self, i: int) -> Transaction:
        return Transaction(self._transactions[i])

    def __len__(self) -> int:
        return len(self._transactions)

    def compute_income_and_expenses(self):

        start = (datetime.max.year, datetime.max.month)
        end = (datetime.min.year, datetime.min.month)
        total = IncomeAndExpense(spent=0, income=0)
        table: Dict[Tuple[int, int]] = {}

        for transaction in self:

            transaction_time = datetime.strptime(transaction.transaction_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            period = (transaction_time.year, transaction_time.month)
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

        report = {
            f'{format(period[0], "04")}-{format(period[1], "02")}': table[period].as_dict() for period in sorted(table)
        }

        months = 12 * (end[0] - start[0]) + (start[1] - end[1])
        report['average'] = IncomeAndExpense(spent=total.spent // months, income=total.income // months).as_dict()

        return report
