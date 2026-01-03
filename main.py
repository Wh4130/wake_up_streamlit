import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver():
    chrome_options = Options()
    
    # 關鍵：雲端環境必須開啟 headless 模式
    chrome_options.add_argument("--headless") 
    
    # 關鍵：解決 Linux 權限與資源限制問題
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu") # 雲端無顯示卡

    # 如果是在 Render 部署，通常需要指定 Chrome 執行檔路徑（視安裝方式而定）
    # chrome_options.binary_location = "/usr/bin/google-chrome" 

    driver = webdriver.Chrome(options=chrome_options)
    return driver

# * Cronjob that wakes up the streamlit apps
urls = {
        "bubble_tea": "https://dssq-bubble-tea-m9jzmospevfsw8uh2ncz4o.streamlit.app/",

        "easyessay_master": "https://easyessay-literature-review-toolkit-wally.streamlit.app/",

        "easyessay_guest": "https://easyessay-literature-review-toolkit-guest.streamlit.app/",

        "iii_Demand_Foresight_Tools (dev)": "https://demand-foresight-trend-report-generator-dev.streamlit.app/",

        "iii_Demand_Foresight_Tools (main)": "https://demand-foresight-trend-report-generator-main.streamlit.app/",
        
        "Taiwan Media Dashboard": "https://taiwan-media-dashboard-tool.streamlit.app/",
        
        "Tic Tac Toe": "https://tic-tac-toe-with-agent.streamlit.app/",
        
        "Minesweeper": "https://minesweeper-wh.streamlit.app/"}



for title, url in urls.items():
    driver = get_driver()

    # Open a web page
    driver.get(url)

    # Explicit wait then click the wake up button
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
        driver.find_element(By.TAG_NAME, 'button').click()
        print(f"'{title}' is awaken!")
    except Exception as E:
        print(E)

    # Close the browser
    driver.quit()
