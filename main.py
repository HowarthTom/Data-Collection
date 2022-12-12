import selenium
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome()
time.sleep(2)
show_list = []

def get_show_score():
    link = 'https://www.rottentomatoes.com/'
    driver.get(link)

    time.sleep(2)

    try:
        accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
        accept_cookies_button.click()

    except Exception as e:
        print(e)


    driver.find_element(By.XPATH, '//*[@id="header-main"]/rt-header-nav/rt-header-nav-item[2]/a').click()
    time.sleep(2)
    shows = driver.find_elements(By.CLASS_NAME, 'js-tile-link')
    for show in shows:
        title = show.find_element(By.CLASS_NAME, 'p--small').get_attribute('innerText')
        img = show.find_element(By.CLASS_NAME, 'posterImage').get_attribute('currentSrc')
        critic_score = show.find_element(By.TAG_NAME, 'score-pairs').get_attribute('criticsscore')
        audience_score = show.find_element(By.TAG_NAME, 'score-pairs').get_attribute('audiencescore')

        link = show.get_attribute('href')
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        
        time.sleep(2)

        try:
            driver.find_element(By.CLASS_NAME, 'button--link js-clamp-toggle clamp-toggle__show-more').click()
        
        except Exception as e:
            #print(e)
            pass
        
        synopsis = driver.find_element(By.CSS_SELECTOR, '[class^="tv-series__series-info--synopsis clamp clamp-6 js-clamp clearfix"]').text
        aired = driver.find_element(By.CLASS_NAME, 'h3.subtle').text[1:-1]
        seasons = len(driver.find_elements(By.TAG_NAME, 'season-list-item'))

        global item
        item = {
            'Title': title,
            'Synopsis': synopsis,
            'Img': img,
            'Critic Score': critic_score,
            'Audience Score': audience_score,
            'Aired': aired,
            'Seasons': seasons
        }
        show_list.append(item)
        save_images(img, title)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        
    
    df = pd.DataFrame(show_list)
    print(df)


def save_images(img, title):
    img_data = requests.get(img).content
    with open(f'images/{title}.jpg', 'wb') as handler:
        handler.write(img_data)
    

if __name__ == '__main__':
    get_show_score()