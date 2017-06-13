# capitalone-exercise

This module and its command line interface was developed and tested under [Python](https://goo.gl/WxZLS2) 3.6 on macOS
Sierra and is [mypy](https://goo.gl/Un5F1A) 0.511 clean. The command line interface is self documenting. Assuming that
the Python 3.6 interpreter is on your path, run this command from the capitalone-exercise directory to get help:

```bash
python capitalone.py --help
```

Execute this command to run the capitalone tests:

```bash
python -m pytest test
```
## Requirements

This module requires Python 3.6 and these packages:
 
1. [pytest](https://goo.gl/9Jhu8G)
2. [requests](http://docs.python-requests.org/en/master/)

## Setup instructions

The setup instructions depend on your platform and its package manager.

### On Debian 8.8

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
