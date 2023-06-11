from selenium import webdriver
from selenium.webdriver.common.by import By
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
        Omits any incomplete dictionaries and instead returns None
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
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
            time.sleep(1)
        except:
            pass   
    
    def get_title(self):
        try:
            raw_text = self.driver.find_element(By.XPATH, '//p[@class= "scoreboard__title"]').text
            underscores = raw_text.upper().replace(' ', '_')
            title = re.sub(r'[^a-zA-Z0-9_]', '', underscores)
        except:
            title = 'N/A'
        return title

    def get_scores(self):
        try:
            tomatometer = self.driver.find_element(By.XPATH, '//SCORE-BOARD[@class= "scoreboard"]').get_attribute('tomatometerscore')
            if tomatometer == '':
                tomatometer = 'N/A'
        except:
            tomatometer = 'N/A'
        try:
            audience_score = self.driver.find_element(By.XPATH, '//SCORE-BOARD[@class= "scoreboard"]').get_attribute('audiencescore')
            if audience_score == '':
                audience_score = 'N/A'
        except:
            audience_score = 'N/A'
        return tomatometer, audience_score


    def get_synopsis(self):
        try:
            self.driver.find_element(By.XPATH, '//button[@class= "button--link"]').click()
        except:
            pass
        try:
            synopsis_raw_text = self.driver.find_element(By.XPATH, '//p[@data-qa= "series-info-description"]').text
            synopsis = str(BeautifulSoup(synopsis_raw_text, 'html.parser'))
        except:
            synopsis = 'N/A'
        return synopsis

    def get_additional_show_data(self):
        try:
            list_items = self.driver.find_elements(By.XPATH, '//SECTION[@id="series-info"]/div/ul/li')
            for item in list_items:
                name = item.text.split(":")[0]
                if name == 'TV Network':
                    network = item.text.split(":")[1][1:]
                if name == 'Premiere Date':
                    premiere_date = item.text.split(":")[1][1:]
                if name == 'Genre':
                    genre = item.text.split(":")[1][1:]
        except:
            network = 'N/A'
            premiere_date = 'N/A'
            genre = 'N/A'
        return network, premiere_date, genre


    def get_img(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@data-qa= "poster-image"]')))
            img = self.driver.find_element(By.XPATH, '//img[@data-qa= "poster-image"]').get_attribute('src')
        except:
            img = 'N/A'    
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
        self.item_dict['TV Network'] = Items.get_additional_show_data(self)[0]
        self.item_dict['Premiere Date'] = Items.get_additional_show_data(self)[1]
        self.item_dict['Genre'] = Items.get_additional_show_data(self)[2]
        self.item_dict['Img'] = Items.get_img(self)
        self.item_dict['Timestamp'] = Items.get_timestamp(self)
        self.item_dict['ID'] = Items.get_uuid(self)
        for key, value in self.item_dict.items():
            if value == 'N/A':
                print(f'{self.get_title()}: invalid {key} data, result omitted')
                return None
        return self.item_dict


if __name__ == '__main__':
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--window-size=1920,1080')
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(options=firefox_options)
    test_url = 'https://www.rottentomatoes.com/tv/the_last_of_us'
    driver.get(test_url)
    time.sleep(2)
    items = Items(driver)
    item_dict = items.get_items()
    driver.quit()
