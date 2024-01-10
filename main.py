from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from durable.lang import *
import rule_set

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
driver = webdriver.Chrome(service=service_obj, options=chrome_options)
# 웹페이지 열기
driver.get("https://www.naver.com")

# 'button', 'form', 'a' 태그 요소 찾기
buttons = driver.find_elements(By.TAG_NAME, 'button')
forms = driver.find_elements(By.TAG_NAME, 'form')
links = driver.find_elements(By.TAG_NAME, 'a')

# 결과 출력
print("Buttons:")
for button in buttons:
    print(button.get_attribute('outerHTML'))

print("\nForms:")
for form in forms:
    print(form.get_attribute('outerHTML'))

print("\nLinks:")
for link in links:
    print(link.get_attribute('outerHTML'))
# 추출된 요소에 대한 assert_fact
for button in buttons:
    soup = BeautifulSoup(button.get_attribute('outerHTML'), 'html.parser')
    text = soup.text.strip()
    assert_fact('web_test', {'tag': 'button', 'text': text})
for form in forms:
    soup = BeautifulSoup(form.get_attribute('outerHTML'), 'html.parser')
    action = soup.form.get('action')
    assert_fact('web_test', {'tag': 'form', 'action': action})

for link in links:
    href = link.get_attribute('href')
    assert_fact('web_test', {'tag': 'a', 'href': href})
# 브라우저 닫기
driver.quit()