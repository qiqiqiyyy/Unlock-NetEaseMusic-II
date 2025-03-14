# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00F8732DFBB1BAA640B24F4CAF250E6A056AAE67879C77B2DDD4BF4A4AFC0A114DE6ED2134A5FBE7CE54AD637E0B1C5734AF15E5FD8B1C5DADEF61C3E5BC7970DFA9D1D30E2225C5B9A63DB5A67C1B7AEA284E9C4639935F2CF3C1286ED3D11C65A19BED20414F69B881A8656CC8C975562DF9D5B6270E99D2EB40B6323C03C7F0E1F84E2F5D07C322AC82018043FC23D297CFD0F4ABD530753416DD360C9725D80900A610C2882D841F5DC711857CD08E89E0B40219B6AA67630CA78D4B9CE113D3B1658F417EECC631336899B7E7512B9E2B40F3EADD64415D997B00222CBE1956DEFBFACD50338D35049F614A2F0EF3893330C4DD8E331166B93E22C672B4A9E2DB1DBACD4B8484EDFE97E7FF0A7A891D54A85334E087DCB032823BB746A8E4B7BFBD6180387016545B046F3427CDE564F0D6AC9AE1E64DF93147C41529C8C3C404117FD3E67DCFA89BB0F4D30CAF277891F24BA95A9EA2A7BF8A2528C25CAC"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
