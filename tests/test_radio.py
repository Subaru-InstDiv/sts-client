import unittest

import pytest
from subaru.sts.client import Datum, Radio

from .test_datum import DatumTest


class RadioTest(unittest.TestCase):
    """Unit tests for the Radio class."""

    def test_default_constructor(self):
        """Test the default constructor of the Radio class."""

        _ = Radio()

    def test_pack_method_with_invalid_data_type(self):
        """Test the pack static method with an invalid data type."""

        datum = Datum(id=0, format=6)
        with pytest.raises(RuntimeError):
            Radio.pack(datum)

    def test_unpack_method_with_invalid_packet_size(self):
        """Test the unpack static method with an invalid packet size."""

        packet = Radio.pack(Datum.Integer(id=0, timestamp=0, value=0))
        packet[0:1] = bytes([18 | 0x80])
        with pytest.raises(RuntimeError):
            Radio.unpack(packet)

    def test_unpack_method_with_invalid_data_type(self):
        """Test the unpack static method with an invalid data type."""

        packet = Radio.pack(Datum.Integer(id=0, timestamp=0, value=0))
        packet[5:6] = bytes([6])
        with pytest.raises(RuntimeError):
            Radio.unpack(packet)

    def test_round_trip(self):
        """Test if data round-trips through the pack and unpack static methods."""

        data = DatumTest.create_data()
        for datum in data:
            Radio.unpack(Radio.pack(datum))

    def test_transmit_method(self):
        """Test the transmit method by actually sending data to STS."""

        radio = Radio()
        data = DatumTest.create_data()
        radio.transmit(data)

    def test_receive_method(self):
        """Test the receive method by actually retrieving the latest data from STS."""

        radio = Radio()
        ids = DatumTest.create_ids()
        _ = radio.receive(ids)
