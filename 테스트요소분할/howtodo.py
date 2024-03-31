import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from durable.lang import *
import rule_set
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

from json_process import initialize_file, reset_indexes_in_json_file

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
#driver = webdriver.Chrome(service=service_obj, options=chrome_options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 웹페이지 열기
driver.get("https://rahulshettyacademy.com/angularpractice/")
#driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
# 페이지가 완전히 로드될 때까지 기다립니다.
def get_xpath(driver, element):
    script = """
    var getElementXPath = function(element) {
        if (element.id !== '') {
            return 'id("' + element.id + '")';
        }
        if (element === document.body) {
            return element.tagName.toLowerCase();
        }
        var ix = 0;
        var siblings = element.parentNode.childNodes;
        for (var i = 0; i < siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling === element) {
                return getElementXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
            }
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                ix++;
            }
        }
    };
    return getElementXPath(arguments[0]);
    """
    return driver.execute_script(script, element)


# input 요소들을 찾습니다.
inputs = driver.find_elements(By.TAG_NAME, 'input')

# Form 내부의 input 요소와 form의 XPath를 저장하는 리스트를 정의합니다.
form_inputs_with_xpath = []

# 각 input 요소에 대해 반복하면서 form 요소의 XPath를 찾습니다.
for element in inputs:
    try:
        # 상위 form 요소를 찾습니다.
        form_element = element.find_element(By.XPATH, ".//ancestor::form")
        # form 요소의 XPath를 가져옵니다.
        form_xpath = get_xpath(driver, form_element)
        # 리스트에 (input 요소, form의 XPath) 튜플을 추가합니다.
        form_inputs_with_xpath.append((element, form_xpath))
        print(f"Input Element: {element.get_attribute('outerHTML')}\nForm XPath: {form_xpath}\n")
    except NoSuchElementException:
        # form 요소가 없으면 무시합니다.
        continue

# 처리가 완료되면 드라이버를 종료합니다.
driver.quit()
