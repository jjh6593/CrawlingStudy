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
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# 웹페이지 열기
driver.get("https://rahulshettyacademy.com/angularpractice/")
#driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
# 페이지가 완전히 로드될 때까지 기다립니다.
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'div')))

# 'div' 태그 요소 찾기
divs = driver.find_elements(By.TAG_NAME,'div')
sent_facts = set()

# 'button', 'form', 'a' 태그 요소 찾기
buttons = driver.find_elements(By.TAG_NAME, 'button')
forms = driver.find_elements(By.TAG_NAME, 'form')
links = driver.find_elements(By.TAG_NAME, 'a')

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
selects = driver.find_elements(By.TAG_NAME, 'select')
textareas = driver.find_elements(By.TAG_NAME, 'textarea')

# Form과 연결되지 않은 요소만 추출
independent_selects = []

for element in selects:
    try:
        element.find_element(By.XPATH, "./ancestor::form")
    except NoSuchElementException:
        independent_selects.append(element)

initialize_file('select_data.json')
initialize_file('reset_index_select_data.json')
# for index, select in enumerate(independent_selects,start = 1):
for index, select in enumerate(independent_selects,start = 1):
    try:
        outerHTML = select.get_attribute('outerHTML')
        soup = BeautifulSoup(outerHTML, 'html.parser')
        text = soup.text.strip()
        select_element = soup.find('select')

        select_id = select_element.get('id')

        if select_id:
            xpath = f"//select[@id='{select_id}']"
        else:
            xpath = driver.execute_script(script, select)

        select_name = select_element.get('name')
        select_disabled = 'disabled' if select_element.has_attr('disabled') else 'enabled'
        select_required = 'required' if select_element.has_attr('required') else 'not required'
        # HTML 표준에 따른 기본값을 사용합니다.
        multiple = 'true' if select_element.has_attr('multiple') else 'false'
        autofocus = 'true' if select_element.has_attr('autofocus') else 'false'
        form_id = select_element.get('form', 'None')
        current_fact = str({
            'tag': 'select',
            'index': index,
            'id': select_id,
            'xPath': xpath,
            'name': select_name,
            'multiple': multiple,
            'autofocus': autofocus,
            'disabled': select_disabled,
            'required': select_required,
            'form_': form_id
        })

        if current_fact not in sent_facts:
            assert_fact('web_test', eval(current_fact))
            sent_facts.add(current_fact)
    except NoSuchElementException:
        print(f"NoSuchElementException 발생, index: {index}. 요소가 없으므로 무시하고 다음으로 넘어감.")
        continue
    except StaleElementReferenceException:
        print(f"StaleElementReferenceException 발생, index: {index}. 요소 무시하고 다음으로 넘어감.")
        continue
    except Exception as e:
        print(f"오류 발생: {e}")
        continue

#브라우저 닫기
driver.quit()
# 처리된 데이터 확인
# 예: 파일에서 처리된 데이터를 읽어 출력
with open('select_data.json', 'r') as file:
    for line in file:
        print(json.loads(line))
# 함수를 호출하여 index를 재설정하고 결과를 저장합니다.
reset_indexes_in_json_file('select_data.json', 'reset_index_select_data.json')
# 예: 파일에서 처리된 데이터를 읽어 출력
with open('reset_index_select_data.json', 'r') as file:
    for line in file:
        print(json.loads(line))