from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import json
from urllib.parse import unquote
import re


def get_data():
    start_time = time.time()

    ################################# regions list
    try:
        url = 'https://kolesa.kz/'
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        regions = soup.find_all('div', class_='block-links-list row')[-1]
        regions = regions.find_all('a')
        regions_list = []
        for tag in regions:
            regions_list.append(re.search('\/cars\/(.*)\/', tag['href']).group(1))
        print(regions_list)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

    ################################# cars list
    try:
        url = 'https://kolesa.kz/cars' #+ '/region-abaiskaya-oblast' #regions_list[0]
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
        for car in cars_list:
            print(car)
            ################################# pages count
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
                        price = unquote(price)
                        description = add.find('p', class_='a-card__description').text.strip()
                        city = add.find('span', class_='a-card__param').text.strip()
                        date_add = add.find('span', class_='a-card__param a-card__param--date').text.strip()
                        views = add.find('span', class_='a-card__views nb-views').text.strip()
                        result_list.append(
                            {
                                'date_load': time.time(),
                                'name': vehicle_name,
                                'price': price,
                                'description': description,
                                'region': region,
                                'city': city,
                                'date_add': date_add,
                                'views': views
                            }
                        )
                    #print(result_list)
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


def test1():
    result_list = []

    ################################# pages count
    try:
        pages_list = ['']
        url = 'https://kolesa.kz/cars/' + 'jeep/region-abaiskaya-oblast'
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if str(soup).find('Объявлений не найдено') > 0:
            print('Объявлений не найдено')
        if str(soup).find('<div class="pager"') > 0:
            print('Больше одной страницы')
            pages_count = int(soup.find('div', class_='pager').find_all('a')[-2].text)
            print(pages_count)
            for p in range(2, pages_count + 1):
                pages_list.append('/?page=' + str(p))
        else:
            print('Одна страница')
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

    count = 1
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        for page in pages_list:
            url = 'https://kolesa.kz/cars/' + 'jeep/region-abaiskaya-oblast' + page
            driver.get(url)
            time.sleep(random.randrange(2, 5))
            if count % 10 == 0:
                time.sleep(random.randrange(5, 9))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            adds_div = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['a-list__item'])
            for add in adds_div:
                vehicle_name = add.find('h5', class_='a-card__title').text.strip()
                price = add.find('span', class_='a-card__price').text.strip()
                price = unquote(price)
                description = add.find('p', class_='a-card__description').text.strip()
                city = add.find('span', class_='a-card__param').text.strip()
                date_add = add.find('span', class_='a-card__param a-card__param--date').text.strip()
                views = add.find('span', class_='a-card__views nb-views').text.strip()
                result_list.append(
                    {
                        'date_load': time.time(),
                        'name': vehicle_name,
                        'price': price,
                        'description': description,
                        'region': region,
                        'city': city,
                        'date_add': date_add,
                        'views': views
                    }
                )
            print(result_list)
            #print(f'[+] Processed: {round(count / pages_count * 100, 2)}')
            count += 1
    except:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def test2():
    pages = ['']
    pages_count = 8
    for page in range(2, pages_count):
        pages.append('/?page=' + str(page))
    print(pages)


def test3():
    st = '<div class="pager">'
    if st.find('paer') > 0:
        print('Yes')
    else:
        print('No')


def main():
    get_data()
    #test1()
    #test2()
    #test3()


if __name__ == '__main__':
    main()


