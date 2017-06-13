# Copyright © David Noble. All Rights Reserved.

from typing import Any, Mapping


class Transaction(object):

    __slots__ = ('_transaction',)

    def __init__(self, transaction: Mapping[str, Any]) -> None:
        self._transaction = transaction

    def __repr__(self):
        return repr(self._transaction)

    def __str__(self):
        return str(self._transaction)

    @property
    def amount(self):
        return self._transaction['amount']

    @property
    def is_pending(self):
        return self._transaction['is-pending']

    @property
    def aggregation_time(self):
        return self._transaction['aggregation-time']

    @property
    def account_id(self):
        return self._transaction['account-id']

    @property
    def clear_date(self):
        return self._transaction['clear-date']

    @property
    def transaction_id(self):
        return self._transaction['transaction-id']

    @property
    def raw_merchant(self):
        return self._transaction['raw-merchant']

    @property
    def categorization(self):
        return self._transaction['categorization']

    @property
    def merchant(self):
        return self._transaction['merchant']

    @property
    def transaction_time(self):
        return self._transaction['transaction-time']
