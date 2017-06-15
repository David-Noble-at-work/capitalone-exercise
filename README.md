# capitalone-exercise

The `capitalone` package and its command line interface `capitalone.py` were developed and tested under 
[Python](https://goo.gl/WxZLS2) 3.6 on macOS Sierra. The source is [mypy](https://goo.gl/Un5F1A) 0.511 clean.

The command line interface is self documenting. Assuming that the Python 3.6 interpreter is on your path, run this 
command from the `capitalone-exercise` directory to get help:

```bash
python3.6 capitalone.py --help
```

Tests that run each of the examples in the next section are provided. The tests run against live data. Time to write 
mocks (see, for example [`requests-mock`](https://pypi.python.org/pypi/requests-mock)) against a stable source of
transactions. We did check in such a such a source: `tests/Transactions.json` but do not use it.

Given the nature of this exercise it is worth noting that income and expense averages are computed using Python's
[decimal package](https://docs.python.org/2/library/decimal.html) and its default context:

```
>>> from decimal import *
>>> getcontext()
Context(
    prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0, flags=[], traps=[
        InvalidOperation, DivisionByZero, Overflow
    ]
)
```

Results were checked against the numbers produced by Microsoft Excel for Mac version 15.33 and we saw some differences
in the second decimal place on averages. If we were to take this exercise one more step we might reconcile those
differences taking Capital One's rounding rules into account.

Issue these commands to run tests against live data:

```bash
cd tests && python3.6 -m pytest .
```

## Examples

**Example 1:**

Produce unfiltered income and expense report.

```bash
python3.6 capitalone.py --email interview@levelmoney.com --password password2
```

*Output:* 

A single JSON document of income and expenses as documented in `Coding-exercise-instructions.md`.

**Example 2:**

Produce income and expense report that excludes expenses (or--theoretically--income earned) on donuts.

```bash
python3.6 capitalone.py --email interview@levelmoney.com --password password2 --ignore-donuts
```

*Output:* 

A single JSON document of income and expenses as documented in `Coding-exercise-instructions.md`.

**Example 3:**

Produce income and expense report that excludes credit card payments.

```bash
python3.6 capitalone.py --email interview@levelmoney.com --password password2 --ignore-cc-payments
```
*Output:* 

A single JSON document with two fields: `income-and-expenses` and `cc-payments`. The `income-and-expenses` field
is formatted as documented in `Coding-exercise-instructions.md`. The `cc-payments` field lists all credit card
transactions that were ignored.

**Example 4:**

Produce income and expense report that excludes credit card payments and donut expenses.

```bash
python3.6 capitalone.py --email interview@levelmoney.com --password password2 --ignore-cc-payments --ignore-donuts
```

*Output:* 

A single JSON document with two fields: `income-and-expenses` and `cc-payments`. The `income-and-expenses` field
is formatted as documented in `Coding-exercise-instructions.md`. The `cc-payments` field lists all credit card
transactions that were ignored.

## Requirements

The `capitalone` package requires Python 3.6 and these packages:
 
1. [pytest](https://goo.gl/9Jhu8G)
2. [requests](http://docs.python-requests.org/en/master/)

Setup instructions are provided for Debian (not verified).  

## Setup instructions

The setup instructions depend on your platform and its package manager.

### On Debian 3.16

**TODO:** Test these instructions. (We leave this for another day.)

```bash
sudo apt update
sudo apt install python3.6
sudo python3.6 -m ensurepip
sudo python3.6 -m pip install pytest requests
```

### On Fedora 25

```bash
sudo dnf install python3.6
sudo python3.6 -m ensurepip
sudo python3.6 -m pip install pytest requests
```

### On macOS Sierra

If you are using homebrew as your package manager, execute these commands:

```bash
sudo brew update
sudo brew install python36
sudo python3.6 -m ensurepip
sudo python3.6 -m pip install pytest requests
```

Please note that David Noble is a Mac Ports user. Please accept the homebrew instructions as an approximation.

If you are using Mac Ports as your package manager, execute these commands:

```bash
sudo port selfupdate
sudo port install python36
sudo python3.6 -m ensurepip
sudo python3.6 -m pip install pytest requests
```

### On Windows 10

Download and install Python 3.6 from [https://www.python.org/downloads/windows/], ensure that Python 3.6 is on 
your path and then execute this command from an elevated command line window:

```cmd
python3.6 -m pip install pytest requests
```
