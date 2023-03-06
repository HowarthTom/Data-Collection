import unittest
import random
import sys
sys.path.append('../')
from scraper.initialiser import Initialiser


class InitialiserTestcase(unittest.TestCase):

    def setUp(self):
        initialiser = Initialiser()
        self.url_list = initialiser.scrape()
        random_index = random.randint(0, 150)
        self.test_url = self.url_list[random_index]

    def test_scrape(self):
        self.assertEqual(len(self.url_list), 150)
        self.assertIn('https://www.rottentomatoes.com/tv/', self.test_url)
