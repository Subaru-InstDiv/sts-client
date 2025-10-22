# STSpy

## Overview
- STSpy is a small Python library for communicating with the Subaru Telescope STS board ("STS radio").
- It provides two core classes:
  - Datum: a lightweight container representing typed values (integer, float, text, integer-with-text, float-with-text, exponent) with an STS radio ID and timestamp.
  - Radio: a client that packs/unpacks STS binary protocol messages and transmits/receives data to/from an STS board over TCP.

## Stack and compatibility
- Language: Python (tested with Python 3). The shebang in tests uses python3.
- Standard library only: socket, struct, time, unittest. No third-party dependencies.
- Packaging: pyproject.toml with setuptools backend is provided for builds and installation.

## Project structure
- STSpy/
  - __init__.py: Exposes Datum and Radio at package level.
  - datum.py: Defines Datum class and factory constructors for each supported data type.
  - radio.py: Defines Radio class and binary packing/unpacking, plus TCP transmit/receive.
- test_STSpy.py: Unittest suite for Datum and Radio. Note: some tests connect to a live STS server.

## Requirements
- Python 3.7+ recommended. The code uses only the standard library and should work on most recent Python 3 versions.
- Network access to an STS board if you intend to run the integration tests or use Radio.transmit/Radio.receive against a live system.

## Installation
- Install from source:
  - python -m pip install .
- Editable/development install:
  - python -m pip install -e .
- Requirements:
  - Python 3.7+; no third-party dependencies beyond the standard library.

## Usage
- Once installed, import as shown below. You can also use the package directly from the source tree if you prefer, by setting PYTHONPATH=. when running examples/tests.

## Quick start examples
### Create Datum values
- from STSpy import Datum
- d1 = Datum.Integer(id=1090, timestamp=0, value=1)
- d2 = Datum.Float(id=1091, timestamp=0, value=3.14)
- d3 = Datum.Text(id=1092, timestamp=0, value='hello')
- d4 = Datum.IntegerWithText(id=1093, timestamp=0, value=(1, 'ok'))
- d5 = Datum.FloatWithText(id=1094, timestamp=0, value=(2.5, 'm/s'))
- d6 = Datum.Exponent(id=1095, timestamp=0, value=1.0)

### Send and receive with Radio
- from STSpy import Radio, Datum
- radio = Radio()  # defaults shown below
- radio.transmit([d1, d2, d3, d4, d5, d6])
- latest = radio.receive([1090, 1091, 1092, 1093, 1094, 1095])
- print(latest)

## Configuration
- Radio defaults (as defined in STSpy/radio.py):
  - HOST: 133.40.160.114
  - PORT: 9001
  - TIMEOUT: 5.0 seconds
- You can override these via the constructor:
  - Radio(host='example.org', port=9001, timeout=2.0)

## Entry points and scripts
- This repository provides a Python package (STSpy) intended to be imported by other code.
- No console scripts or CLI entry points are defined at this time. Usage is via Python imports as shown above.
- Tests can be run as scripts; see the Tests section.

## Tests
- The test suite uses unittest and resides in test_STSpy.py.
- Some tests are pure unit tests (packing/unpacking, factory methods), and others perform live network I/O against the default STS HOST/PORT.
- Running all tests as-is will attempt to connect to 133.40.160.114:9001 and may fail or hang if not reachable.

### Run tests
- Run all tests (may attempt network access):
  - python -m unittest -v
- Run only offline/unit tests (examples):
  - python -m unittest -v test_STSpy.DatumTest
  - python -m unittest -v test_STSpy.RadioTest.test_pack_method_with_invalid_data_type
  - python -m unittest -v test_STSpy.RadioTest.test_unpack_method_with_invalid_packet_size
  - python -m unittest -v test_STSpy.RadioTest.test_unpack_method_with_invalid_data_type
- If you wish to run integration tests that hit the live STS server, ensure network connectivity and that the HOST/PORT are correct or pass custom values when constructing Radio in your own tests.
- TODO: Introduce a test marker or environment flag to skip integration tests by default.

## Development notes
- Coding style: straightforward Python 3 with standard library only.
- Network protocol: The Radio class uses struct to pack/unpack a specific binary protocol header and payload for STS. See radio.py for details.

## Known limitations
- Packaging metadata is provided via pyproject.toml; no setup.cfg/setup.py files are used.
- No CI configuration is present.
- Integration tests depend on external network availability and an accessible STS board.

## License
- Copyright (c) 2018 Subaru Telescope.
- A LICENSE file is not included in the repository.
- TODO: Add an explicit license file (e.g., MIT, BSD-3-Clause, Apache-2.0) or the appropriate Subaru Telescope license text.

## Attribution
- Original copyright notice retained in source files.
