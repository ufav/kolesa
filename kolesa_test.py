from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import json
from urllib.parse import unquote
import re


def get_data():
    start_time = time.time()

    ################################# regions list
    regions_list_ex = ['/region-abaiskaya-oblast', '/region-almatinskaya-oblast', '/region-yuzhnokazahstanskaya-oblast']

    ################################# cars list
    try:
        url = 'https://kolesa.kz/cars'  # + '/region-abaiskaya-oblast' #regions_list[0]
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cars = soup.find_all('div', class_='cross-links show-all js__show-all')[0]
        cars = cars.find_all('a')
        cars_list = []
        for tag in cars:
            cars_list.append(re.search('\/cars\/(.*)\/', tag['href']).group(1))
        print(cars_list)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

    result_list = []
    count = 1
    for region in regions_list:
        if region == '/region-almatinskaya-oblast' or region == '/region-yuzhnokazahstanskaya-oblast' or region == '/region-akmolinskaya-oblast':
            for car in cars_list:
                print(car)
                try:
                    pages_list = ['']
                    url = 'https://kolesa.kz/cars/' + car + '/' + region
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                    driver.get(url)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    if str(soup).find('Объявлений не найдено') > 0:
                        continue
                    if str(soup).find('<div class="pager"') > 0:
                        pages_count = int(soup.find('div', class_='pager').find_all('a')[-2].text)
                        print(pages_count)
                        for p in range(2, pages_count + 1):
                            pages_list.append('/?page=' + str(p))
                except Exception as _ex:
                    print(_ex)
                finally:
                    driver.close()
                    driver.quit()

                try:
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                    for page in pages_list:
                        url = 'https://kolesa.kz/cars/' + car + '/' + region + page
                        driver.get(url)
                        time.sleep(random.randrange(2, 5))
                        if count % 10 == 0:
                            time.sleep(random.randrange(5, 9))
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        adds_div = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['a-list__item'])
                        for add in adds_div:
                            vehicle_name = add.find('h5', class_='a-card__title').text.strip()
                            price = add.find('span', class_='a-card__price').text.strip()
                            price = unquote(price).replace('\xa0', '').replace('₸', '').strip()
                            description = add.find('p', class_='a-card__description').text.strip()
                            manufacture_year = description.split(',')[0].replace('г.', '').strip()
                            body = description.split(',')[1].strip()
                            engine = description.split(',')[2].replace('л', '').strip()
                            try:
                                wheel = re.search('[^,]*руль[^,]*', description).group(0).strip()
                            except:
                                wheel = ''
                            try:
                                transmission = re.search('[^,]*КПП[^,]*', description).group(0).strip()
                            except:
                                transmission = ''
                            city = add.find('span', class_='a-card__param').text.strip()
                            date_add = add.find('span', class_='a-card__param a-card__param--date').text.strip()
                            views = add.find('span', class_='a-card__views nb-views').text.strip()
                            imgs = add.find_all('img')
                            uniq_id = imgs[0]['src']
                            url = 'https://kolesa.kz' + \
                                  add.find('div', class_='a-card__picture').find('a', class_='a-card__link')['href']
                            result_list.append(
                                {
                                    'date_load': time.time(),
                                    'name': vehicle_name,
                                    'price': price,
                                    'description': description,
                                    'city': city,
                                    'date_add': date_add,
                                    'views': views,
                                    'manufacture_year': manufacture_year,
                                    'body': body,
                                    'engine': engine,
                                    'wheel': wheel,
                                    'transmission': transmission,
                                    'uniq_id': uniq_id,
                                    'url': url
                                }
                            )
                        # print(result_list)
                    print(f'[+] Processed: {round(count / len(cars_list) * 100, 2)}')
                    count += 1
                except:
                    print(_ex)
                finally:
                    driver.close()
                    driver.quit()
        else:
            try:
                pages_list = ['']
                url = 'https://kolesa.kz/cars/' + car + '/' + region
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if str(soup).find('<div class="pager"') > 0:
                    pages_count = int(soup.find('div', class_='pager').find_all('a')[-2].text)
                    print(pages_count)
                    for p in range(2, pages_count + 1):
                        pages_list.append('/?page=' + str(p))
            except Exception as _ex:
                print(_ex)
            finally:
                driver.close()
                driver.quit()

            try:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                for page in pages_list:
                    url = 'https://kolesa.kz/cars/' + car + '/' + region + page
                    driver.get(url)
                    time.sleep(random.randrange(2, 5))
                    if count % 10 == 0:
                        time.sleep(random.randrange(5, 9))
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    adds_div = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['a-list__item'])
                    for add in adds_div:
                        vehicle_name = add.find('h5', class_='a-card__title').text.strip()
                        price = add.find('span', class_='a-card__price').text.strip()
                        price = unquote(price).replace('\xa0', '').replace('₸', '').strip()
                        description = add.find('p', class_='a-card__description').text.strip()
                        manufacture_year = description.split(',')[0].replace('г.', '').strip()
                        body = description.split(',')[1].strip()
                        engine = description.split(',')[2].replace('л', '').strip()
                        try:
                            wheel = re.search('[^,]*руль[^,]*', description).group(0).strip()
                        except:
                            wheel = ''
                        try:
                            transmission = re.search('[^,]*КПП[^,]*', description).group(0).strip()
                        except:
                            transmission = ''
                        city = add.find('span', class_='a-card__param').text.strip()
                        date_add = add.find('span', class_='a-card__param a-card__param--date').text.strip()
                        views = add.find('span', class_='a-card__views nb-views').text.strip()
                        imgs = add.find_all('img')
                        uniq_id = imgs[0]['src']
                        url = 'https://kolesa.kz' + \
                              add.find('div', class_='a-card__picture').find('a', class_='a-card__link')['href']
                        result_list.append(
                            {
                                'date_load': time.time(),
                                'name': vehicle_name,
                                'price': price,
                                'description': description,
                                'city': city,
                                'date_add': date_add,
                                'views': views,
                                'manufacture_year': manufacture_year,
                                'body': body,
                                'engine': engine,
                                'wheel': wheel,
                                'transmission': transmission,
                                'uniq_id': uniq_id,
                                'url': url
                            }
                        )
                    # print(result_list)
                print(f'[+] Processed: {round(count / len(cars_list) * 100, 2)}')
                count += 1
            except:
                print(_ex)
            finally:
                driver.close()
                driver.quit()


    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
    print(round((time.time() - start_time) / 60, 2))
    return '[INFO] Data collected successfully'


def main():
    get_data()


if __name__ == '__main__':
    main()

