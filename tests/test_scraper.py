import unittest
from unittest.mock import patch
import sys
sys.path.append('../')
from scraper.scraper import Scraper


class ScraperTestcase(unittest.TestCase):

    def test_perform_scrape(self):
        with patch.object(Scraper, 'scrape_items', return_value=None) as mock_scrape_items:
            scrape = Scraper()
            self.url_list = scrape.url_list
            scrape.perform_scrape()
            mock_scrape_items.assert_called()
            self.assertEqual(mock_scrape_items.call_count, len(scrape.url_list))
            urls_used = [args[0] for args in mock_scrape_items.call_args_list]
            self.assertEqual(len(set(urls_used)), len(scrape.url_list))
