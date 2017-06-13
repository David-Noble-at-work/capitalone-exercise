# Copyright © David Noble. All Rights Reserved.

from enum import Enum


class DemoAccountType(Enum):
    default = 'default'
    autosave_enabled = 'autosave-enabled'
    no_savings_account = 'no-savings-account'
    overspent = 'overspent'
