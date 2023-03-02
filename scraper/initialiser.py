from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Initialiser:
    '''
    This class scrapes the "TV SHOWS" page on the rotten tomatoes website and retrieves url links for each show


    Parameters:
    ----------
    url: str
        url for the "TV SHOWS" page on the rotten tomatoes website


    Attributes:
    ----------
    number_of_pages_to_scrape: int
        Number of pages of results loaded on the "TV SHOWS" page

    url_list: list
        List of urls to each TV show page

    Methods:
    -------
    open_url()
        Opens the "TV SHOWS" page on the rotten tomatoes website 
    accept_cookies()
        Accepts the cookies pop-up
    load_pages()
        Loads the desired amount of results by clicking the "Load More" button
    get_urls()
        Locates each TV show, gets the href link to it's rotten tomatoes page, and stores it in the url_list
    scrape()
        Calls the other methods and returns the populated href_list
    '''

    def __init__(self, number_of_pages_to_scrape=4):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.number_of_pages_to_scrape = number_of_pages_to_scrape
        self.url_list = []

    def open_url(self):
        self.driver.get('https://www.rottentomatoes.com/browse/tv_series_browse/sort:popular')
        time.sleep(2)

    def accept_cookies(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
            time.sleep(2)
        except:
            pass
            
    def load_pages(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Load more")]')))
        button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Load more")]')
        button.click()
        time.sleep(2)

    def get_urls(self):
        title_cards = self.driver.find_elements(By.CLASS_NAME, 'js-tile-link')
        for title in title_cards:
            url = title.get_attribute('href')
            self.url_list.append(url)
        print('urls successfully scraped')

    def scrape(self):
        Initialiser.open_url(self)
        Initialiser.accept_cookies(self)
        n = 1
        for number in range(self.number_of_pages_to_scrape):
            Initialiser.load_pages(self)
            n += 1
            time.sleep(2)
        print(f'{n} pages loaded')
        Initialiser.get_urls(self)
        return self.url_list


if __name__ == '__main__':
    initialise = Initialiser()
    initialise.scrape()
    print(initialise.url_list)
    initialise.driver.quit()