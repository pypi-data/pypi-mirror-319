# winzy-taskloop

[![PyPI](https://img.shields.io/pypi/v/winzy-taskloop.svg)](https://pypi.org/project/winzy-taskloop/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-taskloop?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-taskloop/releases)
[![Tests](https://github.com/sukhbinder/winzy-taskloop/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-taskloop/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-taskloop/blob/main/LICENSE)

Run tasks in loop from cli

## Installation

First [install winzy](https://github.com/sukhbinder/winzy) by typing

```bash
pip install winzy
```

Then install this plugin in the same environment as your Winzy application.
```bash
winzy install winzy-taskloop
```
## Usage

Use this to look task from cli. 

![demo of winzy taskloop](https://raw.githubusercontent.com/sukhbinder/winzy-taskloop/refs/heads/main/demo.gif)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-taskloop
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
