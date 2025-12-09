# @ej31
# 현재 코드에 POM을 적용해주시고 이후에 점진적으로 계층을 나누어보시기 바랍니다.
# 꼭 필요한 과정이에요!!
# 계층을 나눌 때 여러가지 방법이 있으나 잘알려져있고 보편적인 방법 중 하나는 "클린 아키텍쳐" 입니다. (보편적이라고 해서 쉽다는게 아닙니다. 공부해야되요!)
# 1단계 POM 도입해서 Locator, Action 분리하기 -> 2단계 Driver wrapping 하기 or 추상화하기 -> 3단계 use case 분리하기 (비즈니스 로직 캡슐화하기!, 캡슐화는 객체지향에서 쓰는 용어입니다.) -> 4단계 설정을 외부화하기 (설정 값이나 테스트에 사용되는 외부 이미지 등의 테스트 데이터를 분리해서 관리하기)

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

    # @ej31
    # 오타 있습니다. `presEence_of_element_located` => 이거 실행 되던가요?.. 안될텐데..
    WebDriverWait(driver, 10).until(EC.presEence_of_element_located((By.ID, "welcome-msg")))
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
        # @ej31 이 변수는 앞에서 선언 된 적이 없습니다. 음............................ 실행 해보지 않으신거 같은데.................. 🙄
        xt_login_pw = ""
    
######## 7. 이용 약관 및 개인정보 처리방침 동작
driver.find_element(By.XPATH, "//a[@href='terms.html']").click()
def scroll_down():
    url2 = "https://ej31.github.io/learn-for-selector/terms.html"
    driver.get(url2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    driver.save_screenshot("terms.png")
    print("📸이용약관 스크린샷 찍었습니다.📸")
scroll_down()




