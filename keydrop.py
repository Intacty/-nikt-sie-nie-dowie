from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import datetime
import undetected_chromedriver as uc
import sys

options = uc.ChromeOptions()
options=options

driver = uc.Chrome(
    options = options , version_main = 112
    )

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

options.add_argument('--lang=pl-PL')
options.add_argument('--disable-tracking')
options.add_argument("--timezone=Poland/Warsaw")

stealth(driver,
        languages=["pl-PL", "PL"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

window_handle = driver.window_handles[0]
driver.switch_to.window(window_handle)
driver.set_window_position(0, 0)
screen_width = driver.execute_script("return window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;")
screen_height = driver.execute_script("return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;")
driver.set_window_size(screen_width // 2, screen_height)

def internal_error(driver, cookies):
    try:
        wait = WebDriverWait(driver, 3)
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#giveaways-root > div > div > div > button > span")))
        print("[CONSOLE] Strona jest zbugowana jak skurwynsyn i wystartowała z błędem BRUH")
        driver.refresh()
        driver.refresh()
        driver.refresh()
        driver.refresh()
        driver.refresh()
        driver.refresh()
        driver.refresh()
        return
    except Exception as e:
        print("[CONSOLE] Strona działa poprawnie")

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

        while retries < max_retries:
            try:
                find_giveaway = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[3]/div[2]/div[5]/div/div/div/div[2]/a')))
                find_giveaway.click()
                print("[CONSOLE] [{}] Giveaway został znaleziony".format(datetime.datetime.now().strftime("%H:%M:%S")))
                break
            except Exception as e:
                print("[CONSOLE] [{}] Błąd podczas znajdowania giveawaya".format(str(e)))
                retries += 1

        if retries == max_retries:
            print("[CONSOLE] Nie udało się znaleźć giveawaya, odswiezam stronę".format(max_retries))
            driver.get('https://key-drop.com/pl/giveaways/list')
            time.sleep(2)
            driver.refresh()
        return

def join_giveaway(driver, cookies):
    while True:
        max_retries = 1
        retries = 0

        while retries < max_retries:
            try:
                join_giveaway = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.button')))
                join_giveaway.click()
                print("[CONSOLE] [{}] Dołączono do giveawaya".format(datetime.datetime.now().strftime("%H:%M:%S")))
                break
            except Exception as e:
                print("[CONSOLE] [{}] Błąd podczas dołączania do giveawaya".format(str(e)))
                retries += 1

        if retries == max_retries:
            print("[CONSOLE] Nie udało się dołączyć do giveawaya, odswiezam stronę".format(max_retries))
            driver.get('https://key-drop.com/pl/giveaways/list')
            time.sleep(2)
            driver.refresh()
        return

def ended_giveaway(driver, cookies):
    while True:
        max_retries = 1
        retries = 0

        while retries < max_retries:
            try:
                wait = WebDriverWait(driver, 999)
                ended_giveaway = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#giveaway-drawing-winners")))
                print("[CONSOLE] [{}] Wygrana osoba została wylosowana, wracam do strony głównej".format(datetime.datetime.now().strftime("%H:%M:%S")))
                break
            except Exception as e:
                print("[CONSOLE] [{}] Nie udało się wyłonić zwycięzcy: {}".format(str(e)))
                retries += 1

        if retries == max_retries:
            print("[CONSOLE] [{}] Nie udało się wyłonić zwycięzcy, odswiezam stronę".format(max_retries))
            driver.get('https://key-drop.com/pl/giveaways/list')
            time.sleep(2)
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

    time.sleep(3)

    find_giveaway(driver, cookies)
    driver.refresh()

    join_giveaway(driver, cookies)

    ended_giveaway(driver, cookies)
    driver.refresh()

    time.sleep(10)
