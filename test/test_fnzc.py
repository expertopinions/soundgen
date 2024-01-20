import unittest
from context import soundgen
from soundgen import *

class TestFindNearestZeroCrossing(unittest.TestCase):
    def setUp(self) -> None:
        self.a = np.full(1000, 1)
        self.a[[87, 173, 211, 304, 468, 823, 900, 902]] = 0
        self.a[[143, 257, 366, 411, 640, 781, 901, 951]] = -1
    
    def test100(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 100), 87)
    
    def test200(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 200), 211)
    
    def test250(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 250), 256)
    
    def test300(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 300), 304)
    
    def test400(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 400), 410)
    
    def test500(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 500), 468)
    
    def test600(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 600), 639)
    
    def test700(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 700), 640)
    
    def test800(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 800), 781)
    
    def test900(self):
        self.assertEqual(find_nearest_zero_crossing(self.a, 900), 900)

    def test901(self):
        # returns lower of the two nearest zero crossings
        self.assertEqual(find_nearest_zero_crossing(self.a, 901), 900)
        
if __name__ == '__main__':
    unittest.main()