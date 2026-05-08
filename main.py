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
# GitHub Secrets
# =========================
EMPLOYEE = os.getenv("EMPLOYEE_NUMBER")
LAST_NAME = os.getenv("FORM_LAST_NAME")
FIRST_NAME = os.getenv("FORM_FIRST_NAME")
EMAIL = os.getenv("FORM_EMAIL")
OFFICE = os.getenv("OFFICE")


# =========================
# 現在時刻
# =========================
now = datetime.now(ZoneInfo("Asia/Tokyo"))
today = now.date()
hour = now.hour


# =========================
# 実行期間制限
# =========================
start_date = date(2026, 5, 7)
end_date = date(2026, 5, 22)

if not (start_date <= today <= end_date):
    print("対象期間外")
    exit()


# =========================
# 時間帯判定（ラジオ）
# =========================
radio_id = None

if hour == 10:
    radio_id = "tmp_0"
elif hour == 13:
    radio_id = "tmp_1"
elif hour == 16:
    radio_id = "tmp_2"
else:
    print("対象時間外")
    exit()

if radio_id is None:
    print("radio未設定")
    exit()


# =========================
# ★ここが重要：2〜18分ランダム遅延
# =========================
delay_sec = random.randint(2 * 60, 18 * 60)

print(f"送信まで待機: {delay_sec}秒")
time.sleep(delay_sec)


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
    next_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='__send' and contains(@value,'次へ')]")
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        next_btn
    )


    # =========================
    # 2ページ目待機
    # =========================
    commit_btn = wait.until(
        EC.element_to_be_clickable((By.NAME, "__commit"))
    )

    time.sleep(random.uniform(2, 5))

    # =========================
    # 送信
    # =========================
    driver.execute_script(
        "arguments[0].click();",
        commit_btn
    )

    print("送信完了")


except Exception as e:
        print("エラー:", e)
        raise

finally:
        driver.quit()
