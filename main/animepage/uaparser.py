from playwright.sync_api import sync_playwright
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import uuid
import requests
import time
from .models import Anime, Genre, AdditionalImage


def links_parser():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
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
        
        
def main():
    type_changer = {
        'Аніме серіали': "ТВ-Серіал",
        "Повнометражка": "Фільм",
        "Онґоїнґ": "Онґоїнґ",
        "OVA": "OVA",
        "ONA": "ONA",
        '': "ТВ-Серіал",
    }
    with open('D:\.prog\lunime-repo\lunime-\links.txt', 'r') as file:
        for link in file:
            print('Ссылка:', link)
            data = player_parser(link)
            title = data['Назва']
            original_title = data['Оригінальна назва']
            ani_type = type_changer[data['Тип']]
            amount_of_episodes = data['Кількість епізодів']
            description = data['Опис']
            date_published = data["Прем'эра"]
            studio = data["Студія"]
            cover = image_saver(data['Обкладинка'])
            player = data['Плеєр']
            genres = data['Жанри']
            additional_images = data["Кадри"]
            
            new_anime = Anime.objects.create(
                title=title,
                original_title=original_title,
                anime_type = ani_type,
                amount_of_episodes = amount_of_episodes,
                description = description,
                date_published = date_published,
                studio = studio,
                cover = cover,
                player = player
            )
            
            genre_objects = []
            for genre in genres:
                try:
                    genre_objects.append(Genre.objects.get_or_create(name=genre)[0])
                except Genre.DoesNotExist:
                                    # Обработка ситуации, когда жанр не найден
                    pass
            new_anime.genres.set(genre_objects)
            
            if additional_images:
                for image in additional_images:
                        image_to_save = AdditionalImage.objects.create(anime=new_anime, image=image_saver(image))
                    
            print("Ссылка прошла парсинг")
def image_saver(image_bytes_io):
    try:
        # Открываем изображение с помощью PIL
        img = Image.open(image_bytes_io)

        # Преобразуем изображение к режиму RGB
        img = img.convert('RGB')

        # Создаем объект BytesIO для сохранения изображения
        img_io = BytesIO()
        img.save(img_io, format='JPEG')  # Выберите формат изображения по вашему усмотрению

        # Создаем объект InMemoryUploadedFile с уникальным именем файла
        img_file = InMemoryUploadedFile(
            img_io, None, f"{uuid.uuid4()}.jpg", 'image/jpeg', img_io.tell(), None
        )

        # Возвращаем объект InMemoryUploadedFile
        return img_file
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def player_parser(link):
    start_time = time.time()
    data = {}
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto(link)
        
        page.wait_for_timeout(2500)
        
        title = page.locator('//*[@id="dle-content"]/article/div[1]/header/h1').text_content()
        data['Назва'] = title
        
        original_title = page.locator('//*[@id="dle-content"]/article/div[1]/header/div[1]').text_content()   
        data['Оригінальна назва'] = original_title
        
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
        data['Тип'] = ani_type
        data['Жанри'] = genre_lst
            
        amount_eps = page.locator('//*[@id="dle-content"]/article/div[1]/div/div/div').text_content()
        data['Кількість епізодів'] = amount_eps.split(' ')[1]
        
        date_published = page.locator('//*[@id="dle-content"]/article/div[1]/header/div[2]').text_content()
        data["Прем'эра"] = date_published.split(' ')[1]
        
        description = page.locator('//*[@id="dle-content"]/article/div[3]/div[1]/div[1]').text_content()
        data['Опис'] = description
        
        studio = page.locator('//*[@id="dle-content"]/article/div[1]/ul/li[2]').text_content()
        data['Студія'] = studio.split('\n')[2]
        
        try:
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
                    print(img)
                    additional_images.append(img)
                    
                else:
                    print(f"Не удалось получить изображение по URL: {src}")
            else:
                print("Изображение не содержит атрибута 'src'")
                
            data['Кадри'] = additional_images
        except:
            print("Кадров нету")
            data['Кадри'] = []
            
        
        cover_wrap = page.query_selector('.pmovie__poster')
        cover_img = cover_wrap.query_selector('img').get_attribute('src')
        if cover_img:
            response = requests.get(f'https://animeua.club/{cover_img}')
            
        if response.status_code == 200:
                # Преобразуем содержимое в объект изображения
            cover = BytesIO(response.content)
                
                # Задаем имя файла на основе URL или другого уникального идентификатора
            data['Обкладинка'] = cover
        else:
            print(f"Не удалось получить изображение по URL: {src}")
            
        player_container = page.locator('//*[@id="dle-content"]/article/div[4]/div[2]/iframe')
        link = player_container.get_attribute('data-src')
        data['Плеєр'] = link
        
        browser.close()
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения: {execution_time} секунд")
    return data
        

main()