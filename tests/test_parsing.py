import unittest
import sys
from unittest.mock import MagicMock
from datetime import datetime, timedelta

# Mock external dependencies that are missing in the environment
mock_modules = ['curl_cffi', 'pandas', 'bs4', 'colorama']
for module_name in mock_modules:
    sys.modules[module_name] = MagicMock()

# Now we can import the functions from paladins
import paladins

class TestParsing(unittest.TestCase):

    def test_parse_stat_value(self):
        # Numeric strings
        self.assertEqual(paladins.parse_stat_value("123"), 123)
        # Thousands separators (commas and dots)
        self.assertEqual(paladins.parse_stat_value("1,234"), 1234)
        self.assertEqual(paladins.parse_stat_value("1.234"), 1234)
        self.assertEqual(paladins.parse_stat_value("1,234,567"), 1234567)
        self.assertEqual(paladins.parse_stat_value("1.234.567"), 1234567)
        # Whitespace
        self.assertEqual(paladins.parse_stat_value("  456  "), 456)
        # Falsy values
        self.assertEqual(paladins.parse_stat_value(""), 0)
        self.assertEqual(paladins.parse_stat_value(None), 0)
        # Non-numeric
        self.assertEqual(paladins.parse_stat_value("abc"), 0)
        self.assertEqual(paladins.parse_stat_value("123a"), 0)
        self.assertEqual(paladins.parse_stat_value("12.3k"), 0)

    def test_extract_player_id_from_href(self):
        # Valid profile hrefs
        self.assertEqual(paladins.extract_player_id_from_href("/profile/12345-Name"), "12345")
        self.assertEqual(paladins.extract_player_id_from_href("/profile/67890-Another-Name"), "67890")
        # Non-profile hrefs
        self.assertEqual(paladins.extract_player_id_from_href("/match/12345"), "")
        self.assertEqual(paladins.extract_player_id_from_href("/other/12345-Name"), "")
        # Falsy values
        self.assertEqual(paladins.extract_player_id_from_href(""), "")
        self.assertEqual(paladins.extract_player_id_from_href(None), "")

    def test_parse_relative_time(self):
        # Valid units
        now = datetime.now()

        res = paladins.parse_relative_time("5 minutes ago")
        self.assertIsInstance(res, datetime)
        # Check if it's within a reasonable range (allow some seconds diff)
        self.assertTrue(now - timedelta(minutes=6) < res < now - timedelta(minutes=4))

        res = paladins.parse_relative_time("2 hours ago")
        self.assertIsInstance(res, datetime)
        self.assertTrue(now - timedelta(hours=3) < res < now - timedelta(hours=1))

        res = paladins.parse_relative_time("1 day ago")
        self.assertIsInstance(res, datetime)
        self.assertTrue(now - timedelta(days=2) < res < now - timedelta(days=0))

        res = paladins.parse_relative_time("1 week ago")
        self.assertIsInstance(res, datetime)
        self.assertTrue(now - timedelta(weeks=2) < res < now - timedelta(weeks=0))

        res = paladins.parse_relative_time("1 month ago")
        self.assertIsInstance(res, datetime)
        self.assertTrue(now - timedelta(days=32) < res < now - timedelta(days=28))

        res = paladins.parse_relative_time("1 year ago")
        self.assertIsInstance(res, datetime)
        self.assertTrue(now - timedelta(days=367) < res < now - timedelta(days=363))

        # Invalid formats
        self.assertIsNone(paladins.parse_relative_time("just now"))
        self.assertIsNone(paladins.parse_relative_time("yesterday"))
        self.assertIsNone(paladins.parse_relative_time(""))
        self.assertIsNone(paladins.parse_relative_time(None))

    def test_extract_info_from_url(self):
        # Valid profile URL
        # Function returns (player_name, player_id)
        name, pid = paladins.extract_info_from_url("https://paladins.guru/profile/123456-PlayerName")
        self.assertEqual(name, "PlayerName")
        self.assertEqual(pid, "123456")

        # URL with query params
        name, pid = paladins.extract_info_from_url("https://paladins.guru/profile/98765-AnotherUser?page=1")
        self.assertEqual(name, "AnotherUser")
        self.assertEqual(pid, "98765")

        # Invalid URL
        name, pid = paladins.extract_info_from_url("https://paladins.guru/other")
        self.assertIsNone(name)
        self.assertIsNone(pid)

        name, pid = paladins.extract_info_from_url("https://google.com")
        self.assertIsNone(name)
        self.assertIsNone(pid)

if __name__ == '__main__':
    unittest.main()
