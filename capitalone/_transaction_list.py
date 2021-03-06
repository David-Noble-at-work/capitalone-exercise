# Copyright © David Noble. All Rights Reserved.

from typing import Dict, Sequence, Union

from ._transaction import Transaction


class TransactionList(Sequence[Transaction]):

    __slots__ = ('_transactions', '_underlying')

    def __init__(self, transactions: Sequence[Dict[str, Union[bool, int, str]]]) -> None:
        self._transactions = [Transaction(underlying_transaction) for underlying_transaction in transactions]
        self._underlying = transactions

    def __getitem__(self, index: int) -> Transaction:  # type: ignore
        return self._transactions[index]

    def __len__(self) -> int:
        return len(self._transactions)

    def to_json(self) -> Sequence[Dict[str, Union[bool, int, str]]]:
        return self._underlying
