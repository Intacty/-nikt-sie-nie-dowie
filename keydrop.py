from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time

driver_path = 'C:/Users/geting/Downloads/chromedriver_win32/chromedriver.exe'

service = Service(executable_path=driver_path)
service.start()

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=service, options=options)

with open('cookies.json', 'r') as f:
    cookies = json.load(f)

while True:
    driver.get('https://key-drop.com/en/giveaways/list')

    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(10)
    find_giveaway = driver.find_element(By.CSS_SELECTOR, 'div.relative:nth-child(5) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')
    find_giveaway.click()
    print("[CONSOLE] Giveaway został znaleziony")

    time.sleep(3)
    join_giveaway = driver.find_element(By.CSS_SELECTOR, 'div.relative:nth-child(4) > div:nth-child(1)')
    join_giveaway.click()
    print("[CONSOLE] Dołączono do giveawaya")
    
    time.sleep(5)
    driver.refresh()

    try:
        wait = WebDriverWait(driver, 999)
        first_giveaway = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li.relative:nth-child(1) > div:nth-child(1)")))
        print("[CONSOLE] Wygrana osoba została wylosowana, wracam do strony głównej")
    except:
        print("CSS selector not found")

    time.sleep(5)
