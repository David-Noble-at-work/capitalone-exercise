# Copyright © David Noble. All Rights Reserved.

from typing import Sequence
import io
import json
import pytest
from os import path
from subprocess import Popen, PIPE
from sys import executable

capitalone = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'capitalone.py')


@pytest.mark.parametrize(
    'args, expected_filename',
    [
        ([], 'example-1.json'),
        (['--ignore-donuts'], 'example-2.json'),
        (['--ignore-cc-payments'], 'example-3.json'),
        (['--ignore-donuts', '--ignore-cc-payments'], 'example-4.json'),
    ]
)
def test_example(args: Sequence[str], expected_filename: str):

    process = Popen(
        [executable, capitalone, '--email', 'interview@levelmoney.com', '--password', 'password2'] + args,
        stdout=PIPE, stderr=PIPE
    )

    output, errors = process.communicate()

    errors = errors.decode('utf-8')  # no assertions because output depends on the current test runner
    assert process.returncode == 0, f'Expected returncode == 0, not {process.returncode}:\n  {errors}'

    output = output.decode('utf-8')

    with io.open(expected_filename) as istream:
        expected_text = istream.read()

    expected_json = json.loads(expected_text)
    observed_json = json.loads(output)

    assert observed_json == expected_json, f'Expected match to contents of {expected_filename}, not: \n  {output}'
