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
from .models import AdditionalImage, AdditionalFilmImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
import uuid

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
        file.close()
        

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
                    additional_images = link_data.get('Кадры', "0")
                    
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
                            
                            for image in additional_images:
                                image_to_save = AdditionalImage.objects.create(anime=new_anime, image=image_saver(image))
                                
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
                    additional_images = link_data.get('Кадры', "0")
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
                            
                            for image in additional_images:
                                image_to_save = AdditionalFilmImage.objects.create(film=new_film, image=image_saver(image))    
                                
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

    except Exception as e:
        print(f"Ошибка при выборе вкладки: {e}")
        traceback.print_exc()

    span_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    for num in span_lst:
        try:
            player_link = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="video-players"]/span[{num}]'))
            )
            src_check = link_check(player_link, driver)
            if src_check:
                break

        except (StaleElementReferenceException, TimeoutException, NoSuchElementException):
            continue

    if src_check:
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
    actions = ActionChains(driver)

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
            except Exception:
                player_select_btn_locator = (By.XPATH, '//*[@id="video-players-tab"]')
                player_select_btn = WebDriverWait(carousel, 5).until(
                    EC.presence_of_element_located(player_select_btn_locator)
                )
                player_select_btn.click()

            player_select_btn.click()
            try:
                span_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for num in span_lst:
                    try:
                        player_link = WebDriverWait(driver, 3).until(
                            EC.visibility_of_element_located((By.XPATH, f'//*[@id="video-players"]/span[{num}]'))
                        )
                        src_check = link_check(player_link, driver)
                        if src_check:
                            break
                    except (StaleElementReferenceException, TimeoutException, NoSuchElementException):
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
                print(f'{counter} - ' + episode)
                episodes_dict[counter] = episode
            else:
                print("❌ Нету ссылки кодика, аниме не добавится в базу")
                return None

        print(f'✔️   {link.strip()}: парсинг пройден')
        print("Полученное количество серий:", counter, '\n')
        return episodes_dict

    except StaleElementReferenceException as stale_error:
        print(f"Произошла ошибка StaleElementReferenceException: {stale_error}")

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

def image_parser(driver, xpath):
    try:
        # Используем XPath для получения ссылки на изображение из атрибута srcset
        image = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/img'))
                    )

        
        image_url = image.get_attribute('srcset').split(' ')[0]
        # Используем библиотеку requests для загрузки изображения
        response = requests.get(image_url)
        # Проверяем успешность запроса
        if response.status_code == 200:
            # Получаем байт-код изображения
            image_bytes = BytesIO(response.content)
            return image_bytes
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def additional_images_parser(driver):
    try:
        image1 = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="screenshots-list"]/a[1]'))
                ).get_attribute('href')
        print("Получен 1 кадр (1)")
        image2 = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="screenshots-list"]/a[2]'))
                        ).get_attribute('href')
        print("Получен 2 кадр (1)")
        image3 = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="screenshots-list"]/a[3]'))
                        ).get_attribute('href')
        print("Получен 3 кадр (1)")
    except:
        try:
            image1 = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="screenshots-list"]/a[1]'))
                ).get_attribute('href')
            print("Получен 1 кадр (2)")
            image2 = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, f'//*[@id="screenshots-list"]/a[2]'))
                            ).get_attribute('href')
            print("Получен 2 кадр (2)")
            image3 = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, f'//*[@id="screenshots-list"]/a[3]'))
                            ).get_attribute('href')
            print("Получен 3 кадр (2)")
        except:
            print("Кадры аниме не найдены")
            return None
        
    converted = []
    unconverted = [image1, image2, image3]
        
    for image_url in unconverted:
        response = requests.get(image_url)
        print("Ответ получен")

        # Проверяем успешность запроса
        if response.status_code == 200:
            print("Ответ получен")
            image_bytes = BytesIO(response.content)
            converted.append(image_bytes)
            print("Байт-код получен и добавлен в список")
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
            return None
    print("Возвращаем байт-коды кадров")
    return converted
        

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

def additional_names_parser(driver):
    
    lst = []
    for i in range(1, 4):
        try:
            name = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[1]/div[2]/div[2]/div/div/div[1]/ul/li[{i}]'))
                    ).text
            lst.append(name)
        except:
            break
    return lst if lst else None
    
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

    if ani_type == 'Фильм':
        film = True

    if ongoing_check != 'Следующий эпизод':
        if ani_type == '1':
            film = True
        if ani_type_check == 'Фильм':
            film = True
    else:
        ongoing = True

    start_range, stop_range, i_plus_required = (
        (1, 9, False) if film else (2, 13, True) if ongoing else (1, 12, False)
    )

    data['Обложка'] = image_parser(driver, link)
    data['Кадры'] = additional_images_parser(driver)
    data['Другие названия'] = additional_names_parser(driver)
    description = description_parser(driver, link, start_range, stop_range, i_plus_required)

    actions = ActionChains(driver)
    for _ in range(5):
        actions.send_keys(Keys.PAGE_UP).perform()

    try:
        actions.send_keys(Keys.PAGE_DOWN).perform()
        button18 = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="video-player"]/div[1]/div/div[2]/button[2]'))
        )
        print("✔️18+ обнаружено")
        button18.click()
        print("✔️18+ пройдено")
    except Exception:
        print("18+ не обнаружено")

    for _ in range(3):
        actions.send_keys(Keys.PAGE_UP).perform()

    try:
        actions.send_keys(Keys.PAGE_DOWN).perform()
        player_select_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="video-players-tab"]'))
        )
        player_select_btn.click()
    except Exception:
        print('Нету плеера')
        driver.quit()
        return None

    if film:
        anime = film_parser(driver, link)
        data['type'] = 'Film'
    else:
        anime = series_parser(driver, link, ongoing)
        data['type'] = 'Anime'

    if anime is None:
        return None
    else:
        data['Название'] = title
        data['Характеристики'] = description
        data['Плеер'] = anime

    driver.quit()
    return data
    

print(links_parser('D:\.prog\lunime-repo\lunime-\main\links.txt'))
# print(animego_link_parser('https://animego.org/anime?sort=r.rating&direction=desc&type=animes&page='))