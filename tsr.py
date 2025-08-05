import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# TSR Cinemax URL and target date
MOVIE_URL = "https://www.tsrcinemax.asia/Home/Detail?movieID=1000000392"
SDATE = "8/14/2025"           # The actual date in the HTML attribute
DISPLAY_DATE = "14 / 8"       # For your alert message

# Your Telegram Bot details
BOT_TOKEN = "8308850437:AAF4I6gQxu6XSct447sx-Ds1iqPFz8CFkBU"
CHAT_ID = "769278137"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("[Telegram] Notification sent successfully.")
        else:
            print(f"[Telegram] Failed to send notification. Status: {response.status_code}")
    except Exception as e:
        print(f"[Telegram] Error sending message: {e}")

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def check_showtime():
    driver = setup_driver()
    driver.get(MOVIE_URL)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@sdate='{SDATE}']"))
        )
        found = True
    except:
        found = False
    driver.quit()
    return found

def main():
    print(f"Monitoring TSR Cinemax for showtime on {DISPLAY_DATE}...")
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            if check_showtime():
                message = (
                    f"🎬 TSR Cinemax Update\n"
                    f"Showtime for *{DISPLAY_DATE}* is now available!\n"
                    f"{MOVIE_URL}"
                )
                print(f"[{now}] Showtime found! Sending Telegram alert...")
                send_telegram_alert(message)
                break
            else:
                print(f"[{now}] Not yet available. Checking again in 60 seconds...")
        except Exception as e:
            print(f"[{now}] Error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
