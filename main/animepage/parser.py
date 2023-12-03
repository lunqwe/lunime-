import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException,  TimeoutException, NoSuchElementException
from django.core.files.base import ContentFile
import traceback
from .models import Anime, Genre, Episode, Film
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from PIL import Image

def animego_link_parser(link):
    print("Начинаем парсить...")
    links_counter = 0
    anime_counter = 0

    with open('D:\.prog\lunime\links.txt', "w", encoding='utf-8') as file:
        for i in range(1, 124):
            links_counter += 1
            print("Парсим страницу "+str(links_counter))
            r = requests.get(link+str(i))
            html = BS(r.content, 'html.parser').select('.mb-1')
            for element in html:
                data = element.select_one("a")
                if data:
                    href = data.get('href')
                    print(href)
                    file.write(href + '\n')
                    anime_counter += 1

    print("Спаршено страниц:", links_counter)
    print("Получено аниме:", anime_counter)


def links_parser(file_name):
    print("Начинаем парсить")
    with open(file_name, 'r', encoding='utf-8') as file:
        anime_data = []
        error_links = []
        counter = 0
        for link in file:
            print("====================================\n")
            print(f"Парсим ссылку: {link.strip()}")
            link_data = parser(link.strip())
            if link_data is None:
                print("❌ Ссылка не прошла парсинг: " + link.strip())
                error_link('links.txt', link.strip())
                remove_first_line(file_name)
                print("Cсылка с ошибкой добавлена в конец списка ссылок")
            else:
                print(link_data)
                if link_data.get('type','') == 'Anime':
                    title = link_data.get('Название', '')
                    data_description = link_data.get('Характеристики', {})
                    a_type = data_description.get('Тип', '0')
                    amount_of_episodes = data_description.get('Эпизоды', '0')
                    status = data_description.get('Статус', '0')
                    genres = data_description.get('Жанр', '').split(', ')
                    origin_source = data_description.get('Первоисточник', '0')
                    release = data_description.get('Выпуск', '0')
                    studio = data_description.get('Студия', '0')
                    duration = data_description.get('Длительность', '0')
                    description = data_description.get('Описание', '0')
                    image = image_saver(link_data.get('Обложка', ''))
                    try:
                        check = Anime.objects.filter(title = title)
                        if check:
                            print("найдена повторка, аниме не добавится")
                            remove_first_line(file_name)
                        else:
                            new_anime = Anime.objects.create(
                                title=title,
                                image = image,
                                anime_type = a_type,
                                description = description,
                                date_published = release,
                                status = status,
                                studio = studio,
                                amount_of_episodes = amount_of_episodes,
                                duration = duration,
                                origin_source = origin_source,
                            )
                            for key, value in link_data['Плеер'].items():
                                new_episode = Episode.objects.create(
                                    anime = new_anime,
                                    n_episode = key,
                                    kodik_link = value,
                                )
                            genre_objects = []
                            for genre in genres:
                                try:
                                    genre_objects.append(Genre.objects.get_or_create(name=genre)[0])
                                except Genre.DoesNotExist:
                                    # Обработка ситуации, когда жанр не найден
                                    pass
                            new_anime.genres.set(genre_objects)
                            remove_first_line(file_name)
                    except Exception as e:
                        print(f"Ошибка добавления в базу данных: {e}")                
                        
                elif link_data.get('type','') == 'Film':
                    title = link_data.get('Название', '')
                    data_description = link_data.get('Характеристики', {})
                    a_type = data_description.get('Тип', '0')
                    amount_of_episodes = data_description.get('Эпизоды', '0')
                    genres = data_description.get('Жанр', '').split(', ')
                    origin_source = data_description.get('Первоисточник', '0')
                    release = data_description.get('Выпуск', '0')
                    studio = data_description.get('Студия', '0')
                    duration = data_description.get('Длительность', '0')
                    description = data_description.get('Описание', '0')
                    image = image_saver(link_data.get('Обложка', ''))
                    link = link_data['Плеер']['Ссылка']
                    try:
                        try:
                            check = Film.objects.get(title = title)
                            print("найдена повторка, аниме не добавится")
                            remove_first_line(file_name)
                        except:
                            new_film = Film.objects.create(
                                title = title,
                                image = image,
                                anime_type = a_type,
                                description = description,
                                date_published = release,
                                studio = studio,
                                duration = duration,
                                origin_source = origin_source,
                                link = link
                            )
                            
                            genre_objects = []
                            for genre in genres:
                                try:
                                    genre_objects.append(Genre.objects.get_or_create(name=genre)[0])
                                except Genre.DoesNotExist:
                                        # Обработка ситуации, когда жанр не найден
                                    pass
                            new_film.genres.set(genre_objects) 
                            remove_first_line(file_name)
                    except Exception as e:
                        print(f"Ошибка: {e}")
                
                print("Ссылка удалена из списка ссылок")    
                counter += 1
                print("✔️   Количество ссылок, которые уже прошли парсинг:", counter)

    print("Удачно:", len(anime_data))
    print("Неудачно:", len(error_links))
    print("Парсинг успешно завершен!")

