# Copyright © David Noble. All Rights Reserved.

from typing import Any, Dict, List, Sequence

from ._transaction import Transaction


class TransactionCollection(Sequence[Transaction]):

    __slots__ = ('_transactions',)

    def __init__(self, transactions: Sequence[Any]) -> None:
        self._transactions = transactions

    def __getitem__(self, i: int) -> Transaction:
        return Transaction(self._transactions[i])

    def __len__(self) -> int:
        return len(self._transactions)

    def to_json(self) -> Sequence[Dict[str, Any]]:
        return self._transactions
