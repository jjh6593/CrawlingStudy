from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service_obj = Service("E:\chromedriver-win64\chromedriver.exe");
driver = webdriver.Chrome(service=service_obj, options=chrome_options)

driver.get("https://rahulshettyacademy.com/client/")
driver.find_element(By.LINK_TEXT, "Forgot password?").click()
driver.find_element(By.XPATH,"//form/div[1]/input").send_keys("demo@gmail.com")
driver.find_element(By.CSS_SELECTOR,"form div:nth-child(2) input").send_keys("Hello@1234")
driver.find_element(By.CSS_SELECTOR,"#confirmPassword").send_keys("Hello@1234")
#driver.find_element(By.XPATH, "//button[@type='submit'").click()
driver.find_element(By.XPATH, "//button[text()='Save New Password']").click()
#driver.find_element(By.LINK_TEXT).click()
# //form
# form 안에 있는 요소에 접근할 때 양식이 여러개일 경우 //form/div[1]/input
# //tagname으로 접근이 어려움, css 의 경우 form div:nth-child(2) input
# LINK_Text가 아닐때는 //button[text()='Save New Password'

# ID, Xpath, CSSSelector, Classname, name, linkText