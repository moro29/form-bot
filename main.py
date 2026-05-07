from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from datetime import datetime, date
from zoneinfo import ZoneInfo

import random
import time
import os


# =========================
# Secrets
# =========================
EMPLOYEE = os.getenv("EMPLOYEE_NUMBER")
LAST_NAME = os.getenv("FORM_LAST_NAME")
FIRST_NAME = os.getenv("FORM_FIRST_NAME")
EMAIL = os.getenv("FORM_EMAIL")
OFFICE = os.getenv("OFFICE")


# =========================
# 時刻
# =========================
now = datetime.now(ZoneInfo("Asia/Tokyo"))
today = now.date()
hour = now.hour
minute = now.minute


# =========================
# 実行期間
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

if hour == 10 and minute <= 20:
    radio_id = "tmp_0"

elif hour == 13 and minute <= 20:
    radio_id = "tmp_1"

elif hour == 16 and minute <= 20:
    radio_id = "tmp_2"

else:
    print("対象時間外")
    exit()

if radio_id is None:
    print("radio未設定")
    exit()


# =========================
# 人間っぽい待機
# =========================
time.sleep(random.randint(120, 1080))


# =========================
# Chrome設定
# =========================
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)


try:

    # =========================
    # フォームアクセス
    # =========================
    driver.get("https://krs.bz/ssis/m?f=299")

    wait.until(EC.presence_of_element_located((By.ID, "e_10663")))


    # =========================
    # 1ページ目入力
    # =========================
    driver.find_element(By.ID, "e_10663").send_keys(EMPLOYEE)
    driver.find_element(By.ID, "e_10664").send_keys(LAST_NAME)
    driver.find_element(By.ID, "e_10665").send_keys(FIRST_NAME)
    driver.find_element(By.ID, "e_10666").send_keys(EMAIL)
    driver.find_element(By.ID, "e_10669").send_keys(OFFICE)


    # =========================
    # ラジオボタン
    # =========================
    wait.until(
        EC.element_to_be_clickable((By.ID, radio_id))
    ).click()


    # =========================
    # プルダウン（固定：東海BL）
    # =========================
    Select(driver.find_element(By.ID, "e_10667")) \
        .select_by_visible_text("東海BL")


    # =========================
    # 次へボタン
    # =========================
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='__send' and contains(@value,'次へ')]")
        )
    ).click()


    # =========================
    # 2ページ目待機
    # =========================
    wait.until(
        EC.presence_of_element_located((By.NAME, "__commit"))
    )


    # =========================
    # 送信ボタン
    # =========================
    time.sleep(random.uniform(2, 5))

    wait.until(
        EC.element_to_be_clickable((By.NAME, "__commit"))
    ).click()


    # =========================
    # 完了待機
    # =========================
    time.sleep(3)

    print("送信完了")


except Exception as e:
    print("エラー:", e)
    raise

finally:
    driver.quit()
