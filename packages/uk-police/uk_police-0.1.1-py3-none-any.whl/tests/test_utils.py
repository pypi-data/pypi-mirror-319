import unittest
from Pyolice.utils import validate_lat_lng, validate_polygon

class TestUtils(unittest.TestCase):
    def test_validate_lat_lng(self):
        self.assertIsNone(validate_lat_lng(51.5074, -0.1278))  # Valid values

    def test_validate_polygon(self):
        self.assertIsNone(validate_polygon("51.5,-0.1:51.5,-0.2"))  # Valid polygon