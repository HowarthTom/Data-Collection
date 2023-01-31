import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import os
import json
import time
from datetime import datetime 



class Scraper:
    def __init__(self, rt_link, tv_or_movie_selection, number_of_pages, additional_data):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.rt_link = rt_link
        self.tv_or_movie_selection = tv_or_movie_selection
        self.number_of_pages = number_of_pages
        self.additional_data = additional_data
        self.driver.get(self.rt_link)
        time.sleep(2)
        self.accept_cookies()


    def accept_cookies(self):
        try:
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
            accept_cookies_button.click()

        except Exception as cookies_error:
            print(cookies_error)
        
        self.tv_or_movies()


    def tv_or_movies(self):
        tv_show_data = '//*[@id="header-main"]/rt-header-nav/rt-header-nav-item[2]/a'
        movie_data = '//*[@id="header-main"]/rt-header-nav/rt-header-nav-item[1]/a'
        if self.tv_or_movie_selection == 'tv_show_data':
            tv_or_movies = tv_show_data
        elif self.tv_or_movie_selection == 'movie_data':
            tv_or_movies = movie_data
        
        self.driver.find_element(By.XPATH, tv_or_movies).click()
        self.number_of_pages_to_scrape()


    def number_of_pages_to_scrape(self):
        for index in range(self.number_of_pages):
            self.driver.find_element(By.XPATH, '//*[@id="main-page-content"]/div/div[5]/button').click()
            time.sleep(2)    
        
        self.get_data()


    def get_data(self):
        title_cards = self.driver.find_elements(By.CLASS_NAME, 'js-tile-link')
        for element in title_cards:
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'posterImage')))
                img = element.find_element(By.CLASS_NAME, 'posterImage').get_attribute('currentSrc')
                print(img)
            except Exception as locate_img_error:
                print(locate_img_error)
                continue

            title = element.find_element(By.CLASS_NAME, 'p--small').get_attribute('innerText')
            audience_score = element.find_element(By.TAG_NAME, 'SCORE-PAIRS').get_attribute('audiencescore')
            critic_score = element.find_element(By.TAG_NAME, 'SCORE-PAIRS').get_attribute('criticsscore')
            href = element.get_attribute('href')

            dateTimeObj = datetime.now()
            timestamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

            self.item = {
                'Title': title,
                'Audience Score': audience_score,
                'Critic Score': critic_score,
                'Timestamp': timestamp
            }   
            if self.additional_data == 'yes':
                self.get_additional_data(href)
            else:
                continue
            self.save_data(title, self.item, img)

        
    def get_additional_data(self, href):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(href)

        if self.tv_or_movie_selection == 'tv_show_data':
            try:
                self.driver.find_element(By.CLASS_NAME, 'button--link js-clamp-toggle clamp-toggle__show-more').click()
            except:
                pass
            synopsis = self.driver.find_element(By.CSS_SELECTOR, '[class*="tv-series__series-info--synopsis clamp clamp-6 js-clamp"]').get_attribute('innerText')
            premiere_date = self.driver.find_element(By.XPATH, '//*[@id="detail_panel"]/div/table/tbody/tr[2]/td[2]').get_attribute('innerText')
        else:
            synopsis = self.driver.find_element(By.XPATH, '//*[@id="movieSynopsis"]').get_attribute('innerText')
            premiere_date = self.driver.find_element(By.TAG_NAME, 'TIME').get_attribute('innerText')
        
        dateTimeObj = datetime.now()
        timestamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

        self.item.update({
            'Synopsis': synopsis,
            'Premiere Date': premiere_date,
            'Timestamp': timestamp
        })

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


    def save_data(self, title, item, img):
        file_path = f'raw_data/{self.tv_or_movie_selection}/{title}'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        try:
            with open(f'{file_path}/data.json', 'w') as fp:
                json.dump(obj=item, indent=4, fp=fp)
        except Exception as save_data_error:
            print(save_data_error)
        try:
            print(title, img)
            img_data = requests.get(img).content
            with open(f'{file_path}/{title}.jpg', 'wb') as handler:
                handler.write(img_data)
        except Exception as save_img_error:
            print(save_img_error)
        
            
        

if __name__ == '__main__':
    rt_link = 'https://www.rottentomatoes.com/'
    tv_or_movie_selection = 'movie_data'
    number_of_pages = 2
    additional_data = 'yes'
   
    scraper = Scraper(rt_link, tv_or_movie_selection, number_of_pages, additional_data)
    scraper