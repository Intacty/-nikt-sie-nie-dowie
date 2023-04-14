from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import json
import time
import datetime
import undetected_chromedriver as uc

options = uc.ChromeOptions()
options=options

options.add_argument('--load-extension={}'.format(r'C:\Users\geting\AppData\Local\Google\Chrome\User Data\Default\Extensions\ifibfemgeogfhoebkmokieepdoobkbpo\3.3.3_0'))
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--lang=pl-PL')
options.add_argument('--disable-tracking')
options.add_argument('--timezone=Poland/Warsaw')

driver = uc.Chrome(options = options , version_main = 112)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

stealth(driver,
        languages=["pl-PL", "PL"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.set_window_position(0, 0)
screen_width = driver.execute_script("return window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;")
screen_height = driver.execute_script("return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;")
driver.set_window_size(screen_width // 2, screen_height)

def internal_error(driver, cookies):
    try:
        wait = WebDriverWait(driver, 3)
        while True:
            try:
                element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#giveaways-root > div > div > div > button > span")))
                print("[CONSOLE] Strona jest zbugowana jak skurwynsyn i wystartowała z błędem BRUH")
                driver.refresh()
            except TimeoutException:
                print("[CONSOLE] Strona działa poprawnie")
                break
        return
    except Exception as e:
        print("[CONSOLE] Wystąpił inny błąd:", e)

def drawing_is_started(driver, cookies):
    try:
        wait = WebDriverWait(driver, 3) # wait for 3 seconds
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.relative:nth-child(5) > div:nth-child(1) > a:nth-child(1) > p:nth-child(2)")))
        print("[CONSOLE] Giveaway się już rozpoczął, wznawiam kod aby uniknąć błędów")
        driver.refresh()
        return
    except:
        print("[CONSOLE] Giveaway się jeszcze nie rozpoczął")

def find_giveaway(driver, cookies):
    while True:
        max_retries = 1
        retries = 0
        found_giveaway = False

        while retries < max_retries:
            try:
                find_giveaway = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[3]/div[2]/div[5]/div/div/div/div[2]/a')))
                find_giveaway.click()
                print("[CONSOLE] [{}] Giveaway został znaleziony".format(datetime.datetime.now().strftime("%H:%M:%S")))
                found_giveaway = True
                break
            except Exception as e:
                print("[CONSOLE] [{}] Błąd podczas znajdowania giveawaya".format(str(e)))
                retries += 1

            if retries == max_retries:
                print("[CONSOLE] Nie udało się znaleźć giveawaya, odswiezam stronę".format(max_retries))
                driver.get('https://key-drop.com/pl/giveaways/list')
                driver.refresh()
                retries = 0
            return
        if found_giveaway:
            break

def join_giveaway(driver, cookies):
    while True:
        max_retries = 1
        retries = 0
        joined_giveaway = False

        while retries < max_retries:
            try:
                join_giveaway = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div > div.flex.flex-col.gap-4 > div.flex.flex-1.flex-col > div.relative > div > button > svg')))
                join_giveaway.click()
                print("[CONSOLE] [{}] Dołączono do giveawaya".format(datetime.datetime.now().strftime("%H:%M:%S")))
                joined_giveaway = True
                break
            except Exception as e:
                print("[CONSOLE] [{}] Błąd podczas dołączania do giveawaya".format(str(e)))
                retries += 1

            if retries == max_retries:
                print("[CONSOLE] Nie udało się dołączyć do giveawaya, odswiezam stronę".format(max_retries))
                driver.get('https://key-drop.com/pl/giveaways/list')
                driver.refresh()
                retries = 0
            return
        if joined_giveaway:
            break

def ended_giveaway(driver, cookies):
    while True:
        max_retries = 1
        retries = 0

        while retries < max_retries:
            try:
                wait = WebDriverWait(driver, 900)
                ended_giveaway = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#giveaway-drawing-winners > h3")))
                print("[CONSOLE] [{}] Wygrana osoba została wylosowana, wracam do strony głównej".format(datetime.datetime.now().strftime("%H:%M:%S")))
                break
            except Exception as e:
                print("[CONSOLE] Nie udało się wyłonić zwycięzcy".format(str(e)))
                retries += 1

        if retries == max_retries:
            print("[CONSOLE] Nie udało się wyłonić zwycięzcy, odswiezam stronę".format(max_retries))
            driver.get('https://key-drop.com/pl/giveaways/list')
            driver.refresh()
        return

with open('cookies.json', 'r') as f:
    cookies = json.load(f)

while True:
    driver.get('https://key-drop.com/pl/giveaways/list')

    for cookie in cookies:
        driver.add_cookie(cookie)

    internal_error(driver, cookies)
    drawing_is_started(driver, cookies)
    time.sleep(5)
    find_giveaway(driver, cookies)
    driver.refresh()
    join_giveaway(driver, cookies)
    ended_giveaway(driver, cookies)
    time.sleep(10)