def error_link(file_path, link_to_add):
    try:
        # Открываем файл для добавления ссылки в конец
        with open(file_path, 'a') as file:
            file.write(link_to_add + '\n')

        print(f"Ссылка {link_to_add} успешно добавлена в файл {file_path}")
    except Exception as e:
        print(f"Произошла ошибка при добавлении ссылки: {e}")

def remove_first_line(file_path):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        with open(file_path, "w") as f:
            f.writelines(lines[1:])

        print(f"Первая строка успешно удалена из файла {file_path}")
    except Exception as e:
        print(f"Произошла ошибка при удалении первой строки: {e}")


def link_check(player_link, driver):
    check_src = player_link.get_attribute('data-player').split('?')[0]
    if check_src.startswith('//kodik.info/'):
        return True
    else:
        return False


def film_parser(driver, link):
    film_dict = {}
    try:
        player_select_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="video-players-tab"]'))
            )
        player_select_btn.click()
    except:
        player_select_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="video-players-tab"]'))
                )
        player_select_btn.click()
        print(f"Произошла ошибка: {e}")
        traceback.print_exc() 
                                
    span_lst = [1,2,3,4,5,6,7,8,9]
    for num in span_lst:
        try:
            player_link = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, f'//*[@id="video-players"]/span[{num}]'))
                )
            src_check = link_check(player_link, driver)
            if src_check:
                break
        except(StaleElementReferenceException, TimeoutException, NoSuchElementException):
                continue
    if src_check == True:
        try:
            film_link = player_link.get_attribute('data-player').split('?')[0]
            print(film_link)
            print("✔️  Ссылка на фильм/односерийное аниме - получено")
            print(f'{link.strip()}: парсинг пройден')
            film_dict['Ссылка'] = film_link
            driver.quit()
            return film_dict
        except Exception as e:
            print("Не удалось получить ссылку на плеер")
            print(f"Произошла ошибка: {e}")
            traceback.print_exc() 
    else:
        print("Нету ссылки кодика, аниме не добавится в базу")
        driver.quit()
        return None

def process_data(input_data):
    expected_keys = ["Тип", "Эпизоды", "Статус", "Жанр", "Первоисточник", "Сезон", "Выпуск", "Студия", "Длительность"]
    
    output_data = {key: input_data.get(key, 0) for key in expected_keys}
    
    return output_data

def series_parser(driver, link, ongoing):
    episodes_dict = {}
    counter = 0
    try:
        carousel = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.ID, "video-carousel"))
        )

        buttons = carousel.find_elements(By.CLASS_NAME, "video-player-bar-series-item")
        
        for button in buttons:
            button.click()
            try:
                player_select_btn_locator = (By.XPATH, '//*[@id="video-players-tab"]')
                player_select_btn = WebDriverWait(carousel, 5).until(
                    EC.presence_of_element_located(player_select_btn_locator)
                )
                player_select_btn.click()
            except:
                player_select_btn_locator = (By.XPATH, '//*[@id="video-players-tab"]')
                player_select_btn = WebDriverWait(carousel, 5).until(
                    EC.presence_of_element_located(player_select_btn_locator)
                )
                player_select_btn.click() 
            player_select_btn.click()       
            try:
                span_lst = [1,2,3,4,5,6,7,8,9]
                for num in span_lst:
                    try:
                        player_link = WebDriverWait(driver, 3).until(
                            EC.visibility_of_element_located((By.XPATH, f'//*[@id="video-players"]/span[{num}]'))
                        )
                        src_check = link_check(player_link, driver)
                        if src_check:
                            break
                    except(StaleElementReferenceException, TimeoutException, NoSuchElementException):
                        continue
                    
                    
                    
                    
            except Exception as e:
                print(f"Ошибка {e}")
                traceback.print_exc()
                
            if src_check:
                counter += 1
                try:
                    episode = player_link.get_attribute('data-player').split('?')[0]
                except StaleElementReferenceException:
                    episode = player_link.get_attribute('data-player').split('?')[0]
                print(f'{counter} - '+ episode)
                episodes_dict[counter] = episode
            else:
                print("❌Нету ссылки кодика, аниме не добавится в базу")
                return None
        
        print(f'✔️   {link.strip()}: парсинг пройден')
        print("Полученное количество серий:", counter,'\n')
        return episodes_dict

    except StaleElementReferenceException as stale_error:
    # Обработка устаревшего элемента
        print(f"Произошла ошибка StaleElementReferenceException: {stale_error}")
        # Возможно, здесь вы захотите попробовать выполнить дополнительные шаги для восстановления ситуации
        return None
    except Exception as e:
        if ongoing:
            print("✔️   Это онгоинг, парсинг доступных серий прошел успешно")
            with open('ongoings', "w") as f:
                f.writelines(link)
            return episodes_dict
        else:
            print("Ошибка", e)
            traceback.print_exc() 
            return None
    
    finally:
        driver.quit()

