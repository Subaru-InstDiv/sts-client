# STSpy

[![Offline Tests](https://github.com/Subaru-InstDiv/sts-client/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Subaru-InstDiv/sts-client/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/Subaru-InstDiv/STSpy/branch/main/graph/badge.svg)](https://codecov.io/gh/Subaru-InstDiv/STSpy)

## Overview
- STSpy is a small Python library for communicating with the Subaru Telescope STS board ("STS radio").
- It provides two core classes:
  - Datum: a lightweight container representing typed values (integer, float, text, integer-with-text, float-with-text, exponent) with an STS radio ID and timestamp.
  - Radio: a client that packs/unpacks STS binary protocol messages and transmits/receives data to/from an STS board over TCP.

## Stack and compatibility
- Language: Python 3 (requires Python >= 3.12).
- Standard library only: socket, struct, time, unittest. No third-party runtime dependencies.
- Packaging/build: pyproject.toml using setuptools (with setuptools-scm for versioning).
- Development tools: ruff (formatter and linter), pytest (testing), hatch (environment management).

## Project structure
- src/
  - subaru/
    - sts/
      - __init__.py
      - client/
        - __init__.py  (exposes Datum and Radio)
        - datum.py     (Datum class and factory constructors)
        - radio.py     (Radio class and binary packing/unpacking, TCP transmit/receive)
- tests/
  - test_datum.py      (unit tests for Datum)
  - test_radio.py      (unit and integration tests for Radio; some perform live network I/O)

## Requirements
- Python 3.12+.
- Network access to an STS board if you intend to run the integration tests or use Radio.transmit/Radio.receive against a live system.

## Installation
- Install from source (in this repository's root):
  - python -m pip install .
- Editable/development install:
  - python -m pip install -e .
- Development install with dev tools:
  - python -m pip install -e ".[dev]"
- Package name (when published): `subaru-sts-client`.

## Usage
- Once installed, import as shown below. You can also use the package directly from the source tree by running Python from the repository root (src/ layout is discovered automatically by setuptools-installed packages).

## Quick start examples
### Create Datum values
- from subaru.sts.client import Datum
- d1 = Datum.Integer(id=1090, timestamp=0, value=1)
- d2 = Datum.Float(id=1091, timestamp=0, value=3.14)
- d3 = Datum.Text(id=1092, timestamp=0, value='hello')
- d4 = Datum.IntegerWithText(id=1093, timestamp=0, value=(1, 'ok'))
- d5 = Datum.FloatWithText(id=1094, timestamp=0, value=(2.5, 'm/s'))
- d6 = Datum.Exponent(id=1095, timestamp=0, value=1.0)

### Send and receive with Radio
- from subaru.sts.client import Radio, Datum
- radio = Radio()  # defaults shown below
- radio.transmit([d1, d2, d3, d4, d5, d6])
- latest = radio.receive([1090, 1091, 1092, 1093, 1094, 1095])
- print(latest)

## Configuration
- Radio defaults (as defined in src/subaru/sts/client/radio.py):
  - HOST: sts
  - PORT: 9001
  - TIMEOUT: 5.0 seconds
- You can override these via the constructor:
  - Radio(host='example.org', port=9001, timeout=2.0)

## Tests
- Some tests are pure unit tests (packing/unpacking, factory methods), and others perform live network I/O against the default STS HOST/PORT.
- Running all tests as-is may attempt to connect to sts:9001 and may fail or hang if not reachable.

### Run tests
- Run all tests (may attempt network access):
  - pytest -v
  - or: python -m pytest -v
- Run only offline/unit tests (examples):
  - pytest -v -k 'not transmit_method and not receive_method'
- If you use Hatch, equivalent scripts are defined:
  - hatch run test
  - hatch run test-offline

### Code quality and formatting
- This project uses ruff for both linting and code formatting.
- Ruff configuration is defined in pyproject.toml and follows:
  - Line length: 100 characters
  - Target: Python 3.12
  - Docstring convention: numpy

#### Hatch commands for code quality:
- Format code:
  - hatch run format
- Check formatting without changes:
  - hatch run format-check
- Lint code:
  - hatch run lint
- Lint and auto-fix issues:
  - hatch run lint-fix
- Run all quality checks (lint + format check):
  - hatch run check

#### Manual ruff commands (if not using Hatch):
- Format code:
  - ruff format .
- Check formatting:
  - ruff format --check .
- Lint code:
  - ruff check .
- Lint and auto-fix:
  - ruff check --fix .

- If you wish to run integration tests that hit the live STS server, ensure network connectivity and that the HOST/PORT are correct or pass custom values when constructing Radio in your own tests.

## Development notes
- Network protocol: The Radio class uses struct to pack/unpack a specific binary protocol header and payload for STS. See radio.py for details.

## Known limitations
- Integration tests depend on external network availability and an accessible STS board.
