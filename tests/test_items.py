import unittest
from selenium import webdriver
import random
import sys
sys.path.append('../')
from scraper.initialiser import Initialiser
from scraper.items import Items


class ItemsTestcase(unittest.TestCase):

    def setUp(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--window-size=1920,1080')
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)
        initialiser = Initialiser()
        self.url_list = initialiser.scrape()
        random_index = random.randint(0, 150)
        self.test_url = self.url_list[random_index]
        driver.get(self.test_url)
        items = Items(driver)
        self.item_dict = items.get_items()

    def test_get_items(self):
        if self.item_dict != None:
            self.item_dict_values = self.item_dict.values()
            self.assertNotIn('N/A', self.item_dict_values)