def image_parser(driver, link):
    try:
        image_element = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/img'))
        )
        image_url = image_element.get_attribute('src')

        image_content = requests.get(image_url).content

        image_file = io.BytesIO(image_content)
        image_file.name = image_url.split('/')[-1]

        return image_file

    except Exception as e:
        print(f"Ошибка при парсинге и сохранении изображения: {e}")
        return None

def image_saver(image):
    image = Image.open(image)
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='JPEG')  # Выберите формат сохранения по необходимости

    # После этого, вы можете создать объект InMemoryUploadedFile
    img_file = InMemoryUploadedFile(
        img_byte_array,
        None,
        'image.jpg',  # Имя файла
        'image/jpeg',  # MIME-тип
        img_byte_array.tell(),
        None
    )
    return img_file

def description_parser(driver, link, start_range,stop_range, i_plus_required):
    description_dict = {}
    for i in range(start_range,stop_range):
        try:
            anime_info = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[@id='content']/div/div[1]/div[2]/div[3]/dl/dt[{i}]"))
                    )
                                            
            additional_info = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[@id='content']/div/div[1]/div[2]/div[3]/dl/dd[{ i+1 if i_plus_required else i}]"))
            )
        except(StaleElementReferenceException, TimeoutException, NoSuchElementException):
            break
        anime_info_text = anime_info.text
        additional_info_text = additional_info.text
        print(anime_info_text, "-", additional_info_text)
        description_dict[anime_info_text] = additional_info_text 
                    
            
    try:                  
        description = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[@id='content']/div/div[2]"))
            ).text
        
        description_dict["Описание"] = description
        print("Описание:", description)
    except:
        print("не удалось получить описание")
        traceback.print_exc()

    return description_dict


def parser(link):
        driver = webdriver.Firefox()
        driver.get(link)
        ongoing = False
        film = False
        data = {}
        if link == 'https://animego.org':
            return None
            # Получение даных для проверки типа аниме 
        try:
            name = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div/div[1]/div[2]/div[2]/div/h1"))
            ).text
            ongoing_check = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[1]/div[2]/div[3]/dl/dt[1]'))
                        ).text
            ani_type_check = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[1]/div[2]/div[3]/dl/dd[1]'))
                        ).text
            ani_type = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[1]/div[2]/div[3]/dl/dd[2]'))
                    ).text
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            traceback.print_exc()
            return None

        title = name 
            # Проверка на тип аниме в ссылке
        if ani_type == 'Фильм':
                film = True

        if ongoing_check != 'Следующий эпизод':
            if ani_type == '1':
                    film = True
            if ani_type_check == 'Фильм':
                    film = True
        else:
            ongoing = True
            
        if film:
            start_range = 1
            stop_range = 9
            i_plus_required = False
        elif ongoing:
            start_range = 2
            stop_range = 13
            i_plus_required = True  
        else:
            start_range = 1
            stop_range = 12
            i_plus_required = False

        image = image_parser(driver, link)
        data['Обложка'] = image
        description = description_parser(driver, link, start_range, stop_range, i_plus_required)
        
        
            
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()

        try:
            button18 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="video-player"]/div[1]/div/div[2]/button[2]'))
            )
            print("✔️18+ обнаружено")
            button18.click()
            print("✔️18+ пройдено")
        except:
            try:
                actions.send_keys(Keys.PAGE_DOWN).perform()
                button18 = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="video-player"]/div[1]/div/div[2]/button[2]'))
                )
                print("✔️18+ обнаружено")
                button18.click()
                print("✔️18+ пройдено")
            except:
                print("18+ не обнаружено")
        for i in range(5):
            actions.send_keys(Keys.PAGE_UP).perform()
            actions.send_keys(Keys.PAGE_UP).perform()
            actions.send_keys(Keys.PAGE_UP).perform()
        try:
            actions.send_keys(Keys.PAGE_DOWN).perform()
            player_select_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="video-players-tab"]'))
                    )
            player_select_btn.click()
        except:
            try:
                actions.send_keys(Keys.PAGE_DOWN).perform()
                player_select_btn = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="video-players-tab"]'))
                    )
                player_select_btn.click()
            except:
                print('Нету плеера')
                driver.quit()
                return None

        if film:
            anime = film_parser(driver, link)
            data['type'] = 'Film'
            
        else:
            anime = series_parser(driver, link, ongoing)
            data['type'] = 'Anime'
        
        if anime == None:
            return None
        else: 
            data['Название'] = title
            data['Характеристики'] = description
            data['Плеер'] = anime
            data['Обложка'] = image
        driver.quit()
        return data
        

