#!/usr/bin/env python36

""" Capital One Programming Exercise

Written by David Noble <david@thenobles.us>.

This module was developed and tested under Python 3.6 on macOS Sierra. Please ask for Python 2.7 code or code that
will run under Python 2.7 or Python 3.6, if you would prefer it.

mypy 0.511 clean

"""
from argparse import ArgumentParser


def argument_parser() -> ArgumentParser:

    parser = ArgumentParser(
        description='',
        fromfile_prefix_chars='@'
    )

    return parser


if __name__ == '__main__':
    import sys
    arguments = argument_parser().parse_args(sys.argv[1:])
