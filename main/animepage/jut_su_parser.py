import re
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, parse_qs, quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException,  TimeoutException, NoSuchElementException

from PIL import Image
import requests
from io import BytesIO



def links_parser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://animeua.club/f/sort=rating/order=desc/")

        counter = 0
        with open("links.txt", "a", encoding="utf-8") as file:
            for i in range(1, 34):
                page.goto(f"https://animeua.club/f/sort=rating/order=desc/page/{i}/")
                
                links = page.query_selector_all('.poster')
                for link in links:
                    href = link.get_attribute('href')
                    file.write(href + "\n")

        print(counter)
        browser.close()
        
def player_parser(link):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(link)
        
        page.wait_for_timeout(2000)
        player_container = page.locator('//*[@id="dle-content"]/article/div[4]/div[2]/iframe')
        link = player_container.get_attribute('data-src')
        print(link) 
        
        title = page.locator('//*[@id="dle-content"]/article/div[1]/header/h1').text_content()
        print(title)
        
        original_title = page.locator('//*[@id="dle-content"]/article/div[1]/header/div[1]').text_content()
        print(original_title)        
        
        genres_div = page.query_selector('.pmovie__genres')
        genres = genres_div.query_selector_all('a')
        ani_type = ''
        genre_lst = []
        types = ['Аніме серіали', 'Повнометражка', "OVA", "ONA", 'Онґоїнґ']
        for genre in genres:
            if genre.text_content() in types:
                ani_type = genre.text_content()
            else:
                genre_lst.append(genre.text_content())
        print(f'Тип: {ani_type}')
        print(genre_lst)
            
        amount_eps = page.locator('//*[@id="dle-content"]/article/div[1]/div/div/div').text_content()
        print(amount_eps.split(' ')[1])
        
        date_published = page.locator('//*[@id="dle-content"]/article/div[1]/header/div[2]').text_content()
        print(date_published.split(' ')[1])
        
        description = page.locator('//*[@id="dle-content"]/article/div[3]/div[1]/div[1]').text_content()
        print(description)
        
        studio = page.locator('//*[@id="dle-content"]/article/div[1]/ul/li[2]').text_content()
        print(studio.split('\n')[2])
        
        
        
        images_button = page.locator('//*[@id="dle-content"]/article/div[3]/div[2]/div[1]/div').click()
        image_wrap = page.query_selector('.screenshots')
        image_list = image_wrap.query_selector_all('a')
        additional_images = []
        for image in image_list:
            src = image.query_selector('img').get_attribute('src')
            if src:
        # Получаем содержимое изображения
                response = requests.get(f'https://animeua.club/{src}')
            
            # Проверяем успешность запроса
            if response.status_code == 200:
                # Преобразуем содержимое в объект изображения
                img = BytesIO(response.content)
                
                # Задаем имя файла на основе URL или другого уникального идентификатора
                additional_images.append(img)
                
            else:
                print(f"Не удалось получить изображение по URL: {src}")
        else:
            print("Изображение не содержит атрибута 'src'")
            
        
            
        print(additional_images)
        
        cover_wrap = page.query_selector('.pmovie__poster')
        cover_img = cover_wrap.query_selector('img').get_attribute('src')
        if cover_img:
            response = requests.get(f'https://animeua.club/{cover_img}')
            
        if response.status_code == 200:
                # Преобразуем содержимое в объект изображения
            cover = BytesIO(response.content)
                
                # Задаем имя файла на основе URL или другого уникального идентификатора
            print(cover)
        else:
            print(f"Не удалось получить изображение по URL: {src}")
        
        print(cover_img)

        
    
    
if __name__ == "__main__":
    player_parser("https://animeua.club/7347-one-piece.html")