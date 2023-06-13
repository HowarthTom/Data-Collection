# Data Collection Pipeline

This project uses various webscraping and html parsing tools such as selenium, chromedriver, beatifulsoup to collect and analyse data from the rottentomatoes website.

## Milestone 1 - Choosing a website 

* I chose rotten tomatoes for this project as it contains lots of different forms of data (TV show info, images, links to other pages), which is updated and changed on a regular basis. 
* This provides the challenge of making a webscraper that both targets specific data and adapts to change. 
* Furthermore, the data collected from this website can be used to provide some interesting and useful information to the user, such as ranking by critic and audience scores simultaneously.

## Milestone 2 - Creating the initialiser class and methods

* The initialiser class visits the 'TV show' page on rotten tomatoes and scrapes a list of urls for each show.
    - The challenge was that sometimes it would load an incorrect number of pages if the 'load more' button was slow to load in. I solved this by adding a webdriver waitkey that waits for the presence of the button before trying to execute any more of the script.  
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
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
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--window-size=1920,1080')
        firefox_options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=firefox_options)
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
            if url == None:
                url = title.find_element(By.XPATH, './/a[@data-qa= "discovery-media-list-item-caption"]').get_attribute('href')

            print(url)
            self.url_list.append(url)

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
        print(f'{len(self.url_list)} urls successfully scraped')
        return self.url_list


if __name__ == '__main__':
    initialise = Initialiser()
    initialise.scrape()
    #print(initialise.url_list)
    initialise.driver.quit()
```

## Milestone 3 - Creating the data handling classes and methods

* The items class creates a dictionary of all the required data from each TV show page.
    - Here I had to make use of the try: except: function, since a lot of the data was not consistent across each page. Some required a button click to reveal the whole synopsis, some didn't have enough data to provide a tomatometer score.
    - I also discovered that the elements containing the scores required '.text' instead of 'get_attribute('innerText')' to get the data I wanted, even though 'get_attribute('innerText')' worked correctly for the other elements. This is because 'innerText' is not a standard HTML attribute and is explicitly defined, whereas the '.textContent' attribute is standard, and always returns the text attribute of an element, whether its defined as innerText or as something else such as outerText or textContent.

```python
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
```

* The saver class is used to save the dictionary locally as a JSON file, with the poster image saved seperately as a JPG file.

```python
import os
import json
import requests

class Saver:
    '''
    This class creates a local folder for each TV show and saves the dictionary and img data inside

    Parameters:
    ----------
    item_dict: dict
        The dictionary used to store all of the information for a particular TV show

    
    Attributes:
    ----------
    item_dict: dict
        The dictionary used to store all of the information for a particular TV show
    img: str
        The TV show's poster img url
    title: str
        The TV show's title
    file_path: str
        The location in the directory where the files will be saved 

    
    Methods:
    -------
    save_item_dict()
        Creates the folder for the TV show if it does not already exist and saves the dictionary in the folder as a JSON file
    save_img()
        Reads the content of the poster img url and saves it in the folder as a JPG file
    save()
        Calls the other methods 
    '''
    def __init__(self, item_dict):
        self.item_dict = item_dict
        self.img = self.item_dict['Img']
        self.title = self.item_dict['Title']
        self.file_path = os.path.abspath(f'../raw_data/{self.title}')

    def save_item_dict(self):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        with open(f'{self.file_path}/data.json', 'w') as fp:
            json.dump(obj=self.item_dict, indent=4, fp=fp)

    def save_img(self):
        img_data = requests.get(self.img).content
        with open(f'{self.file_path}/{self.item_dict["Title"]}.jpg', 'wb') as handler:
            handler.write(img_data)

    def save(self):
        Saver.save_item_dict(self)
        Saver.save_img(self)
        print(f'{self.title}: scraped successfully')


if __name__ == '__main__':
    test_item = {'Title': 'THE_LAST_OF_US', 'Tomatometer': '96%', 'Audience Score': '90%', 'Synopsis': 'Joel and Ellie must survive ruthless killers and monsters on a trek across America after an outbreak.', 'TV Network': 'HBO', 'Premiere Date': 'Jan 15, 2023', 'Genre': 'Action', 'Img': 'https://resizing.flixster.com/T-YbkLxt3WvVPB2ZLnHUT8nYb68=/206x305/v2/https://resizing.flixster.com/2TwYzc7hklVW2s4fN1ypuyYWMj0=/ems.cHJkLWVtcy1hc3NldHMvdHZzZXJpZXMvYjBiZTZiODMtODQ1OC00MDY3LTkzNTItZjZlMzQ5ZGM1MzEwLmpwZw==', 'Timestamp': '02-Mar-2023 (13:40:22.150968)', 'ID': 'cf5a5ea2-cae7-4f91-9968-677821b80ff7'}
    save = Saver(test_item)
    save.save()
