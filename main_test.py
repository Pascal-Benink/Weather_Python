import unittest

from main import meme


class TestUtilityFunctions(unittest.TestCase):
    def test_meme_function(self):
        self.assertTrue(meme(9, 10) == 21)
        self.assertFalse(meme(9, 10) == 19)


if __name__ == '__main__':
    unittest.main()
