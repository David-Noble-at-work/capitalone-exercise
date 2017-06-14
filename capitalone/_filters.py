# Copyright © David Noble. All Rights Reserved.

from collections import OrderedDict
from datetime import timedelta
from typing import Iterable, Sequence

from ._transaction import Transaction


class TimeWindow(Iterable[Transaction]):

    def __init__(self, predicate, interval: timedelta, transactions: Iterable[Transaction]) -> None:
        self._predicate = predicate
        self._removals = None
        self._interval = interval
        self._transactions = transactions

    def __iter__(self) -> Transaction:
        """ Iterate over the set of transactions that aren't removed based on what `TimeWindow.predicate` returns """

        def removed() -> bool:
            """ Conditionally removes a transaction and its correlated transactions from the current time window

            :return: :const:`True`, if the transaction and its correlated transactions was removed; otherwise
            :const:`False`.

            """
            remove, correlated_transactions = self._predicate(start, window)
            if remove:
                removals.append(start)
                for removal in correlated_transactions:
                    window.pop(removal.amount)
                removals.extend(correlated_transactions)
            return remove

        # Setup

        transactions = self._transactions

        start = next(iter(transactions), None)
        removals = []

        if start is None:  # there are no transactions
            self._removals = removals
            return

        end = next(iter(transactions), None)
        window = OrderedDict()

        if end is None:  # we've got a single transaction--start
            if not removed():
                yield start
            self._removals = removals
            return

        start_time = start.transaction_time
        end_time = end.transaction_time
        more = True

        # Process transaction stream

        while True:

            if more and end_time - start_time < self._interval:

                # Extend the current time window until it covers a full time interval

                window[end.amount] = end
                more = False

                for end in transactions:
                    end_time = end.transaction_time
                    if end_time - start_time > self._interval:
                        more = True
                        break
                    window[end.amount] = end

            if not removed():
                yield start

            try:
                amount, start = window.popitem(last=False)
            except KeyError:
                if not more:
                    break
                start = end

            start_time = start.transaction_time

        self._removals = removals

    @property
    def interval(self) -> timedelta:
        return self._interval

    @property
    def predicate(self):
        return self._predicate

    @property
    def removals(self) -> Sequence[Transaction]:
        return self._removals


time_window = TimeWindow
