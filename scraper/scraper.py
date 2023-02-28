from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class Scraper:

    def __init__(self, number_of_pages_to_scrape=2):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.number_of_pages_to_scrape = number_of_pages_to_scrape
        self.href_list = []

    def open_url(self):
        self.driver.get('https://www.rottentomatoes.com/browse/tv_series_browse/sort:popular')
        time.sleep(2)

    def accept_cookies(self):
        self.driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]').click()
        time.sleep(2)

    def load_pages(self):
        button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Load more")]')
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()
        time.sleep(2)

    def get_hrefs(self):
        title_cards = self.driver.find_elements(By.CLASS_NAME, 'js-tile-link')
        for title in title_cards:
            href = title.get_attribute('href')
            self.href_list.append(href)

    def scrape(self):
        Scraper.open_url(self)
        Scraper.accept_cookies(self)
        for number in range(self.number_of_pages_to_scrape):
            Scraper.load_pages(self)
            time.sleep(2)
        Scraper.get_hrefs(self)
        return self.href_list


if __name__ == '__main__':
    scrape = Scraper()
    scrape.scrape()
    print(scrape.href_list)
    scrape.driver.quit()