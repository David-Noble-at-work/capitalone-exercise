# Copyright © David Noble. All Rights Reserved.

from typing import Mapping
from collections import namedtuple
from decimal import Decimal


class IncomeAndExpense(namedtuple('IncomeAndExpense', ('spent', 'income'))):

    # noinspection PyMethodMayBeStatic
    def to_json(self) -> Mapping[str, str]:
        """ Converts an income and expense item to a dictionary for serialization as a JSON object

        This method also converts the income and expense values from centicents to dollar amounts represented as
        strings.

        """
        return {
            'spent': f'${format(Decimal(-self.spent // 100) / 100, ".2f")}',
            'income': f'${format(Decimal(self.income // 100) / 100, ".2f")}'
        }
