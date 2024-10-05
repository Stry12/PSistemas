import unittest
import distance_unary_pb2 as pb2
from geo_location import Position

class TestDistanceService(unittest.TestCase):

    def setUp(self):
        self.post = Position

    def test_value_error_in_position(self):

        with self.assertRaises(ValueError):
            self.post(100,71,0)

if __name__ == '__main__':
    unittest.main()
