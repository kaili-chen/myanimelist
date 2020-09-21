import unittest
import utility
from utility import MalUrlError

class TestIsMalUrl(unittest.TestCase):

    def test_plain(self):
        self.assertTrue(utility.is_mal_url('https://myanimelist.net'))
        self.assertFalse(utility.is_mal_url('animelist.net'))

    def test_invalid_type(self):
        with self.assertRaises(MalUrlError):
            utility.is_mal_url('https://myanimelist.net', check_type="Not")

if __name__ == '__main__':
    unittest.main()
