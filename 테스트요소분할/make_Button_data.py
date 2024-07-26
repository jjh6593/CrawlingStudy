from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from durable.lang import *
import json
from json_process import initialize_file, reset_indexes_in_json_file
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


import rule_set
sent_facts = set()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
#service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
#driver = webdriver.Chrome(service=service_obj, options=chrome_options)
#service = Service(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome()
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
# driver = webdriver.Chrome(service=service_obj, options=chrome_options)
# 웹페이지 열기
driver.get("https://www.daum.net/")
#driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
# 'button', 'form', 'a' 태그 요소 찾기
buttons = driver.find_elements(By.TAG_NAME, 'button')
forms = driver.find_elements(By.TAG_NAME, 'form')
links = driver.find_elements(By.TAG_NAME, 'a')
sent_facts = set()
# XPath 추출하는 자바스크립트 함수
script = """
    var getElementXPath = function(element) {
        // id를 우선적으로 사용
        if (element.id !== '') {
            return "//" + element.tagName.toLowerCase() + "[@id='" + element.id + "']";
        }

        // class를 이용한 XPath 생성
        if (element.className !== '') {
            var classes = element.className.trim().split(/\\s+/).join('.');
            return "//" + element.tagName.toLowerCase() + "[contains(@class, '" + classes + "')]";
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
initialize_file('button_data.json')
initialize_file('reset_button_data.json')
for index, button in enumerate(buttons,start=1):
    try:

        # button 요소의 outerHTML을 가져오기
        outerHTML = button.get_attribute('outerHTML')
        soup = BeautifulSoup(outerHTML, 'html.parser')
        button_element = soup.find('button')
        button_id = button_element.get('id')
        button_class = button_element.get('class')

        if button_id:
            xpath = f"//button[@id='{button_id}']"
        else:
            xpath = driver.execute_script(script, button)

        # 각 속성을 가져오기
        button_type = button.get_attribute('type')
        disabled = button.get_attribute('disabled')
        value = button.get_attribute('value')
        name = button.get_attribute('name')
        form = button.get_attribute('form')
        role = button.get_attribute('role')
        text = button_element.text.strip()
        current_fact = str({
            'tag': 'button',
            'index':index,
            'text': text,
            'xPath': xpath,
            'id': button_id,
            'type': button_type,
            'disabled': disabled,
            'value': value,
            'name': name,
            'btn_form': form,
            'role': role
        })

        # 현재 fact가 이전에 보낸 적 없는 경우에만 assert_fact 실행
        if current_fact not in sent_facts:
            assert_fact('web_test', eval(current_fact))
            sent_facts.add(current_fact)
    except NoSuchElementException:
        print(f"NoSuchElementException 발생, index: {index}. 요소가 없으므로 무시하고 다음으로 넘어감.")
        continue
    except StaleElementReferenceException:
        print(f"StaleElementReferenceException 발생, index: {index}. 요소 무시하고 다음으로 넘어감.")
        # StaleElementReferenceException이 발생하면 현재 요소를 무시하고 다음 요소로 넘어감
        continue
    except Exception as e:
        print(f"오류 발생: {e}, index: {index}")
        continue


# 브라우저 닫기
driver.quit()
# 처리된 데이터 확인
# 예: 파일에서 처리된 데이터를 읽어 출력
with open('button_data.json', 'r') as file:
    for line in file:
        print(json.loads(line))

# 함수를 호출하여 index를 재설정하고 결과를 저장합니다.
reset_indexes_in_json_file('button_data.json', 'reset_button_data.json')
# 예: 파일에서 처리된 데이터를 읽어 출력
with open('reset_button_data.json', 'r') as file:
    for line in file:
        print(json.loads(line))