# Copyright © David Noble. All Rights Reserved.

from typing import Any, Dict, Mapping, Optional

import json
from copy import deepcopy
from requests import HTTPError, post

from ._demo_account_type import DemoAccountType
from ._transaction_collection import TransactionCollection


class Account(object):

    def __init__(self, demo_account_type: Optional[DemoAccountType]=None) -> None:

        self._endpoints = {}
        self._uid: str = None
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
        self._uid = message['uid']
        self._token = message['token']

    def get_all_transactions(self) -> TransactionCollection:

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
        return TransactionCollection(message['transactions'])

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
