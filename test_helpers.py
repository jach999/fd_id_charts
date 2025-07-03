import unittest
from helpers import SetBarsWithAndSize

class TestSetBarsWithAndSize(unittest.TestCase):

    def test_less_than_90(self):
        figwidth, fontsize = SetBarsWithAndSize(89)
        self.assertEqual(figwidth, 18, 'The figwidth is wrong. It has to be 18')
        self.assertEqual(fontsize, 12, 'The figwidth is wrong. It has to be 12')

    def test_equal_90(self):
        figwidth, fontsize = SetBarsWithAndSize(90)
        self.assertEqual(figwidth, 18, 'The figwidth is wrong. It has to be 18')
        self.assertEqual(fontsize, 12, 'The figwidth is wrong. It has to be 12')

    def test_90_between_130(self):
        figwidth, fontsize = SetBarsWithAndSize(100)
        self.assertEqual(figwidth, 20, 'The figwidth is wrong. It has to be 20')
        self.assertEqual(fontsize, 10.8, 'The figwidth is wrong. It has to be 10.8')

if __name__ == '__main__':
    unittest.main()