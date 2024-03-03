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
import json_process
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
driver = webdriver.Chrome(service=service_obj, options=chrome_options)
# 웹페이지 열기
driver.get("https://naver.com")

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
if __name__ == "__main__":
    initialize_file()
    for button in buttons:
        try:
            try:
                # button 요소의 outerHTML을 가져오기
                outerHTML = button.get_attribute('outerHTML')
            except StaleElementReferenceException:
                # StaleElementReferenceException이 발생하면 현재 요소를 무시하고 다음 요소로 넘어감
                continue

            soup = BeautifulSoup(outerHTML, 'html.parser')
            button_element = soup.find('button')
            button_id = button_element.get('id')
            button_class = button_element.get('class')

            if button_id:
                xpath = f"//button[@id='{button_id}']"
            # elif button_class:
            #     class_selector = '.'.join(button_class)
            #     xpath = f"//button[contains(@class, '{class_selector}')]"
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
                'text': text,
                'xPath': xpath,
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
        except Exception as e:
            print(f"오류 발생: {e}")
            continue
    initialize_file()
    for form in forms:
        try:
            try:
                # form 요소의 outerHTML을 가져오기
                outerHTML = form.get_attribute('outerHTML')
            except StaleElementReferenceException:
                # StaleElementReferenceException이 발생하면 현재 요소를 무시하고 다음 요소로 넘어감
                continue

            soup = BeautifulSoup(outerHTML, 'html.parser')
            form_id = form.get_attribute('id')
            form_class = form.get_attribute('class')

            if form_id:
                xpath = f"//form[@id='{form_id}']"
            # elif form_class:
            #     class_selector = '.'.join(form_class.split())
            #     xpath = f"//form[contains(@class, '{class_selector}')]"
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

            assert_fact('web_test', {
                'tag': 'form',
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
        except Exception as e:
            print(f"오류 발생: {e}")
            continue
    initialize_file()
    for link in links:
        try:
            try:
                # a 태그 요소의 outerHTML을 가져오기
                link_html = link.get_attribute('outerHTML')
            except StaleElementReferenceException:
                # StaleElementReferenceException이 발생하면 현재 요소를 무시하고 다음 요소로 넘어감
                continue

            soup = BeautifulSoup(link_html, 'html.parser')
            link_tag = soup.a

            link_href = link_tag.get('href')
            link_text = link_tag.text.strip()
            link_target = link_tag.get('target', '_self')
            link_rel = link_tag.get('rel')
            link_id = link_tag.get('id')
            link_class = link_tag.get('class')
            class_value = link_class[0] if link_class else None  # 클래스가 없는 경우 None으로 설정
            link_title = link_tag.get('title')
            link_aria_label = link_tag.get('aria-label')
            link_download = link_tag.get('download')
            if link_id:
                xpath = f"//a[@id='{link_id}']"
            # elif link_class:
            #     # class가 여러 개 있을 수 있으므로 join 사용
            #     class_selector = '.'.join(link_class)
            #     link_xpath = f"//a[contains(@class, '{class_selector}')]"
            else:
                # id와 class 모두 없는 경우, JavaScript 함수를 사용해 XPath 생성
                link_xpath = driver.execute_script(script, link)
            #link_xpath = driver.execute_script(script, link) if not link_id else f"//a[@id='{link_id}']"

            current_fact = str({
                'tag': 'a',
                'href': link_href,
                'text': link_text,
                'target': link_target,
                'rel': link_rel,
                'id': link_id,
                'class_': class_value,
                'title': link_title,
                'aria-label': link_aria_label,
                'xPath': link_xpath,
                'download': link_download
            })

            # 현재 fact가 이전에 보낸 적 없는 경우에만 assert_fact 실행
            if current_fact not in sent_facts:
                assert_fact('web_test', eval(current_fact))
                sent_facts.add(current_fact)
        except Exception as e:
            print(f"오류 발생: {e}")
            continue
    initialize_file()
    # 추출된 요소에 대한 assert_fact
    for div in divs:
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
            print(div_class)
            class_value = div_class[0] if div_class else None  # 클래스가 없는 경우 None으로 설정

            # id, class 또는 다른 속성에 따라 적절한 XPath 생성
            if div_id:
                xpath = f"//div[@id='{div_id}']"
            # elif div_class:
            #     # class가 여러 개 있을 수 있으므로 join 사용
            #     class_selector = '.'.join(div_class)
            #     xpath = f"//div[contains(@class, '{class_selector}')]"
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

    driver.quit()