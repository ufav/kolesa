from selenium import webdriver
import time

url = 'https://www.flashscore.ru/?rd=myscore.ru'
driver = webdriver.Chrome(executable_path="C:\\Users\\Admin\\PycharmProjects\\betpebet\\chromedriver\\chromedriver.exe")
driver.get(url)

elements = driver.find_elements_by_css_selector("div.tabs__tab")   #.get_attribute('innerHTML')
elements[1].click()


container = driver.find_element_by_css_selector("section[class=event]").get_attribute('innerHTML')


print(container)

#driver.close()
#driver.quit()