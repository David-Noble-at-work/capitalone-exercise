# Copyright © David Noble. All Rights Reserved.

from typing import Any, Mapping, Union, cast
from datetime import datetime


class Transaction(object):

    __slots__ = ('_transaction', '_transaction_time')

    def __init__(self, transaction: Mapping[str, Union[bool, int, str]]) -> None:
        self._transaction = transaction
        self._transaction_time: datetime = None

    def __repr__(self) -> str:
        return repr(self._transaction)

    def __str__(self) -> str:
        return str(self._transaction)

    # region Properties

    @property
    def amount(self) -> int:
        return cast(int, self._transaction['amount'])

    @property
    def is_pending(self) -> bool:
        return cast(bool, self._transaction['is-pending'])

    @property
    def aggregation_time(self) -> int:
        return cast(int, self._transaction['aggregation-time'])

    @property
    def account_id(self) -> str:
        return cast(str, self._transaction['account-id'])

    @property
    def clear_date(self) -> int:
        return cast(int, self._transaction['clear-date'])

    @property
    def transaction_id(self) -> str:
        return cast(str, self._transaction['transaction-id'])

    @property
    def raw_merchant(self) -> str:
        return cast(str, self._transaction['raw-merchant'])

    @property
    def categorization(self) -> str:
        return cast(str, self._transaction['categorization'])

    @property
    def merchant(self) -> str:
        return cast(str, self._transaction['merchant'])

    @property
    def transaction_time(self) -> datetime:
        value = self._transaction_time
        if value is None:
            value = self._transaction_time = datetime.strptime(
                cast(str, self._transaction['transaction-time']), '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        return value

    # endregion

    # region Methods

    def as_mapping(self) -> Mapping[str, Union[bool, int, str]]:
        return self._transaction

    # endregion
    pass