```

* Finally, the scraper class is used to instantiate the other classes and 'activate' the scraper.
    - I felt the scraper performed quite slowly, so to speed up the process I added multithreading, which runs seperate instances of the items and saver class simultaneously, using a list of urls obtained from the initialiser class.

```python
from selenium import webdriver
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
        Creates a webdriver instance and visit a particular url from the url_list
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
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--window-size=1920,1080')
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)
        driver.get(url)
        time.sleep(1)
        items = Items(driver)
        self.item_dict = items.get_items()  
        driver.quit()
        time.sleep(1)
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
```

## Milestone 4 - Adding testing 

* Unit tests were added to test each of the modules and ensure they were functioning as intended.
* The InitialiserTestcase tests to make sure that the url_list is 150 items long (equal to the first 5 pages of results on rotten tomatoes), and that all the urls are valid links.

```python
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
```

* The ItemsTestcase opens a random link from the url_list and checks to make sure it is not an omitted result that had insufficient data. If this check passes, it tests to make sure the item_dict has been filled in correctly as expected.

```python
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
```

* The SaverTestcase uses a sample item_dict item and creates a temporary directory to mimic the file path the Saver class would use when saving an item locally. It tests to make sure the temporary directory is created and the files are saved correctly inside as expected.

```python
import unittest
import tempfile
import os
import sys
sys.path.append('../')
from scraper.saver import Saver

class SaverTestcase(unittest.TestCase):

    def setUp(self):
        self.item_dict = {
            "Title": "THE_LAST_OF_US",
            "Tomatometer": 96,
            "Audience Score": 90,
            "Synopsis": "Joel and Ellie must survive ruthless killers and monsters on a trek across America after an outbreak.",
            "TV Network": "HBO",
            "Premiere Date": "Jan 15, 2023",
            "Genre": "Action",
            "Img": "https://resizing.flixster.com/T-YbkLxt3WvVPB2ZLnHUT8nYb68=/206x305/v2/https://resizing.flixster.com/2TwYzc7hklVW2s4fN1ypuyYWMj0=/ems.cHJkLWVtcy1hc3NldHMvdHZzZXJpZXMvYjBiZTZiODMtODQ1OC00MDY3LTkzNTItZjZlMzQ5ZGM1MzEwLmpwZw==",
            "Timestamp": "06-Mar-2023 (15:34:08.470630)",
            "ID": "846bdd65-d825-406f-8a36-895b1be8e152"
        }
        self.title = self.item_dict['Title']

        self.temp_dirs = tempfile.TemporaryDirectory()
        self.temp_file_path = os.path.abspath(f'{self.temp_dirs.name}/raw_data/{self.title}')
        self.temp_file_path_dict = os.path.abspath(f'{self.temp_dirs.name}/raw_data/{self.title}/data.json')
        self.temp_file_path_img = os.path.abspath(f'{self.temp_dirs.name}/raw_data/{self.title}/{self.title}.jpg')

    def tearDown(self):
        self.temp_dirs.cleanup()

    def test_save(self):
        save = Saver(self.item_dict)
        save.file_path = self.temp_file_path
        save.save()
        self.assertTrue(os.path.isdir(self.temp_file_path))
        self.assertTrue(os.path.isfile(self.temp_file_path_dict))
        self.assertTrue(os.path.isfile(self.temp_file_path_img))
```

* The ScraperTestcase tests performs a mock scrape with all of the urls in the url_list. It checks that all of the urls are used to call the scrape_items method, and that each url is used exactly once. This is to ensure that the multithreading aspect of the Scraper class doesn't open multiple instances of the same url simultaneously.

```python
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
```

## Milestone 5 - Creating a Docker image

* Various Docker files were created to containerise the scraper and allow for deployment across platforms. 
* Firstly, a Dockerfile with the necessary components to build a docker image. This required massive restructuring of my code, as chromedriver and chromedrivermanager were incompatible. I changed the browser to firefox and used geckodriver instead.

```dockerfile
FROM python:3.10.2-slim-buster

RUN apt-get update
#install system depend
RUN apt-get install -y software-properties-common


# Install Firefox and GeckoDriver
RUN apt-get update && apt-get install -y firefox-esr && apt-get install -y wget && \
    wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz" -O geckodriver.tgz && \
    tar -xvzf geckodriver.tgz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver.tgz

# Creates the /app directory 
RUN mkdir /app

# Sets /app as the working directory
WORKDIR /app

# Copies required files to the directory
COPY initialiser.py /app/
COPY items.py /app/
COPY saver.py /app/
COPY scraper.py /app/
COPY requirements.txt /app/

# Installs the dependencies 
RUN pip install -r requirements.txt

# Disables buffering to allow continuous output
ENV PYTHONBUFFERED 1

# Sets the entrypoint when the dockerfile runs
CMD ["python3", "scraper.py"]
```

* Next, a docker-compose file was created to automatically build the docker image.

```yaml
version: '20.10.23'

services:
  scraper_container:
    build:
      context: .
      dockerfile: Dockerfile
    image: rt_scraper
    ports:
      - "5432:5432"
    volumes:
      - /Users/tom/Desktop/Data-Collection/Data-Collection/docker/raw_data:/app/raw_data
    tty: true
    stdin_open: true
```

* Lastly, a CI/CD pipeline was created, which automatically pushes updates to dockerhub whenever a git push is made to the main repository, ensuring the docker image is up to date.

```yml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - 
        name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}

      - 
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - 
        name: Build and push
        uses: docker/build-push-action@v3
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_HUB_USERNAME }}/rt_scraper
```