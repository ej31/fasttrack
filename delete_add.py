import time

from selenium import webdriver
from selenium.common import ElementNotVisibleException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# @ej31
# 안쓰는 드는 삭제하시는게 좋습니다. 
from selenium.webdriver.common.devtools.v140.fetch import continue_request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# @ej31
# 이거 임포트 된 category 가 변수명 겹칠 수도 있지 않을까 하는 불안감이 살짝 생깁니다.
# 아래 코드 내용 중 "element-*" 의 이름을 가진 객체가 존재해서 아슬아슬해 보여요
from unicodedata import category
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select
from websocket import continuous_frame


# @ej31
# 코드가 중복되서 나오고 있습니다.
# 드라이버 설정이 중복되서 나오는 요 부분은 따로 wrapper 함수 혹은 클래스를 만들어서 사용하시는게 좋습니다. 예를 들면..
# def get_driver():
#     chrome_options = Options()
#     chrome_options.add_experimental_option("detach", True)
#     chrome_options.add_argument("--start-maximized")
#     service = Service(ChromeDriverManager().install())
#     return webdriver.Chrome(service=service, options=chrome_options)"""
# 이 반복되는 코드를 따로 빼줌으로써 유지보수성을 끌어올리는 것이지요
# 1. 브라우저 꺼짐 방지 옵션 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 스크립트가 끝나도 브라우저가 꺼지지 않게하려면 True 로 변경
chrome_options.add_argument("--start-maximized")  # 브라우저 창 최대화

# 2. 드라이버 자동 설치 및 서비스 설정 (가장 중요한 부분!)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


url = "https://ej31.github.io/learn-for-selector/inventory.html"
driver.get(url)
driver.implicitly_wait(10)

# 개별 삭제 확인
print("◽◽◽개별 삭제 확인 테스트입니다.◽◽◽")
driver.find_element(By.CSS_SELECTOR, 'tr[data-id="item-101"] > td > button[onclick="deleteItem(\'item-101\')"]').click()
try:
    alert = driver.switch_to.alert
    print(alert.text)
    if alert.text == "삭제 확인: 이 항목을 영구적으로 삭제하시겠습니까?":
        alert.accept() # 삭제 진행
        print("✅개별 확인 삭제 alert 창 확인✅")
    else:
        print(f'❌alert창이 다릅니다.{alert.text}❌')
except Exception as e:
    # @ej31 예외처리 이렇게 하면 안됩니다! 터져야 할 때 안터지는게 더 끔찍한 일이에요. 이렇게 하면 걍 모든 예외가 정상인척하고 슉슉 지나갈 수 있어요
    # 로그 빡세게 찍히면 이거 traceback 발견 못합니다.
    print(e)

pName_before = driver.find_elements(By.CSS_SELECTOR, "tbody[id='table-body']>tr>td>div>span.product-name")
pName_value = [item.text for item in pName_before]

if "Logitech G PRO Wireless" not in pName_value:
    print("⭕Logitech G PRO Wireless가 삭제되었습니다.⭕")
    print(f'✅현재 재고는 {pName_value}')
else :
    print("❌수정이 좀 덜 된 것 같습니다 ~~ ❌")
    print(f'현재 재고는 {pName_value}')
    
    
## 다중 삭제 확인
print("◽◽◽다중 삭제 확인 테스트입니다.◽◽◽")
# 데이터 초기화
driver.find_element(By.CSS_SELECTOR, 'button[onclick="resetData()"]').click()
driver.switch_to.alert.accept()
driver.switch_to.alert.accept()

# 체크박스 선택
dropdown_All = Select(driver.find_element(By.ID, "category-filter"))
dropdown_All.select_by_visible_text("모든 카테고리 보기")
checkbox_101 = driver.find_element(By.CSS_SELECTOR, 'input[value="item-101"')
checkbox_201 = driver.find_element(By.CSS_SELECTOR, 'input[value="item-201"')

checkbox_101.click() # 체크박스를 선택해
checkbox_201.click()


