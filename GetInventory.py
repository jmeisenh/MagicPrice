#!/usr/bin/env python
# coding: utf-8

# In[ ]:



# In[35]:


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

PATH = "C:/Users/Justin Meisenhelter/Projects/MagicPrice/geckodriver.exe"
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
m = driver.find_element("link text", "Tools")
a.move_to_element(m).perform()
#click export
n = driver.find_element("link text", "Export")
a.move_to_element(n).click().perform()
time.sleep(1)

# click on extra columns button to expand list
driver.find_element("id", "extra_columns_container").click()
time.sleep(1)
# click on price
driver.find_element("link text", "Price").click()
#click on rarity
driver.find_element("link text", "Rarity").click()
# click on type
driver.find_element("xpath", "/html/body/div[12]/div[1]/ul/li[1]/a").click()
# click on cost
driver.find_element("xpath", "/html/body/div[12]/div[1]/ul/li[2]/a").click()
# done button
driver.find_element("xpath", "/html/body/div[12]/div[2]/div").click()
time.sleep(1)
# finish export
driver.find_element("css selector", "button.btn-primary:nth-child(7)").click()
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

# Import Data
importDir = r'C:\Users\Justin Meisenhelter\Projects\MagicPrice\Exports' + '\\' + datetime.today().strftime('%Y-%m-%d') + '.csv'
df = pd.read_csv(importDir)
# Keep only usable columns
df = df[['Count', 'Name', 'Edition', 'Card Number', 'Condition', 'Language', 'Foil', 'Type', 'Cost', 'Rarity', 'Price']]

# Add Color Column
#eliminate duplicates in Color Column
df['Color'] = df['Cost'].astype('string')
# fill nas with temporary value
df['Color'] = df.Color.fillna('Z')
df['Color'] = df.Color.apply(lambda x: "".join(sorted(set(x))))

# Replace brackets, X , C, and phyrexian mana with space
for i in ['[^A-Z]', 'X', 'P', 'C']:
    df['Color'] = df['Color'].str.replace(i, '')

#create color replacement dictionary

colorDict = {
    r'\bB\b' : 'Black',
    r'\bU\b' : 'Blue', 
    r'\bG\b' : 'Green', 
    r'\bR\b' : 'Red',
    r'\bW\b' : 'White',
    r'\b[BU]{2}\b' : 'Dimir',
    r'\b[BG]{2}\b' : 'Golgari',
    r'\b[BR]{2}\b' : 'Rakdos',
    r'\b[BW]{2}\b' : 'Orzhov',
    r'\b[UG]{2}\b' : 'Simic',
    r'\b[UR]{2}\b' : 'Izzit',
    r'\b[UW]{2}\b' : 'Azorius',
    r'\b[GR]{2}\b' : 'Gruul',
    r'\b[GW]{2}\b' : 'Selesnya',
    r'\b[RW]{2}\b' : 'Boros',
    r'\b[UGW]{3}\b' : 'Bant',
    r'\b[WBR]{3}\b' : 'Mardu',
    r'\b[UBR]{3}\b' : 'Grixis',
    r'\b[BRG]{3}\b' : 'Jund',
    r'\b[RGW]{3}\b' : 'Naya',
    r'\b[WBG]{3}\b' : 'Abzan',
    r'\b[URW]{3}\b' : 'Jeskai',
    r'\b[BGU]{3}\b' : 'Sultai',
    r'\b[GUR]{3}\b' : 'Temur',
    r'\b[WUB]{3}\b' : 'Esper',
    r'\b[WUBR]{4}\b' : 'Yore-Tiller',
    r'\b[UBRG]{4}\b' : 'Glint-Eye',
    r'\b[BRGW]{4}\b' : 'Dune-Brood',
    r'\b[RGWU]{4}\b' : 'Ink-Treader',
    r'\b[GWUB]{4}\b' : 'Witch-Maw',
    r'\b[WUBRG]{5}\b' : 'Dominion',
    r'\bZ\b' : 'Colorless'
    
}
for key, value in colorDict.items():
    df['Color'] = df['Color'].str.replace(key, value)
# all remaining empty cells will be colorless
df['Color'] = df['Color'].str.replace(r'^\s*$', 'Colorless')
# Save file
dst_path = r'C:\Users\Justin Meisenhelter\Projects\MagicPrice\Exports'
df.to_csv(dst_path + '\\' + 'Cleaned_' + datetime.today().strftime('%Y-%m-%d') + '.csv', index = False)
# remove old uncleaned file
os.remove(dst_path + '\\' + datetime.today().strftime('%Y-%m-%d') + '.csv')

# Take existing wide format full inventory and add new column with todays prices
AllCardsWide =  pd.read_csv(dst_path + '\\' + 'AllCardsWide.csv')
# The following line will not be necesarry in script (df is already defined)
df = pd.read_csv(dst_path + '\\' + 'Cleaned_' + datetime.today().strftime('%Y-%m-%d') + '.csv')
# merge dfs
mergeDF = pd.merge(AllCardsWide, df, how = 'left', on = ['Name', 'Edition', 'Card Number', 'Condition', 'Language', 'Foil'], suffixes=('', '_remove'))
# drop original count column, and rename new count column
mergeDF.drop('Count', axis = 1, inplace = True)
# rename count_remove to count and move to first column
mergeDF.rename(columns = {'Count_remove' : 'Count'}, inplace = True)
mergeDF = mergeDF[['Count'] + [x for x in mergeDF.columns if x != 'Count']]
# rename newest price column and move to end
mergeDF.rename(columns = {'Price' : datetime.today().strftime('%Y-%m-%d')}, inplace = True)
cols = list(mergeDF.columns.values) 
cols.pop(cols.index(datetime.today().strftime('%Y-%m-%d'))) 
mergeDF = mergeDF[cols+[datetime.today().strftime('%Y-%m-%d')]] 
# remove all right hand columns
mergeDF.drop([j for j in mergeDF.columns if 'remove' in j],axis=1, inplace=True)
mergeDF.drop([j for j in mergeDF.columns if '.1' in j],axis=1, inplace=True)
# save new wideformat csv
mergeDF.to_csv(dst_path + '\\' + 'AllCardsWide.csv', index = False)
# Save new long format csv
pd.melt(mergeDF, id_vars=list(mergeDF.columns)[0:11] , value_vars=list(mergeDF.columns)[11:], 
                     var_name= 'Date', value_name='Price', ignore_index=False).sort_values(['Name', 'Date']).to_csv(dst_path + '\\' + 'AllCardsLong.csv', index = False) 













