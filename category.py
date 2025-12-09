# @ej31
# POM 패턴 꼭 적용해보시기 바랍니다.
# 아래와 같이 페이지 별로 묶어서 관리해주면 명확해지고 유지보수도 쉬워져서 시간을 아낄 수 있게 됩니다.
# 시간을 아낄 수 있는 방법을 찾아야해요!
# ✅ 로케이터 분리 예시
class InventoryPage:
    CATEGORY_FILTER = (By.ID, "category-filter")
    SELECT_ALL_CHECKBOX = (By.CSS_SELECTOR, "input[id='select-all']")
    ITEM_CHECKBOXES = (By.CSS_SELECTOR, "input[name='item-check']")
    
    def __init__(self, driver):
        self.driver = driver
    
    def select_category(self, category_name):
        dropdown = Select(self.driver.find_element(*self.CATEGORY_FILTER))
        dropdown.select_by_visible_text(category_name)


import time

from selenium import webdriver
from selenium.common import ElementNotVisibleException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from unicodedata import category
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select

# @ej31
# 모든 코드가 전부 함수화 혹은 클래스화가 되어 있지 않습니다.
# 지금 처럼 전역 스타일로 코드를 작성한다면 시간이 지나서 코드를 확장해야 할 때 전부 다 리팩토링 해야 할 수도 있습니다.

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

# 모든 카테고리 테스트
print("◽◽◽카테고리 별 조회 테스트입니다.◽◽◽")
dropdown_All = Select(driver.find_element(By.ID, "category-filter"))
dropdown_All.select_by_visible_text("모든 카테고리 보기")
All_category_text = driver.find_elements(By.CSS_SELECTOR, "tbody > tr > td:nth-child(6) > span")
values=[ct.text.replace("\n", " ") for ct in All_category_text]
print(f"✅모든 카테고리 총 {len(values)}, 카테고리 종류 {set(values)}")

# 카테고리 별 아이템 테스트
category_list = ["📦 전자기기 (Electronics)", "👕 의류 (Clothing)", "🍎 식품 (Food)"]
for category_name in category_list:
    dropdown = Select(driver.find_element(By.ID, "category-filter"))
    dropdown.select_by_visible_text(category_name)
    category_text = driver.find_elements(By.CSS_SELECTOR, "tbody > tr > td:nth-child(6) > span")
    values = [ct.text.replace("\n", " ") for ct in category_text]
    uniq_values = list(set(values))
    category_name = category_name.replace("\n", " ")
    if len(uniq_values) != 1:
        print(f"❎카테고리 드롭 실패, 문제 카테고리{category_name}")
    else:
        print(f"✅카테고리: {uniq_values}, 갯수: {len(values)} 입니다.")


### inventory 페이지 카테고리 상품 선택 후 새로고침 후 상태 확인(체크박스)
print("◽◽◽체크박스 선택 테스트입니다.◽◽◽")
dropdown_All.select_by_visible_text("모든 카테고리 보기")
checkbox_all = driver.find_element(By.CSS_SELECTOR, "input[id='select-all']")
checkbox = driver.find_elements(By.CSS_SELECTOR, "input[name='item-check']")
chkBox_cnt = 0
checkbox_all.click() # 체크박스를 선택해

# 선택된 체크 박스 갯수 찾기
for chk in checkbox:
    if chk.is_selected():
        chkBox_cnt += 1

if checkbox_all.is_selected():
    print(f"⭕체크 박스가 선택되었습니다. 선택된 체크 박스 {chkBox_cnt}개 ⭕")
    driver.refresh()
    print("🆕새로 고침 했습니다.🆕")
else:
    print("❌체크 박스 선택이 안되었습니다.❌")

# refresh가 되었어서 다시 요소 찾아야함.
checkbox_all = driver.find_element(By.CSS_SELECTOR, "input[id='select-all']")
checkbox = driver.find_elements(By.CSS_SELECTOR, "input[name='item-check']")
chkBox_cnt = 0
for chk in checkbox:
    if chk.is_selected():
        chkBox_cnt += 1
if not checkbox_all.is_selected():
    print(f"⭕체크 박스가 초기화되었습니다. 선택된 체크 박스 {chkBox_cnt}개 ⭕")
else:
    print("❌체크 박스 초기화 실패입니다.❌")


