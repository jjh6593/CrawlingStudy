from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from durable.lang import *
import rule_set

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service_obj = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service_obj, options=chrome_options)

# 웹페이지 열기
driver.get("https://google.com")

# 'button', 'form', 'a' 태그 요소 찾기
buttons = driver.find_elements(By.TAG_NAME, 'button')
forms = driver.find_elements(By.TAG_NAME, 'form')
links = driver.find_elements(By.TAG_NAME, 'a')

# XPath 추출하는 자바스크립트 함수
script = """
    var getElementXPath = function(element) {
        if (element.id !== '') return 'id("' + element.id + '")';
        if (element === document.body) return element.tagName.toLowerCase();

        var ix = 0;
        var siblings = element.parentNode.childNodes;
        for (var i = 0; i < siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling === element) return getElementXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
        }
    };
    return getElementXPath(arguments[0]);
"""

# 결과 출력
print("Buttons:")
for button in buttons:
    xpath = driver.execute_script(script, button)
    print("XPath:", xpath)
    print("HTML:", button.get_attribute('outerHTML'))

print("\nForms:")
for form in forms:
    xpath = driver.execute_script(script, form)
    print("XPath:", xpath)
    print("HTML:", form.get_attribute('outerHTML'))

print("\nLinks:")
for link in links:
    xpath = driver.execute_script(script, link)
    print("XPath:", xpath)
    print("HTML:", link.get_attribute('outerHTML'))

driver.quit()