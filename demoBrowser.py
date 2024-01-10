from selenium import webdriver

#chrome driver
from selenium.webdriver.chrome.service import Service

service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
driver = webdriver.Chrome(service=service_obj)

driver.get("http://www.naver.com")
print(driver.title) # 타이틀 출력
print(driver.current_url)
driver.get("https://donghodazzi.tistory.com/306")
#driver.minimize_window()
#driver.back()
#driver.refresh()
#driver.forward()
#driver.close()

# 크롬브라우저 실행을 위해서 작성하는 것
