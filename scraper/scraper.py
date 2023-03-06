from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import concurrent.futures
import time
import sys
sys.path.append('../scraper')
from initialiser import Initialiser
from items import Items
from saver import Saver


class Scraper:
    '''
    This class acts as the mainframe for the other classes used in the web scraper.
    It calls the Initialiser class to get the list of urls, then uses multithreading to open each url simultaneously.
    In each thread, the Items class is called to retrieve the TV show data, and the Saver class is called to save it locally.

    Parameters:
    ----------
    None


    Attributes:
    ----------
    url_list: list
        List of urls to each TV show page
    item_dict_list: list
        List of populated item dictionaries obtained from the Items class


    Methods:
    -------
    scrape_urls()
        Instantiates the Initialiser class, calls its scrape() method
    scrape_items()
        Creates a chromedriver instance and visit a particular url from the url_list
        Instantiates the Items class and calls its get_items() method
        If a dictionary is returned, calls the save_data() method
        If None is returned, exits the script and the incomplete data is not saved
    save_data()
        Instantiates the Saver class and calls its save() method
        Adds each item dictionary to the item_dict_list
    perform_scrape()
        Calls the scrape_urls() method 
        Uses a thread pool executor to call the scrape_items() method multiple times in parallel, with the items in the url_list as the methods 'url' parameter
        Prints some scraper performance information
    '''

    def __init__(self):
        self.url_list = []
        self.item_dict_list = []

    def scrape_urls(self):
        print('Scraping urls')
        scrape_urls = Initialiser()
        self.url_list = scrape_urls.scrape()
    
    def scrape_items(self, url):
        options = Options()
        options.headless = True
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-notifications')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)
        time.sleep(2)
        items = Items(driver)
        self.item_dict = items.get_items()  
        driver.quit()
        if self.item_dict == None:
            pass
        else:
            self.save_data(self.item_dict)

    def save_data(self, item_dict):
        save = Saver(item_dict)
        save.save()
        self.item_dict_list.append(item_dict)

    def perform_scrape(self):
        Scraper.scrape_urls(self)
        print('Scraping show data')
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.scrape_items, self.url_list)

        print(f'{len(self.url_list)} urls scraped')
        print(f'{len(self.item_dict_list)} items saved')
        print(f'{len(self.url_list) - len(self.item_dict_list)} results omitted')
        print(f'{int((len(self.item_dict_list) / len(self.url_list)) * 100)}% scrape success rate')

if __name__ == '__main__':
    scrape = Scraper()
    scrape.perform_scrape()