# @ej31
# 이런식으로 특정 행동 하나를 함수로 모두 감싸 주시는게 좋습니다.
# 그래야 어떻게 테스트를 할 지 시나리오를 작성할 수 있어요. 재사용성 확보 무조건 중요합니다.
del_btn = driver.find_element(By.CSS_SELECTOR, 'button[id="delete-selected-btn"]')
if del_btn.is_enabled():
    print("✅선택 항목(다중) 삭제 버튼이 활성화 되었습니다.")
    del_btn.click()
    alert = driver.switch_to.alert
    if "다중 삭제 확인" in alert.text:
        print(alert.text)
        print("✅다중 확인 삭제 alert 창 확인✅")
        alert.accept()
    else:
        # @ej31
        # 예외인 상황 같으나 프린팅만 되고 마는 상태여서 이것만 가지고는 이 코드로 뭘 하고 싶은건지 의도 파악이 안되서 뒤에 코드 이어 받는 사람이 맥락을 파악 못하고 폭탄 맞습니다.
        print("❌다중 삭제가 아닌 것 같습니다 ............❌")
else:
    # @ej31
    # assert를 사용해서 테스트 실패인 경우를 명확히 표기해주시는게 좋습니다. 위와 마찬가지로 이게 실패인지 아닌지 확인하기 어렵습니다.
    print("❌삭제 버튼이 안 생겼습니다.❌")


pName_del_after = driver.find_elements(By.CSS_SELECTOR, "tbody[id='table-body']>tr>td>div>span.product-name")
pName_del_value = [item.text for item in pName_del_after]

if "Logitech G PRO Wireless" not in pName_del_value and "FastTrack Logo Hoodie (L)" not in pName_del_value:
    print("⭕Logitech G PRO Wireless와 FastTrack Logo Hoodie (L)가 삭제되었습니다.⭕")
    print(f'✅현재 재고는 : {pName_del_value}')
else :
    print("❌수정이 좀 덜 된 것 같습니다.❌")
    print(f'✅현재 재고는 : {pName_del_value}')


## 아이템 추가
print("◽◽◽아이템 확인 테스트입니다.◽◽◽")
itemCreate_list = [
    ('귤 까주는 기계','5000','20','전자기기 (Electronics)','10'),
    ('귤 까주는 기계2','','','전자기기 (Electronics)','10') ]

for item in itemCreate_list:
    driver.find_element(By.ID, 'add-item-btn').click()
    pName, price, stock, cate, min_stock = item
    it_name_id = driver.find_element(By.ID, "name")
    it_name_id.clear()
    it_name_id.send_keys(pName)
    #print("이름 입력 ok", pName)

    it_price_id = driver.find_element(By.ID, "price")
    it_price_id.clear()
    it_price_id.send_keys(price)
    #print("가격 입력 ok", price)

    it_stock_id = driver.find_element(By.ID, "stock")
    it_stock_id.clear()
    it_stock_id.send_keys(stock)
    #print("재고 입력 ok", stock)

    dropdown_All = Select(driver.find_element(By.ID, "category"))
    dropdown_All.select_by_visible_text(cate)
    #print("카테 입력 ok",cate)

    it_min_stock_id = driver.find_element(By.ID, "min-stock")
    it_min_stock_id.clear()
    it_min_stock_id.send_keys(min_stock)

    driver.find_element(By.ID, "save-btn").click()

    try:
        result = driver.switch_to.alert
        reason = result.text
        result.accept()
        print(f'❎{pName} 추가 실패')
        print(f'❎ 추가 실패 사유는 : {reason}')
        driver.find_element(By.CSS_SELECTOR, "button[onclick='closeModal()']").click()
        continue
    except:
        print(f'✅{pName} 추가 성공')

pName_add_after = driver.find_elements(By.CSS_SELECTOR, "tbody[id='table-body']>tr>td>div>span.product-name")
pName_add_value = [item.text for item in pName_add_after]
print(f' 현재 재고는 : {pName_add_value}')
