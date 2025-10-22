# STSpy

## Overview
- STSpy is a small Python library for communicating with the Subaru Telescope STS board ("STS radio").
- It provides two core classes:
  - Datum: a lightweight container representing typed values (integer, float, text, integer-with-text, float-with-text, exponent) with an STS radio ID and timestamp.
  - Radio: a client that packs/unpacks STS binary protocol messages and transmits/receives data to/from an STS board over TCP.

## Stack and compatibility
- Language: Python 3 (requires Python >= 3.12).
- Standard library only: socket, struct, time, unittest. No third-party runtime dependencies.
- Packaging/build: pyproject.toml using setuptools (with setuptools-scm for versioning).

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
  - HOST: 133.40.160.114
  - PORT: 9001
  - TIMEOUT: 5.0 seconds
- You can override these via the constructor:
  - Radio(host='example.org', port=9001, timeout=2.0)

## Entry points and scripts
- This repository provides a Python package intended to be imported by other code.
- No console scripts or CLI entry points are defined at this time. Usage is via Python imports as shown above.

## Tests
- The test suite uses unittest and resides under the tests/ directory.
- Some tests are pure unit tests (packing/unpacking, factory methods), and others perform live network I/O against the default STS HOST/PORT.
- Running all tests as-is may attempt to connect to 133.40.160.114:9001 and may fail or hang if not reachable.

### Run tests
- Run all tests (may attempt network access):
  - python -m unittest -v
- Run only offline/unit tests (examples):
  - python -m unittest -v tests.test_datum.DatumTest
  - python -m unittest -v tests.test_radio.RadioTest.test_pack_method_with_invalid_data_type
  - python -m unittest -v tests.test_radio.RadioTest.test_unpack_method_with_invalid_packet_size
  - python -m unittest -v tests.test_radio.RadioTest.test_unpack_method_with_invalid_data_type
- If you use Hatch, equivalent scripts are defined:
  - hatch run test
  - hatch run test-offline
- If you wish to run integration tests that hit the live STS server, ensure network connectivity and that the HOST/PORT are correct or pass custom values when constructing Radio in your own tests.

## Development notes
- Coding style: straightforward Python 3 with standard library only.
- Network protocol: The Radio class uses struct to pack/unpack a specific binary protocol header and payload for STS. See radio.py for details.

## Known limitations
- Packaging metadata is provided via pyproject.toml; no setup.cfg/setup.py files are used.
- Integration tests depend on external network availability and an accessible STS board.

## License
- Copyright (c) 2018 Subaru Telescope.
- A LICENSE file is not included in the repository.
- TODO: Add an explicit license file (e.g., MIT, BSD-3-Clause, Apache-2.0) or the appropriate Subaru Telescope license text.

## Attribution
- Original copyright notice retained in source files.
