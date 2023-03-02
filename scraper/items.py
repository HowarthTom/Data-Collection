from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import uuid
from bs4 import BeautifulSoup
import re


class Items:
    '''
    This class defines a dictionary with the keys needed to store TV show data,
    then locates each corresponding value on the rotten tomatoes page

    Parameters:
    ----------
    url: str
        url for the rotten tomatoes page of a particular TV show


    Attributes:
    ----------
    item_dict: dict
        The dictionary used to store all of the information for a particular TV show


    Methods:
    -------
    accept_cookies()
        Accepts the cookies pop-up
    get_title()
        Locates the title text and returns it with a consistent reformatting
    get_scores()
        Locates and returns the tomatometer and audience scores
    get_synopsis()
        Locates and clicks a button the show the full synopsis, formats the synopsis with the beautifulsoup html parser, then returns it
    get_tv_network()
        Locates and returns the TV network
    get_premiere_date()
        Locates and returns the premiere date
    get_genre()
        Locates and returns the genre
    get_img()
        Locates and returns the poster img url
    get_timestamp()
        Returns the current datetime at which the item was scraped
    get_uuid()
        Assigns and returns a uuid code for each TV show
    get_items()
        Calls the other methods and replaces the corresponding dictionary value with their return values, then returns the populated dictionary
    '''

    def __init__(self, driver):
        self.driver = driver
        self.item_dict = {
            'Title': 'N/A',
            'Tomatometer': 'N/A',
            'Audience Score': 'N/A',
            'Synopsis': 'N/A',
            'TV Network': 'N/A',
            'Premiere Date': 'N/A',
            'Genre': 'N/A',
            'Img': 'N/A',
            'Timestamp': 'N/A',
            'ID': 'N/A'
        }
    
    def accept_cookies(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        except:
            pass   
    
    def get_title(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[@class= "mop-ratings-wrap__title mop-ratings-wrap__title--top"]')))
            raw_text = self.driver.find_element(By.XPATH, '//h1[@class= "mop-ratings-wrap__title mop-ratings-wrap__title--top"]').get_attribute('innerText')
            underscores = raw_text.upper().replace(' ', '_')
            title = re.sub(r'[^a-zA-Z0-9_]', '', underscores)
        except:
            print('Page not responding')
        return title

    def get_scores(self):
        scores = self.driver.find_elements(By.XPATH, '//span[@class= "mop-ratings-wrap__percentage"]')
        tomatometer = scores[0].get_attribute('innerText')
        audience_score = scores[1].get_attribute('innerText')
        return tomatometer, audience_score

    def get_synopsis(self):
        try:
            self.driver.find_element(By.XPATH, '//button[@data-qa= "more-btn"]').click()
        except:
            pass
        synopsis_raw_text = self.driver.find_element(By.XPATH, '//div[@id= "movieSynopsis"]').get_attribute('innerText')
        synopsis = str(BeautifulSoup(synopsis_raw_text, 'html.parser'))
        return synopsis

    def get_tv_network(self):
        network = self.driver.find_element(By.XPATH, '//td[@data-qa= "series-details-network"]').get_attribute('innerText')
        return network

    def get_premiere_date(self):
        premiere_date = self.driver.find_element(By.XPATH, '//td[@data-qa= "series-details-premiere-date"]').get_attribute('innerText')
        return premiere_date

    def get_genre(self):
        genre = self.driver.find_element(By.XPATH, '//td[@data-qa= "series-details-genre"]').get_attribute('innerText')
        return genre

    def get_img(self):
        img = self.driver.find_element(By.XPATH, '//img[@class= "posterImage"]').get_attribute('currentSrc')
        return img

    def get_timestamp(self):
        dateTimeObj = datetime.now()
        timestamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        return timestamp

    def get_uuid(self):
        id = str(uuid.uuid4())
        return id

    def get_items(self):
        Items.accept_cookies(self)
        self.item_dict['Title'] = Items.get_title(self)
        self.item_dict['Tomatometer'] = Items.get_scores(self)[0]
        self.item_dict['Audience Score'] = Items.get_scores(self)[1]
        self.item_dict['Synopsis'] = Items.get_synopsis(self)
        self.item_dict['TV Network'] = Items.get_tv_network(self)
        self.item_dict['Premiere Date'] = Items.get_premiere_date(self)
        self.item_dict['Genre'] = Items.get_genre(self)
        self.item_dict['Img'] = Items.get_img(self)
        self.item_dict['Timestamp'] = Items.get_timestamp(self)
        self.item_dict['ID'] = Items.get_uuid(self)
        return self.item_dict


if __name__ == '__main__':
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    test_url = 'https://www.rottentomatoes.com/tv/the_last_of_us'
    driver.get(test_url)
    time.sleep(2)
    items = Items(driver)
    item_dict = items.get_items()
    driver.quit()
    print(item_dict)
