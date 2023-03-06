import unittest 
from test_initialiser import InitialiserTestcase
from test_items import ItemsTestcase
from test_saver import SaverTestcase
from test_scraper import ScraperTestcase

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(InitialiserTestcase))
suite.addTests(loader.loadTestsFromTestCase(ItemsTestcase))
suite.addTests(loader.loadTestsFromTestCase(SaverTestcase))
suite.addTests(loader.loadTestsFromTestCase(ScraperTestcase))

runner = unittest.TextTestRunner()
result = runner.run(suite)