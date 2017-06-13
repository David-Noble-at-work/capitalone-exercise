#!/usr/bin/env python36

# Capital One Programming Exercise
#
# Copyright 2017 David Noble
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#

# This code was developed and tested under Python 3.6 on macOS Sierra. Please ask for Python 2.7 code or code that will
# run under Python 2.7 or Python 3.6, if you would prefer it.
#
# mypy 0.511 clean

from typing import Iterator, Mapping, Optional, Tuple

import json
from argparse import ArgumentParser
from datetime import timedelta

import capitalone
from capitalone import Transaction


def argument_parser() -> ArgumentParser:

    parser = ArgumentParser(
        description='',
        fromfile_prefix_chars='@'
    )

    parser.add_argument('--email', metavar='<email-address>', required=True)
    parser.add_argument('--password', metavar='<password>', required=True)
    parser.add_argument('--crystal-ball', action='store_true')
    parser.add_argument('--ignore-cc-payments', action='store_true')
    parser.add_argument('--ignore-donuts', action='store_true')

    return parser


if __name__ == '__main__':

    import sys

    arguments = argument_parser().parse_args(sys.argv[1:])

    account = capitalone.Account()
    account.login(arguments.email, arguments.password)

    transactions = account.get_all_transactions()

    # Strategy: Construct a processing pipeline composed of filters over a sequence of transactions and then--at the
    # end--report on them. In production code we'd formalize the concept of a processing pipeline which could execute
    # a variety of commands, including--for example--aggregating, filtering, and transforming commands.

    if arguments.ignore_donuts:

        # Simple filter: examine each record and include all those outside the category of donuts
        # One might modify this filter to exclude just payments to donut shops. We've chosen not to for this
        # exercise. We note that the test account includes no payments from Krispy Kreme Donuts or DUNKIN #336784.

        def ignore(transaction: Transaction):
            return transaction.merchant not in ['Krispy Kreme Donuts', 'DUNKIN #336784']

        transactions = filter(ignore, transactions)

    if arguments.ignore_cc_payments:

        # Filter on the transactions in a 24-hour time window: Our strategy is to provide a filter over the transactions
        # in a 24-hour time window. The time_window class constructs an iterator that enables a predicate function to
        # selectively include transactions in the time window. In this exercise transactions are keyed by amount. In a
        # generalized solution we'd offer up the ability to specify a key or--perhaps--set of keys when constructing
        # a time window. Note that in this limited implementation one could still examine any or all transaction fields,
        # just not with the benefit of keyed access.

        def ignore(transaction: Transaction, window: Mapping[int, Transaction]) -> Tuple[bool, Optional[Iterator[Transaction]]]:
            try:
                correlated = window[-transaction.amount]
            except KeyError:
                return False, None
            return True, (correlated,)

        transactions = capitalone.time_window(ignore, timedelta(hours=24), transactions)

    report = capitalone.compute_income_and_expenses(transactions)

    if arguments.ignore_cc_payments:
        report = {
            'income-and-expenses': report,
            'cc-payments': [removal.to_dict() for removal in transactions.removals]
        }

    json.dump(report, sys.stdout, indent=2)