print(links_parser('D:\.prog\lunime\main\links.txt'))

# # print(image_parser('https://animego.org/anime/monolog-farmacevta-2422'))
# print(animego_link_parser('https://animego.org/anime?sort=r.rating&direction=desc&type=animes&page='))
# data = {'Название': 'Мастера Меча Онлайн: Алисизация — Война в Подмирье 2', 'Характеристики': {'Тип': 'ТВ Сериал', 'Эпизоды': '11', 'Статус': 'Вышел', 'Жанр': 'Игры, Приключения, Романтика, Фэнтези, Экшен', 'Первоисточник': 'Легкая новвела', 'Сезон': 'Лето 2020', 'Выпуск': 'с 12 июля 2020 по 20 сентября 2020', 'Студия': 'A-1 Pictures Inc.', 'Рейтинг MPAA': 'NC-17', 'Возрастные ограничения': '18+', 'Длительность': '24 мин. ~ серия', 'Описание': 'Вторая часть аниме «Мастера Меча Онлайн: Алисизация — Война в Подмирье».\n\nЧтобы спасти Андерворлд, Кирито, Юджио, Алисе и всем их союзникам необходимо найти способ разбить армию Дарк Территори.'}, 'Плеер': {1: '//kodik.info/seria/685108/6a9808e89588cc54a7bf64d9fc7fa711/720p', 2: '//kodik.info/seria/689270/6d9aed56a45a3562ca589ce4368c3791/720p', 3: '//kodik.info/seria/693007/2f97934d4f239094eaab9a82a5c255f2/720p', 4: '//kodik.info/seria/697296/7a58d479f21b022adb876c5811da7e81/720p', 5: '//kodik.info/seria/702487/1ca76eecb5bb37f926dabf19be836e05/720p', 6: '//kodik.info/seria/705918/bb8efdf8ed944dc2454bee2daa4aa3e9/720p', 7: '//kodik.info/seria/710490/457a9de3d1a486fdc9d240a840c05db5/720p', 8: '//kodik.info/seria/715329/c8fcd45c51c7981e68586e5abf81f179/720p', 9: '//kodik.info/seria/717675/07ca3512dbbd4187d457cf787b8a2c85/720p', 10: '//kodik.info/seria/719141/a65f57d871ba374b29f00d060f979630/720p', 11: '//kodik.info/seria/720494/6c82aeeeb915677c1c7ed7b207fe77b0/720p'}}

# # # Преобразование вложенного словаря в основной словарь
# # print(data)
# title = data['Название']
# data_description = data['Характеристики']
# a_type = data_description['Тип']
# amount_of_episodes = data_description['Эпизоды']
# status = data_description['Статус']
# genres = data_description['Жанр'].split(', ')
# origin_sourse = data_description['Первоисточник']
# release = data_description['Выпуск']
# studio = data_description['Студия']
# duration = data_description['Длительность']
# description = data_description['Описание']
# print(description)

# for key, value in data['Плеер'].items():
#     print(key, value)
    
# for genre in genres:
#     print(genre)