# 제품 수정
print("◽◽◽제품 수정 테스트입니다.◽◽◽")
itemUpdate_list = [
    ('내 마우스1', '1000', '5', "의류 (Clothing)"), #정상 변경
    ('FastTrack Logo Hoodie (L)', '-100', '0', "의류 (Clothing)"), #가격 마이너스
    ('', '45000', '0', "의류 (Clothing)"), #제품명 없음
    ('FastTrack Logo Hoodie (L)', '49000', '-10', "의류 (Clothing)") #갯수 마이너스
]
for item in itemUpdate_list:
    # 전체 재고 목록에서 ele 따옴
    pName_before = driver.find_element(By.CSS_SELECTOR, "tr[data-id='item-201']>td>div>span").text
    price_before = driver.find_element(By.CSS_SELECTOR, "tr[data-id='item-201']>td:nth-child(3)").text
    stock_before = driver.find_element(By.CSS_SELECTOR, "tr[data-id='item-201']>td:nth-child(4)>span").text
    cate_before = driver.find_element(By.CSS_SELECTOR, "tr[data-id='item-201']>td:nth-child(6)>span").text.replace("\n", "")
    print("⬇️⬇️⬇️수정 전⬇️⬇️⬇️️")
    print(f'제품명: {pName_before}, 가격:{price_before}, 재고: {stock_before}, 카테고리: {cate_before}')

    driver.find_element(By.CSS_SELECTOR, "tr[data-id='item-201']>td>button").click()
    pName, price, stock, cate = item
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

    driver.find_element(By.ID, "save-btn").click()
    #print(pName, price, stock, cate)
    # time sleep 말고 WebDriverWait 을 쓰시는게 좋습니다.
    # 만약 특정 상태가 될 때까지 기다리기 위해서 의도적으로 3초를 쉰거라면 그 상태가 무엇인지 주석에 상세를 적어놓고 WebDriver 에 있는 기능을 최대한 활용하는게 좋습니다.
    # 크롤링 코드가 아닌 테스트 코드에선 time.sleep 은 가급적 쓰지 않는게 좋습니다.
    time.sleep(3)

    try:
        result = driver.switch_to.alert
        print(f'❌{result.text}, "수정 실패"❌')
        print("===============================================================================")
        result.accept()
        driver.find_element(By.CSS_SELECTOR, "button[onclick='closeModal()']").click()
        continue
    except:
        print("✅수정 성공")

    pName_after = driver.find_element(By.CSS_SELECTOR, "tr[data-id='item-201']>td>div>span").text
    price_after = driver.find_element(By.CSS_SELECTOR, "tr[data-id='item-201']>td:nth-child(3)").text
    stock_after = driver.find_element(By.CSS_SELECTOR, "tr[data-id='item-201']>td:nth-child(4)>span").text
    cate_after = driver.find_element(By.CSS_SELECTOR, "tr[data-id='item-201']>td:nth-child(6)>span").text.replace("\n", "")
    print("🆗수정 후🆗")
    print(f'제품명: {pName_after}, 가격:{price_after}, 재고: {stock_after}, 카테고리: {cate_after}')
    print("===============================================================================")


### 재고 부족 알림 발주/수정 테스트
print("◽◽◽재고 부족 알림 발주/수정 버튼 테스트입니다.◽◽◽")
# driver.implicitly_wait(10)
# 판매주기 slider
slider = driver.find_element(By.CSS_SELECTOR, 'input[id="speed-control"]')
time.sleep(2)
# 1초로 설정
driver.execute_script(
    "arguments[0].value = 100; arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));",
    slider
)

time.sleep(5)
low_pName_list_bef = driver.find_elements(By.CSS_SELECTOR, 'tbody[id="low-stock-body"]>tr>td:nth-child(1)')
low_pName_value_bef = [item.text for item in low_pName_list_bef]

print(f'✅현재 재고 부족 상품은 : {low_pName_value_bef}')

wait = WebDriverWait(driver, 10)

openEditModal = wait.until(
EC.element_to_be_clickable(
    (By.XPATH, "//button[@onclick=\"openModal('edit', 'item-102')\" and normalize-space(text())='발주/수정']")
    )
)

try:
    openEditModal.click()
except StaleElementReferenceException:
    openEditModal = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@onclick=\"openModal('edit', 'item-102')\" and normalize-space(text())='발주/수정']")
        )
    )
    #  item 발주/수정이 뜰 때까지 기다림
    openEditModal.click()

# stock 입력 할 수 있을때까지 기다림
it_stock_id = wait.until(EC.visibility_of_element_located((By.ID, "stock")))

it_stock_id.clear()
it_stock_id.send_keys('10')
driver.find_element(By.ID, "save-btn").click()

driver.execute_script(
    "arguments[0].value = 3000; arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));",
    slider
)

low_pName_list = driver.find_elements(By.CSS_SELECTOR, 'tbody[id="low-stock-body"]>tr>td:nth-child(1)')
low_pName_value = [item.text for item in low_pName_list]

if "Keychron K8 Pro Keyboard" not in low_pName_value:
    print("⭕Keychron K8 Pro Keyboard의 재고가 추가입고 되었습니다.⭕")
    print(f'✅현재 재고는 : {low_pName_value}')
else :
    print("❌수정이 좀 덜 된 것 같습니다 ~~ ❌")
    print(f'✅현재 재고는 : {low_pName_value}')
