# Copyright © David Noble. All Rights Reserved.

from typing import Any, Dict, Sequence

from ._transaction import Transaction


class TransactionCollection(Sequence[Transaction]):

    __slots__ = ('_transactions', '_underlying')

    def __init__(self, transactions: Sequence[Any]) -> None:
        self._transactions = [Transaction(underlying_transaction) for underlying_transaction in transactions]
        self._underlying = transactions

    def __getitem__(self, i: int) -> Transaction:
        return self._transactions[i]

    def __len__(self) -> int:
        return len(self._transactions)

    def to_json(self) -> Sequence[Dict[str, Any]]:
        return self._underlying
