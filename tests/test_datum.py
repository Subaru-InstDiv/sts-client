import time
import unittest

from subaru.sts.client import Datum


class DatumTest(unittest.TestCase):
    """Unit tests for the Datum class."""

    @staticmethod
    def create_data():
        """Create a list of STS data that can be written to STS for testing."""

        # Long text data (62*3 bytes)
        text = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' * 3
        timestamp = int(time.time())
        return [
            Datum.Integer(id=1090, timestamp=timestamp, value=1),
            Datum.Float(id=1091, timestamp=timestamp, value=1.0),
            Datum.Text(id=1092, timestamp=timestamp, value=text),
            Datum.IntegerWithText(id=1093, timestamp=timestamp, value=(1, text)),
            Datum.FloatWithText(id=1094, timestamp=timestamp, value=(1.0, text)),
            Datum.Exponent(id=1095, timestamp=timestamp, value=1.0),
        ]

    @staticmethod
    def create_ids():
        """Create a list of STS radio IDs that can be read from STS for testing."""

        return [1090, 1091, 1092, 1093, 1094, 1095]

    def test_default_constructor(self):
        """Test the default constructor of the Datum class."""

        _ = Datum()

    def test_factory_methods(self):
        """Test the factory class methods of the Datum class."""

        _ = DatumTest.create_data()
