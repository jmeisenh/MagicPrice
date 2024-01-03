from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import glob
import os.path
import shutil
import keyring
from datetime import datetime

username = "jmeisenh"
password = keyring.get_password('magic', 'jmeisenh')
options = Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"

PATH = "C:/Users/jmeis/Projects/MagicPrice/geckodriver.exe"
driver = webdriver.Firefox(executable_path=PATH, options = options)

driver.get("https://deckbox.org/accounts/login?return_to=/sets/3285758")
driver.maximize_window()
# Find username, wait and send username
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login"))).send_keys(username)

# find password input field and insert password
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)

# click login button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit_button"))).click()
#driver.find_element_by_id("submit_button").click()
time.sleep(2)
a = ActionChains(driver)
#activate tools hover menu
m = driver.find_element(By.LINK_TEXT, 'Tools')
a.move_to_element(m).perform()
#click export
n = driver.find_element(By.LINK_TEXT, "Export")
a.move_to_element(n).click().perform()
time.sleep(1)

# click on extra columns button to expand list
driver.find_element(By.ID, "extra_columns_container").click()
time.sleep(1)
#driver.switch_to_default_content()
# click on price
driver.find_element(By.LINK_TEXT, "Price").click()
#click on rarity
driver.find_element(By.LINK_TEXT, "Rarity").click()
# click on type
driver.find_element(By.XPATH, "/html/body/div[9]/div[1]/ul/li[2]/a").click()
# click on cost
driver.find_element(By.XPATH, "/html/body/div[9]/div[1]/ul/li[3]/a").click()
# done button
driver.find_element(By.XPATH, "/html/body/div[9]/div[2]/div").click()
time.sleep(1)
# finish export
driver.find_element(By.CSS_SELECTOR, "button.btn-primary:nth-child(7)").click()
# quit instance
time.sleep(3)
driver.quit()

# identify new exported file
src_path = r'C:\Users\Justin Meisenhelter\Downloads'
file_type = r'\*csv'
files = glob.glob(src_path + file_type)
max_file = max(files, key=os.path.getctime)

#move file to working directory
file_name = os.path.basename(max_file)
dst_path = r'C:\Users\Justin Meisenhelter\Projects\MagicPrice\Exports'
shutil.move(max_file, dst_path+ '\\' +datetime.today().strftime('%Y-%m-%d') + '.csv')