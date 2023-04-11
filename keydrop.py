from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import datetime

driver_path = 'chromedriver.exe'

service = Service(executable_path=driver_path)
service.start()

options = Options()
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--load-extension={}'.format(r'C:\Users\geting\AppData\Local\Google\Chrome\User Data\Default\Extensions\mpbjkejclgfgadiemmefgebjfooflfhl\2.0.1_0'))
options.add_experimental_option('excludeSwitches', ['enable-logging'])
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(service=service, options=options)

with open('cookies.json', 'r') as f:
    cookies = json.load(f)

while True:
    driver.get('https://key-drop.com/en/giveaways/list')

    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(3)

    driver.refresh()
    driver.refresh()

    try:
        find_giveaway = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.relative:nth-child(5) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')))
        find_giveaway.click()
        print("[CONSOLE] Giveaway został znaleziony")
    except:
        print("[CONSOLE] Błąd podczas znajdowania giveawaya")

    time.sleep(3)

    try:
        join_giveaway = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.button')))
        join_giveaway.click()
        print("[CONSOLE] Dołączono do giveawaya - {}".format(datetime.datetime.now().strftime("%H:%M:%S")))
    except:
        print("[CONSOLE] Błąd podczas dołączania do giveawaya")

    try:
        wait = WebDriverWait(driver, 999)
        first_giveaway = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#giveaway-drawing-winners")))
        print("[CONSOLE] Wygrana osoba została wylosowana, wracam do strony głównej")
    except:
        print("[CONSOLE] CSS selector not found")

    driver.refresh()
    time.sleep(20)
