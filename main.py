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

# Secrets確認
if not all([EMPLOYEE, LAST_NAME, FIRST_NAME, EMAIL, OFFICE]):
    print("Secrets不足")
    exit()


# =========================
# 現在時刻（JST）
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
# workflow側は55分起動
# ここでどの送信か決定
# =========================
radio_id = None

# 09:55〜 → 10時送信枠
if hour == 9:
    radio_id = "tmp_0"

# 12:55〜 → 13時送信枠
elif hour == 12:
    radio_id = "tmp_1"

# 15:55〜 → 16時送信枠
elif hour == 15:
    radio_id = "tmp_2"

else:
    print("対象時間外")
    exit()


# =========================
# ランダム待機
# 5〜23分
# =========================
delay_sec = random.randint(5 * 60, 23 * 60)

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

    wait.until(
        EC.presence_of_element_located((By.ID, "e_10663"))
    )


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
    # プルダウン
    # 固定：東海BL
    # =========================
    Select(
        driver.find_element(By.ID, "e_10667")
    ).select_by_visible_text("東海BL")


    # =========================
    # 次へ
    # =========================
    next_btn = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//input[@name='__send' and contains(@value,'次へ')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        next_btn
    )

    time.sleep(1)


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
