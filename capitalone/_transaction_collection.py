# Copyright © David Noble. All Rights Reserved.

<<<<<<< HEAD
from typing import Any, Dict, Sequence
=======
from typing import Any, Dict, List, Sequence
>>>>>>> 6c3feab59e6eb9ceaec689d22edb32df2b037cc6

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
<<<<<<< HEAD
        return self._underlying
=======
        return self._transactions
>>>>>>> 6c3feab59e6eb9ceaec689d22edb32df2b037cc6
