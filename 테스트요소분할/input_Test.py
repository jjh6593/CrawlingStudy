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
driver = webdriver.Chrome(service=service_obj, options=chrome_options)
# 웹페이지 열기
driver.get("https://rahulshettyacademy.com/angularpractice/")
#driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
# 페이지가 완전히 로드될 때까지 기다립니다.
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'div')))

# 'div' 태그 요소 찾기
divs = driver.find_elements(By.TAG_NAME,'div')
sent_facts = set()

# 'button', 'form', 'a' 태그 요소 찾기
buttons = driver.find_elements(By.TAG_NAME, 'button')
forms = driver.find_elements(By.TAG_NAME, 'form')
links = driver.find_elements(By.TAG_NAME, 'a')
# 'input', 'select', 'textarea' 태그 요소 찾기
inputs = driver.find_elements(By.TAG_NAME, 'input')
# XPath 추출하는 자바스크립트 함수

script = """
    var getElementXPath = function(element) {
        if (!element || !element.tagName) return ''; // element 또는 tagName이 없는 경우 빈 문자열 반환
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

# 'input', 'select', 'textarea' 태그 요소 찾기
# selects = driver.find_elements(By.TAG_NAME, 'select')
# textareas = driver.find_elements(By.TAG_NAME, 'textarea')

# Form과 연결되지 않은 요소만 추출
#independent_inputs = []

# for element in inputs:
#     try:
#         element.find_element(By.XPATH, "./ancestor::form")
#     except NoSuchElementException:
#         independent_inputs.append(element.get_attribute('outerHTML'))

initialize_file()
for index, input in enumerate(inputs,start = 1):
    try:
        outerHTML = input.get_attribute('outerHTML')

        # input 요소의 outerHTML을 가져와 BeautifulSoup 객체 생성
        soup = BeautifulSoup(input.get_attribute('outerHTML'), 'html.parser')
        text = soup.text.strip()
        input_element = soup.find('input')  # div 요소를 찾습니다.

        # id 속성이 있는지 확인
        input_id = input_element.get('id')

        # class 속성이 있는지 확인
        input_class = input_element.get('class')
        class_value = input_class[0] if input_class else None  # 클래스가 없는 경우 None으로 설정

        # id, class 또는 다른 속성에 따라 적절한 XPath 생성
        if input_id:
            # id 속성이 있는 경우
            input_xpath = f"//input[@id='{input_id}']"

        else:
            # id와 class 모두 없는 경우, JavaScript 함수를 사용해 XPath 생성
            input_xpath = driver.execute_script(script, input)

        # 각 속성을 가져오기
        input_type = soup.get('type')
        input_name = input_element.get('name')
        input_value = input_element.get('value')

        input_placeholder = input_element.get('placeholder')
        input_disabled = 'disabled' if input_element.has_attr('disabled') else 'enabled'
        input_required = 'required' if input_element.has_attr('required') else 'not required'

        current_fact = str({
            'tag': 'input',
            'index': index,
            'id': input_id,
            'class_': class_value,
            'xPath': input_xpath,
            'name': input_name,
            'value': input_value,
            'placeholder': input_placeholder,
            'disabled': input_disabled,
            'required': input_required
        })

        # 현재 fact가 이전에 보낸 적 없는 경우에만 assert_fact 실행
        if current_fact not in sent_facts:
            assert_fact('web_test', eval(current_fact))
            sent_facts.add(current_fact)
    except Exception as e:
        print(f"오류 발생: {e}")
        continue
with open('processed_data.json', 'r') as file:
    for line in file:
        print(json.loads(line))

# 함수를 호출하여 index를 재설정하고 결과를 저장합니다.
reset_indexes_in_json_file('processed_data.json', 'reset_index_data.json')
# # 예: 파일에서 처리된 데이터를 읽어 출력
# with open('reset_index_data.json', 'r') as file:
#     for line in file:
#         print(json.loads(line))
# # 예: 파일에서 처리된 데이터를 읽어 출력
# with open('reset_index_data.json', 'r') as file:
#     for line in file:
#         print(json.loads(line))
# for index, textarea in enumerate(independent_textareas,start=1):
#     try:
#         soup = BeautifulSoup(textarea, 'html.parser')
#         textarea_element = soup.find('textarea')
#
#         textarea_id = textarea_element.get('id')
#         textarea_class = textarea_element.get('class')
#         class_value = " ".join(textarea_class) if textarea_class else None
#
#         textarea_xpath = f"//textarea[@id='{textarea_id}']" if textarea_id else driver.execute_script(script, textarea)
#
#         textarea_name = textarea_element.get('name')
#         textarea_disabled = 'disabled' if textarea_element.has_attr('disabled') else 'enabled'
#         textarea_required = 'required' if textarea_element.has_attr('required') else 'not required'
#
#         current_fact = str({
#             'tag': 'textarea',
#             'id': textarea_id,
#             'class_': class_value,
#             'xPath': textarea_xpath,
#             'name': textarea_name,
#             'disabled': textarea_disabled,
#             'required': textarea_required
#         })
#
#         if current_fact not in sent_facts:
#             assert_fact('web_test', eval(current_fact))
#             sent_facts.add(current_fact)
#     except NoSuchElementException:
#         print(f"NoSuchElementException 발생, index: {index}. 요소가 없으므로 무시하고 다음으로 넘어감.")
#         continue
#     except StaleElementReferenceException:
#         print(f"StaleElementReferenceException 발생, index: {index}. 요소 무시하고 다음으로 넘어감.")
#         # StaleElementReferenceException이 발생하면 현재 요소를 무시하고 다음 요소로 넘어감
#         continue
#     except Exception as e:
#         print(f"오류 발생: {e}, index: {index}")
#         continue

#브라우저 닫기
driver.quit()
# 처리된 데이터 확인
# 예: 파일에서 처리된 데이터를 읽어 출력
with open('processed_data.json', 'r') as file:
    for line in file:
        print(json.loads(line))
# 함수를 호출하여 index를 재설정하고 결과를 저장합니다.
reset_indexes_in_json_file('processed_data.json', 'reset_index_data.json')
# 예: 파일에서 처리된 데이터를 읽어 출력
with open('reset_index_data.json', 'r') as file:
    for line in file:
        print(json.loads(line))