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
    try:
        url = 'https://kolesa.kz/cars/' + cars_list[0] + '/' + regions_list[0]
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pages_count = int(soup.find('div', class_='pager').find_all('a')[-2].text)
        print(pages_count)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()
    result_list = []
    count = 1
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        for page in range(1, pages_count):
            url = 'https://kolesa.kz/cars/' + cars_list[0] + '/' + regions_list[0] + '/?page=' + str(page)
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
                #region = add.find('div', class_='a-card__data').text.strip()
                date = add.find('span', class_='a-card__param a-card__param--date').text.strip()
                views = add.find('span', class_='a-card__views nb-views').text.strip()
                result_list.append(
                    {
                        'name': vehicle_name,
                        'price': price,
                        'description': description,
                        'date': date,
                        'views': views
                    }
                )
            print(result_list)
            print(f'[+] Processed: {round(count / pages_count * 100, 2)}')
            count += 1
    except:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def test():
    result_list = []
    count = 1
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        for page in range(2, 3):
            url = 'https://kolesa.kz/cars/audi/region-abaiskaya-oblast/' + '/?page=' + str(page)
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
                #region = add.find('div', class_='a-card__data').text.strip()
                date = add.find('span', class_='a-card__param a-card__param--date').text.strip()
                views = add.find('span', class_='a-card__views nb-views').text.strip()
                result_list.append(
                    {
                        'name': vehicle_name,
                        'price': price,
                        'description': description,
                        'date': date,
                        'views': views
                    }
                )
            print(result_list)
            print(f'[+] Processed: {round(count / 3 * 100, 2)}')
            count += 1
    except:
        pass
    finally:
        driver.close()
        driver.quit()


def main():
    #get_data()
    test()


if __name__ == '__main__':
    main()


