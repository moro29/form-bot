from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, date
from zoneinfo import ZoneInfo

import random
import time
import os

# =========================
# GitHub Secrets
# =========================
EMPLOYEE = os.getenv("EMPLOYEE_NUMBER")
LAST_NAME = os.getenv("FORM_LAST_NAME")
FIRST_NAME = os.getenv("FORM_FIRST_NAME")
EMAIL = os.getenv("FORM_EMAIL")
OFFICE = os.getenv("OFFICE")

# =========================
# 現在時刻（日本時間）
# =========================
now = datetime.now(ZoneInfo("Asia/Tokyo"))

today = now.date()
hour = now.hour
minute = now.minute

# =========================
# 実行期間
# 2026/05/07 ～ 2026/05/22
# =========================
start_date = date(2026, 5, 7)
end_date = date(2026, 5, 22)
if not (start_date <= today <= end_date):
    print("対象期間外")
    exit()
# =========================
# 時間帯判定
# =========================
radio_id = None
dropdown_text = None

# 10:00〜10:20
if hour == 10 and minute <= 20:
    radio_id = "tmp_0"
    dropdown_text = "午前"

# 13:00〜13:20
elif hour == 13 and minute <= 20:
    radio_id = "tmp_1"
    dropdown_text = "昼"

# 16:00〜16:20
elif hour == 16 and minute <= 20:
    radio_id = "tmp_2"
    dropdown_text = "夕方"

else:
    print("対象時間外")
    exit()

# =========================
# ランダム待機
# 120秒〜1080秒
# =========================
wait_sec = random.randint(120, 1080)

print(f"{wait_sec}秒待機")

time.sleep(wait_sec)

# =========================
# Chrome設定
# =========================
options = Options()

options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
# =========================
# 1ページ目
# =========================

    # =========================
    # フォームURL
    # =========================
    driver.get("https://krs.bz/ssis/m?f=299")

    time.sleep(random.uniform(5, 10))

    # =========================
    # 社員番号入力
    # =========================
    name_box = driver.find_element(By.ID, "e_10663")

    name_box.send_keys(EMPLOYEE)

    time.sleep(random.uniform(10, 20))

    # =========================
    # 姓入力
    # =========================
    name_box = driver.find_element(By.ID, "e_10664")

    name_box.send_keys(LAST_NAME)

    time.sleep(random.uniform(10, 20))

    # =========================
    # 名入力
    # =========================
    name_box = driver.find_element(By.ID, "e_10665")

    name_box.send_keys(FIRST_NAME)

    time.sleep(random.uniform(10, 20))

    # =========================
    # メール入力
    # =========================
    email_box = driver.find_element(By.ID, "e_10666")

    email_box.send_keys(EMAIL)

    time.sleep(random.uniform(10, 30))

    # =========================
    # 所属入力
    # =========================
    email_box = driver.find_element(By.ID, "e_10669")

    email_box.send_keys(OFFICE)

    time.sleep(random.uniform(10, 20))

    # =========================
    # ラジオボタン
    # =========================
    if radio_id is None:
       print("対象外")
       exit()
    
    driver.find_element(By.ID, radio_id).click()

    time.sleep(random.uniform(5, 10))

    # =========================
    # プルダウン
    # =========================
    dropdown = Select(
        driver.find_element(By.ID, "e_10667")
    )

    dropdown.select_by_visible_text("東海BL")

    time.sleep(random.uniform(5, 15))

    # =========================
    # ページ移動
    # =========================

    # 2ページ目待機（送信ボタン出現）
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "__commit"))
    )

    # 送信ボタン押下
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "__commit"))
    )

    send_button.click()

    # 完了待ち（必要なら）
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'送信')]"))
    )

    print("送信完了")

    finally:
        driver.quit()
