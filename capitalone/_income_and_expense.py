# Copyright © David Noble. All Rights Reserved.

from collections import namedtuple
from decimal import Decimal


class IncomeAndExpense(namedtuple('IncomeAndExpense', ('spent', 'income'))):

    def as_dict(self):
        return {'spent': f'${Decimal(-self.spent // 100) / 100}', 'income': f'${Decimal(self.income // 100) / 100}'}
