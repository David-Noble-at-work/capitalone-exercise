# Copyright © David Noble. All Rights Reserved.

from typing import Any, Dict, Mapping, Optional, Tuple, Union, cast

import json
from copy import deepcopy
from enum import Enum

from requests import HTTPError, post

from ._transaction_list import TransactionList


class DemoAccountType(Enum):
    default = 'default'
    autosave_enabled = 'autosave-enabled'
    no_savings_account = 'no-savings-account'
    overspent = 'overspent'


class Account(object):
    def __init__(self, demo_account_type: Optional[DemoAccountType] = None) -> None:

        self._endpoints: Dict[str, Tuple[str, Dict[str, Any]]] = {}
        self._uid: int = None
        self._token: str = None
        self._demo_account_type: Optional[DemoAccountType] = demo_account_type

    def login(self, email: str, password: str) -> None:

        try:
            endpoint, parameters = self._endpoints['login']
        except KeyError:
            self._endpoints['login'] = endpoint, parameters = (
                f'{Account.url}login', {
                    'email': None,
                    'password': None,
                    'args': {
                        'api-token': Account.api_token,
                    },
                    'demo-account-type': self._demo_account_type
                }
            )

        message = self._post(endpoint, parameters, email=email, password=password)
        self._uid = cast(int, message['uid'])
        self._token = cast(str, message['token'])

    def get_all_transactions(self) -> TransactionList:

        assert self._uid and self._token

        try:
            endpoint, parameters = self._endpoints['get_all_transactions']
        except KeyError:
            self._endpoints['login'] = endpoint, parameters = (
                f'{Account.url}get-all-transactions', {
                    'args': {
                        'api-token': Account.api_token,
                        'uid': self._uid,
                        'token': self._token
                    },
                    'demo-account-type': self._demo_account_type
                }
            )

        message = self._post(endpoint, parameters)
        return TransactionList(message['transactions'])

    @staticmethod
    def _post(endpoint: str, parameters: Dict[str, Any], **kwargs) -> Mapping[str, Any]:

        parameters = deepcopy(parameters)

        for name, value in kwargs.items():
            parameters[name] = value

        response = post(endpoint, json=parameters)

        if not response.ok:
            raise HTTPError(response=response)

        message = json.loads(response.text)

        if message['error'] != 'no-error':
            raise HTTPError(response=response)

        return message

    url = 'https://2016.api.levelmoney.com/api/v2/core/'
    api_token = 'AppTokenForInterview'
