import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# * Cronjob that wakes up the streamlit apps
urls = {
    "bubble_tea": "https://dssq-bubble-tea-m9jzmospevfsw8uh2ncz4o.streamlit.app/",
    "easyessay_master": "https://easyessay-literature-review-toolkit-wally.streamlit.app/",
    "easyessay_guest": "https://easyessay-literature-review-toolkit-guest.streamlit.app/",
    "iii_Demand_Foresight_Tools (dev)": "https://demand-foresight-trend-report-generator-dev.streamlit.app/",
    "iii_Demand_Foresight_Tools (main)": "https://demand-foresight-trend-report-generator-main.streamlit.app/",
    "Taiwan Media Dashboard": "https://taiwan-media-dashboard-tool.streamlit.app/",
    "README agent": "https://readme-compile-agent.streamlit.app/",
    "Tic Tac Toe": "https://tic-tac-toe-with-agent.streamlit.app/",
    "Financial Dashboard": "https://taiwan-financialdashboard.streamlit.app/",
    # "Minesweeper": "https://minesweeper-wh.streamlit.app/",
}

# Text on the button Streamlit shows on a sleeping app
WAKE_BUTTON_XPATH = "//button[contains(., 'get this app back up')]"


def get_driver():
    chrome_options = Options()
    # 新版 headless 模式，比舊版穩定
    chrome_options.add_argument("--headless=new")
    # 解決 Linux 權限與資源限制問題
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # 省記憶體：關掉擴充功能、不載入圖片、限制 renderer 數量、限制 JS heap
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--renderer-process-limit=1")
    chrome_options.add_argument("--js-flags=--max-old-space-size=128")
    chrome_options.add_argument("--window-size=800,600")
    # 不等整頁資源載完，DOM 好了就繼續
    chrome_options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)
    return driver


def wake(title, url):
    # 每個 app 開一個新的 Chrome，用完就關，記憶體不會一直累積
    driver = None
    try:
        driver = get_driver()
        driver.get(url)
        try:
            button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, WAKE_BUTTON_XPATH))
            )
            button.click()
            time.sleep(5)  # 給 Streamlit 一點時間開始重啟
            print(f"✅ '{title}' was asleep and has been woken up")
        except TimeoutException:
            print(f"✅ '{title}' is already awake")
    except Exception as e:
        # 單一 app 失敗不會中斷整個排程
        print(f"❌ '{title}' failed: {type(e).__name__}: {e}")
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    for title, url in urls.items():
        wake(title, url)
