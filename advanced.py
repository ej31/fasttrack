# @ej31
# 지금 코드는 "실행코드"의 형태이고 QA 테스팅을 위한 코드로 변환이 필요합니다.
# @pytest 를 사용해서 실제 테스트 코드의 형태로 만들어보세요! 
import time

from selenium import webdriver
from selenium.common import ElementNotVisibleException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v140.fetch import continue_request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from unicodedata import category
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from websocket import continuous_frame


# 1. 브라우저 꺼짐 방지 옵션 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 스크립트가 끝나도 브라우저가 꺼지지 않게하려면 True 로 변경
chrome_options.add_argument("--start-maximized")  # 브라우저 창 최대화

# 2. 드라이버 자동 설치 및 서비스 설정 (가장 중요한 부분!)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


url = "https://ej31.github.io/learn-for-selector/advanced.html"
driver.get(url)
driver.implicitly_wait(10)

# 주문 목록 동기화
print("◽◽◽주문 목록 동기화 테스트입니다.◽◽◽")
driver.find_element(By.CSS_SELECTOR, 'button[id="btn-load-orders"]').click()
driver.implicitly_wait(10)

try:
    order_list = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div#order-list"))
    )
    print("⭕주문 목록 동기화 완료⭕")
except:
    # @ej31 이와 같이 예외처리 하는건 Bare except 처리 라고 합니다. 이렇게 처리하면 나중에 폭탄 맞습니다. 터져야 할 때 안터져서 에러를 못찾는 끔찍한 일이 벌어져요
    print("❌요소를 찾을 수 없거나 표시되지 않음❌")


# 파일 업로드(성공)
print("◽◽◽파일 업로드 성공 테스트입니다.◽◽◽")
file_upload_ele = driver.find_element(By.ID, 'file-upload')
# @ej31
# 파일 경로를 하드코딩 하시면 다른 환경에서는 실행을 반드시 실패 할 수 밖에 없습니다.
# 그리고 실행에 필요한 파일은 모든 환경에서 특정 할 수 경로에 위치 시키는게 좋습니다.
# 아직은 리눅스를 배우지 않아서 생소하시겠지만 "/tmp/fasttrack/dummy_images/...." 처럼 임시로 폴더를 설정해서 그 곳에 위치시키거나 프로젝트 루트경로에 파일을 올려두고 쓰는게 좋습니다.
# 그래야 환경이 바뀌어도 터지지 않는 튼튼한 코드가 완성 됩니다.
# 정리해보자면 상대 경로 혹은 환경 변수를 사용하는게 좋다라고 볼 수 있겠습니다.
# file_path = os.path.join(os.path.dirname(__file__), "test_files", "test.jpg")  ==> 이와 같이 프로젝트 루트 경로에서 파일 올려놓고 쓰면 터질일이 없음
file_path =  r"C:\Users\zup70\OneDrive\Desktop\KakaoTalk_20251020_111409517.jpg"
file_upload_ele.send_keys(file_path)

driver.find_element(By.ID, 'btn-upload').click()

try:
    # 토스트 메시지가 나타날 때까지 기다림
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
    print("✅토스트 메시지:", toast.text)

    # (선택) 토스트가 사라질 때까지 기다림
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
except StaleElementReferenceException :
    print("❎토스트 메시지를 찾을 수 없거나 표시되지 않았습니다.")

# 파일 업로드(강제 실패 모드)
print("◽◽◽파일 업로드 실패 테스트입니다.◽◽◽")
driver.refresh()
file_upload_ele = driver.find_element(By.ID, 'file-upload')
file_path =  r"C:\Users\zup70\OneDrive\Desktop\KakaoTalk_20251020_111409517.jpg"
file_upload_ele.send_keys(file_path)

driver.find_element(By.CSS_SELECTOR, "input[id='force-fail-check']").click()
driver.find_element(By.ID, 'btn-upload').click()

try:
    # 토스트 메시지가 나타날 때까지 기다림
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
    print("✅토스트 메시지:", toast.text)

    # (선택) 토스트가 사라질 때까지 기다림
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
except StaleElementReferenceException :
    print("❎토스트 메시지를 찾을 수 없거나 표시되지 않았습니다.")

#파일 업로드(실패, 아무것도 안 넣기)
print("◽◽◽파일 업로드 null값 테스트입니다.◽◽◽")
driver.refresh()
driver.find_element(By.ID, 'btn-upload').click()

try:
    # 토스트 메시지가 나타날 때까지 기다림
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
    print("✅토스트 메시지:", toast.text)

    # (선택) 토스트가 사라질 때까지 기다림
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
except StaleElementReferenceException :
    print("❎토스트 메시지를 찾을 수 없거나 표시되지 않았습니다.")

# 월간 재고 실사 예약 일정 등록
print("◽◽◽일정 등록 모달 테스트입니다.◽◽◽")
driver.refresh()
driver.find_element(By.CSS_SELECTOR, 'button[onclick="openResModal(\'add\')"]').click()

Modal = driver.find_element(By.ID, 'reservationModal')
if Modal.is_displayed():
    print('✅실사 일정 등록 모달 뜸✅')
