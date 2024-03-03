from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
driver = webdriver.Chrome(service=service_obj, options=chrome_options)
driver.get("https://www.naver.com")

# 웹 페이지의 모든 요소 가져오기
elements = driver.find_elements(By.XPATH, "//*")

# 각 요소에 대해 onclick 이벤트 리스너 확인
for element in elements:
    if driver.execute_script("return arguments[0].onclick;", element):
        # 이벤트 리스너가 있는 요소의 HTML 태그
        tag = element.tag_name

        # 요소의 XPath 추출
        xpath = driver.execute_script("""
        function getElementXPath(element) {
            if (element.id !== '') return 'id("' + element.id + '")';
            if (element === document.body) return element.tagName;

            var ix = 0;
            var siblings = element.parentNode.childNodes;
            for (var i = 0; i < siblings.length; i++) {
                var sibling = siblings[i];
                if (sibling === element)
                    return getElementXPath(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
                    ix++;
            }
        }
        return getElementXPath(arguments[0]);
        """, element)

        print(f"Tag: {tag}, XPath: {xpath}")

#driver.quit()