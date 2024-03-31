from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
driver = webdriver.Chrome(service=service_obj, options=chrome_options)
driver.get("https://rahulshettyacademy.com/dropdownsPractise/")

driver.find_element(By.ID,"autosuggest").send_keys("ind")
time.sleep(2)

countries = driver.find_elements(By.CSS_SELECTOR, "li[class='ui-menu-item'] a")
print(len(countries))

# 클릭하고 반복문 탈출해야함
for country in countries:
    if country.text == "India":
        country.click()
        break
# print(driver.find_element(By.ID, "autosuggest").text)
# 텍스트 아리아에 적혀있는 내용을 동적으로 가져오는 방법은 get_attribute("value")
assert print(driver.find_element(By.ID, "autosuggest")).get_attribute("value") == "india"
