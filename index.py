import time
import logging
from selenium import webdriver
from selenium.common import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# 1. 브라우저 꺼짐 방지 옵션 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 스크립트가 끝나도 브라우저가 꺼지지 않게하려면 True 로 변경
chrome_options.add_argument("--start-maximized")  # 브라우저 창 최대화

# 2. 드라이버 자동 설치 및 서비스 설정 (가장 중요한 부분!)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://ej31.github.io/learn-for-selector/"
driver.get(url)
driver.implicitly_wait(10)

# 로깅 설정
#logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s - %(message)s')
#
# 3. 정상 로그인 테스트
print("◽◽◽로그인 성공 테스트입니다.◽◽◽")
el_login_id = driver.find_element(By.ID, "loginId") #선택자 지정
el_login_pw = driver.find_element(By.ID, "loginPw")
el_login_id.send_keys("admin") # 입력값
el_login_pw.send_keys("1234")
driver.implicitly_wait(10)

driver.find_element(By.CSS_SELECTOR, ".btn_action_primary").click() # 버튼 클릭
time.sleep(2)
driver.switch_to.alert.accept() # alert 창 확인 (인증 성공, 대시보드로 이동합니다.)

# if alert.text == '인증 성공. 대시보드로 이동합니다.':
#     logging.info(alert.text, "로그인 성공했습니다.")
# else:
#     logging.info(alert.text, "로그인 실패입니다.")

# 4. 로그인 성공 확인 및 로그인 실패 테스트를 위한 로그아웃
try:
    #welcome_msg = driver.find_element((By.XPATH, "//span[@id='welcome-msg']")).is_displayed()
    #print(welcome_msg)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "welcome-msg")))
    print("⭕ID: admin, PW: 1234 로그인 성공입니다.⭕")
except:
    print("❌ID: admin, PW: 1234 로그인 실패입니다.❌")

# 5. 로그아웃
print("◽◽◽로그아웃 및 로그인 실패 테스트입니다.◽◽◽")
driver.find_element(By.ID, "logout-btn").click()
driver.implicitly_wait(10)
print("✅ 로그아웃하여 index.html 초기화면으로 돌아갑니다.")

# 6. 로그인 실패 테스트 반복
user_list = [
    ('Admin', ''),
    ('', '1234'),
    ('', ''),
    ('Ad min', '1234'),
    ('aaadmin', '4567')
]

for u_id,u_pw in user_list:
    el_login_id = driver.find_element(By.ID, "loginId")
    el_login_id.send_keys(u_id)
    el_login_pw = driver.find_element(By.ID, "loginPw")
    el_login_pw.send_keys(u_pw)
    driver.find_element(By.CSS_SELECTOR, ".btn_action_primary").click()  # 버튼 클릭
    driver.implicitly_wait(10)

    try:
        # ID 가 welcome-msg인게 보일때까지 기다렸다가 값 주기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "welcome-msg")))
        print(f'⭕ ID: {u_id} & PW: {u_pw} 로그인 성공 ⭕')
    except:
        print(f'❌ ID: {u_id} & PW: {u_pw} 로그인 실패입니다 ❌')


    driver.refresh() # 페이지 새로고침
    txt_login_id = driver.find_element(By.ID, "loginId").get_attribute("value")
    txt_login_pw = driver.find_element(By.ID, "loginPw").get_attribute("value")
    if txt_login_id=="" and txt_login_pw == "":
        print("새로 고침하여 입력되어 있는 ID/PW를 초기화되었습니다.")
        driver.implicitly_wait(10)
    else:
        print("❌ID/PW가 초기화 되지 않아 수동 초기화로 진행합니다.❌")
        txt_login_id = ""
        xt_login_pw = ""
    
######## 7. 이용 약관 및 개인정보 처리방침 동작 (보류)
driver.find_element(By.XPATH, "//a[@href='terms.html']").click()
def scroll_down():
    url2 = "https://ej31.github.io/learn-for-selector/terms.html"
    driver.get(url2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    driver.save_screenshot("terms.png")
    print("📸이용약관 스크린샷 찍었습니다.📸")
scroll_down()




