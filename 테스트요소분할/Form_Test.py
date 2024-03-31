import json

from selenium.common import StaleElementReferenceException, NoSuchElementException
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
driver.get("https://naver.com")

# 'button', 'form', 'a' 태그 요소 찾기
buttons = driver.find_elements(By.TAG_NAME, 'button')
forms = driver.find_elements(By.TAG_NAME, 'form')
links = driver.find_elements(By.TAG_NAME, 'a')


script = """
    var getElementXPath = function(element) {
        // id를 우선적으로 사용
        if (element.id !== '') {
            return "//" + element.tagName.toLowerCase() + "[@id='" + element.id + "']";
        }

        // 다른 속성을 이용한 XPath 생성
        var attributes = element.attributes;
        var attributeXPath = '';
        for (var i = 0; i < attributes.length; i++) {
            var attr = attributes[i];
            if (attr.name !== 'id' && attr.name !== 'class') {
                attributeXPath += "[@" + attr.name + "='" + attr.value + "']";
            }
        }
        if (attributeXPath !== '') {
            return "//" + element.tagName.toLowerCase() + attributeXPath;
        }

        // 상대 경로에 기반한 XPath 생성
        var ix = 0, siblings = element.parentNode.childNodes;
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
for index, form in enumerate(forms, start = 1):
    try:

        # form 요소의 outerHTML을 가져오기
        outerHTML = form.get_attribute('outerHTML')
        soup = BeautifulSoup(outerHTML, 'html.parser')
        form_id = form.get_attribute('id')
        form_class = form.get_attribute('class')

        if form_id:
            xpath = f"//form[@id='{form_id}']"

        else:
            xpath = driver.execute_script(script, form)

        action = form.get_attribute('action')
        name = form.get_attribute('name')
        target = form.get_attribute('target')
        aria_label = form.get_attribute('aria-label')
        role = form.get_attribute('role')

        # 폼 내부의 input, select, textarea 요소 추출
        inputs = [input_el.get_attribute('outerHTML') for input_el in form.find_elements(By.TAG_NAME, 'input')]
        selects = [select_el.get_attribute('outerHTML') for select_el in form.find_elements(By.TAG_NAME, 'select')]
        textareas = [textarea_el.get_attribute('outerHTML') for textarea_el in
                     form.find_elements(By.TAG_NAME, 'textarea')]
        if target == '':
            target = '_self'
        assert_fact('web_test', {
            'tag': 'form',
            'index': index,
            'action': action,
            'role': role,
            'name': name,
            'target': target,
            'xPath': xpath,
            'aria-label': aria_label,
            'inputs': inputs,
            'selects': selects,
            'textareas': textareas
        })
    except NoSuchElementException:
        print(f"NoSuchElementException 발생, index: {index}. 요소가 없으므로 무시하고 다음으로 넘어감.")
        continue
    except StaleElementReferenceException:
        print(f"StaleElementReferenceException 발생, index: {index}. 요소 무시하고 다음으로 넘어감.")
        # StaleElementReferenceException이 발생하면 현재 요소를 무시하고 다음 요소로 넘어감
        continue
    except Exception as e:
        print(f"오류 발생: {e}")
        continue










# 브라우저 닫기
driver.quit()
# 처리된 데이터 확인
# 예: 파일에서 처리된 데이터를 읽어 출력
with open('processed_data.json', 'r') as file:
    for line in file:
        print(json.loads(line))