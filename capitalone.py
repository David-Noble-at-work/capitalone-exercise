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

from argparse import ArgumentParser
import capitalone
import json


def argument_parser() -> ArgumentParser:

    parser = ArgumentParser(
        description='',
        fromfile_prefix_chars='@'
    )

    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)

    return parser


if __name__ == '__main__':

    import sys

    arguments = argument_parser().parse_args(sys.argv[1:])

    account = capitalone.Account()
    account.login(arguments.email, arguments.password)

    transactions = account.get_all_transactions()
    report = transactions.compute_income_and_expenses()

    json.dump(report, sys.stdout, indent=2)
