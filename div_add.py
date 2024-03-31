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
from main import initialize_file

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
driver = webdriver.Chrome(service=service_obj, options=chrome_options)

# 웹페이지 열기
driver.get("https://www.naver.com")

# 페이지가 완전히 로드될 때까지 기다립니다.
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'div')))

# 'button', 'form', 'a' 태그 요소 찾기
divs = driver.find_elements(By.TAG_NAME,'div')
sent_facts = set()

# XPath 추출하는 자바스크립트 함수
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

# 추출된 요소에 대한 assert_fact
initialize_file()
for index,div in enumerate(divs,start=1):
    try:
        try:
            # div 요소의 outerHTML을 가져오기
            outerHTML = div.get_attribute('outerHTML')
        except StaleElementReferenceException:
            # StaleElementReferenceException이 발생하면 현재 요소를 무시하고 다음 요소로 넘어감
            continue
        # div 요소의 outerHTML을 가져와 BeautifulSoup 객체 생성
        soup = BeautifulSoup(div.get_attribute('outerHTML'), 'html.parser')
        text = soup.text.strip()
        div_element = soup.find('div')  # div 요소를 찾습니다.

        # id 속성이 있는지 확인
        div_id = div_element.get('id')

        # class 속성이 있는지 확인
        div_class = div_element.get('class')
        class_value = div_class[0] if div_class else None  # 클래스가 없는 경우 None으로 설정

        # id, class 또는 다른 속성에 따라 적절한 XPath 생성
        if div_id:
            xpath = f"//div[@id='{div_id}']"

        else:
            # id와 class 모두 없는 경우, JavaScript 함수를 사용해 XPath 생성
            xpath = driver.execute_script(script, div)

        # 각 속성을 가져오기
        contenteditable = div.get_attribute('contenteditable')
        role = div.get_attribute('role')
        draggable = div.get_attribute('draggable')
        tabindex = div.get_attribute('tabindex')
        hidden = div.get_attribute('hidden')
        title = div.get_attribute('title')
        name = div.get_attribute('name')

        current_fact = str({
            'tag': 'div',
            'index': index,
            'id': div_id,
            'role': role,
            'name': name,
            'text': text,
            'xPath': xpath,
            'contenteditable': contenteditable,
            'draggable': draggable,
            'tabindex': tabindex,
            'hidden': hidden,
            'title': title
        })

        # 현재 fact가 이전에 보낸 적 없는 경우에만 assert_fact 실행
        if current_fact not in sent_facts:
            assert_fact('web_test', eval(current_fact))
            sent_facts.add(current_fact)
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