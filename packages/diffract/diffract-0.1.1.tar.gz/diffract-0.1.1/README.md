# diffract

[![PyPI version](https://badge.fury.io/py/diffract.svg)](https://badge.fury.io/py/diffract)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
<!-- [![Build Status](https://github.com/<your-username>/diffract/actions/workflows/ci.yaml/badge.svg)](https://github.com/<your-username>/diffract/actions) -->

A CLI tool and library to diff the source of Python objects specified by dotted paths.


## Installation

You can install `diffract` from PyPi:

```bash
pip install diffract
```

The output will be colorized if [`rich`](https://pypi.org/project/rich/) is installed.
This can be installed at the same time:

```bash
pip install "diffract[color]"
```

or separately:

```bash
pip install rich
```


## Usage

```bash
diffract package_a.module_a.function_a package_b.module_b.function_b
```


## License

This project is licensed under the MIT License. See the LICENSE file for details.