else:
    print('❌모달 안뜸❌')

# 1. 아무것도 입력X
print("◽◽◽월간 재고 실사 예약 일정 등록 아무것도 입력xxx 테스트입니다.◽◽◽")
driver.find_element(By.CSS_SELECTOR, 'button[onclick="saveReservation()"]').click()
try:
    # 토스트 메시지가 나타날 때까지 기다림
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
    print("✅토스트 메시지:", toast.text)

    # (선택) 토스트가 사라질 때까지 기다림
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
except StaleElementReferenceException :
    print("❎토스트 메시지를 찾을 수 없거나 표시되지 않았습니다.")

# 2. 담당자만 입력
print("◽◽◽월간 재고 실사 예약 일정 등록 담당자만 입력 테스트입니다.◽◽◽")
driver.find_element(By.ID, "res-manager").send_keys("맹구")
driver.find_element(By.CSS_SELECTOR, 'button[onclick="saveReservation()"]').click()
try:
    # 토스트 메시지가 나타날 때까지 기다림
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
    print("✅토스트 메시지:", toast.text)

    # (선택) 토스트가 사라질 때까지 기다림
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
except StaleElementReferenceException :
    print("❎토스트 메시지를 찾을 수 없거나 표시되지 않았습니다.")

# 3. 예정일만 입력
print("◽◽◽월간 재고 실사 예약 일정 등록 예정일만 입력 테스트입니다.◽◽◽")
driver.find_element(By.ID, "res-manager").clear()
res_Date = driver.find_element(By.ID, 'datepicker')
driver.find_element(By.CSS_SELECTOR, 'button[onclick="saveReservation()"]').click()
driver.execute_script(
"arguments[0].value = '2025-12-02'; arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));",
res_Date
)
try:
    # 토스트 메시지가 나타날 때까지 기다림
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
    print("✅토스트 메시지:", toast.text)

    # (선택) 토스트가 사라질 때까지 기다림
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
except StaleElementReferenceException :
    print("❎토스트 메시지를 찾을 수 없거나 표시되지 않았습니다.")





# 새로운 일정 추가 !!
# 날짜 선택
print("◽◽◽NEW 월간 재고 실사 예약 일정 등록 테스트입니다.◽◽◽")
driver.find_element(By.CSS_SELECTOR, 'button[onclick="saveReservation()"]').click()
res_Date = driver.find_element(By.ID, 'datepicker')
driver.execute_script(
"arguments[0].value = '2025-12-02'; arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));",
res_Date
)
#실사 구분 선택
dropdown = Select(driver.find_element(By.ID, "res-type"))
dropdown.select_by_visible_text("수시 실사 (Spot)")

#담당자 입력
driver.find_element(By.ID, "res-manager").clear()
driver.find_element(By.ID, "res-manager").send_keys("흰둥이")

# 저장
driver.find_element(By.CSS_SELECTOR, 'button[onclick="saveReservation()"]').click()
try:
    # 토스트 메시지가 나타날 때까지 기다림
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
    print("✅토스트 메시지:", toast.text)


    # 토스트 닫힘 확인
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.bottom-5.right-5.z-50"))
    )
except StaleElementReferenceException :
    print("❎토스트 메시지를 찾을 수 없거나 표시되지 않았습니다.")

res_add_after = driver.find_elements(By.CSS_SELECTOR, 'tbody[id="res-table-body"]>tr')
res_add_value = [item.text.split('\n') for item in res_add_after]

print(f'⭕{res_add_value[-1]} 일정이 정상 추가 되었습니다.')
print(f'✅현재 등록된 조사 일정은: {res_add_value}')


# 일정 수정 !!!!
print("◽◽◽UPDATE 월간 재고 실사 예약 일정 등록 테스트입니다.◽◽◽")
# 월간 재고 실사 예약 일정 수정
driver.find_element(
    By.CSS_SELECTOR,
    'button[onclick="openResModal(\'edit\', \'RES-002\')"]'
).click()

# 날짜 선택
res_Date = driver.find_element(By.ID, 'datepicker')
driver.execute_script(
"arguments[0].value = '2025-11-28'; arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));",
res_Date
)
#실사 구분 선택
dropdown = Select(driver.find_element(By.ID, "res-type"))
dropdown.select_by_visible_text("정기 실사 (Regular)")

#담당자 입력
driver.find_element(By.ID, "res-manager").clear()
driver.find_element(By.ID, "res-manager").send_keys("짱구")

# 실사 완료 처리
driver.find_element(By.CSS_SELECTOR, "input[id='res-completed']").click() # 체크박스를 선택해
# 비고 작성
driver.find_element(By.ID, "res-memo").send_keys("실사 조사 완료됨")
driver.find_element(By.CSS_SELECTOR, 'button[onclick="saveReservation()"]').click()

res_up_after = driver.find_elements(By.CSS_SELECTOR, 'tbody[id="res-table-body"]>tr')
res_up_value = [item.text.split('\n') for item in res_up_after]
print(f'✅현재 등록된 조사 일정은: {res_up_value}')

