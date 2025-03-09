# LIBs SETUP
import requests
from bs4 import BeautifulSoup
import numpy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import psutil
import shutil
import requests
from urllib.request import urlretrieve
import zipfile
import os
from chromever import *
from seleniumwrapper import *

#import pytest
import time
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait





# CONFIGURATION SET UP
BROWSERPROCNAME = "chrome.exe"

## Website reference and hooks
 ### URL SITE
MAIN_URL = "https://listingcenter.nasdaq.com/rulebook/nasdaq/rulefilings"
FORM_URL ="https://testpages.eviltester.com/styled/basic-html-form-test.html"
DRIVER_PATH = "/usr/local/bin"

vvv = get_chrome_version()


### CHROME DRIVER UPDATE ROUTINE
# get the latest chrome driver version number
url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
response = requests.get(url)
version_number = vvv #response.text

# build the donwload url
#download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_mac64.zip"
download_url = "https://storage.googleapis.com/chrome-for-testing-public/" + version_number +"/mac-x64/chromedriver-mac-x64.zip"
# download the zip file using the url built above
latest_driver_zip = urlretrieve(download_url,'chromedriver.zip')


# extract the zip file
with zipfile.ZipFile(latest_driver_zip[0], 'r') as zip_ref:
    zip_ref.extractall(DRIVER_PATH) # you can specify the destination folder path here
# delete the zip file downloaded above
os.remove(latest_driver_zip[0])
shutil.move(DRIVER_PATH + '/' + 'chromedriver-mac-x64' + '/' +'chromedriver',DRIVER_PATH + '/' +'chromedriver')
#.(DRIVER_PATH + '/' + 'chromedriver-mac-x64')

########################

 
##
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == BROWSERPROCNAME:
        proc.kill()

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.




# MAIN ROUTINE

## WEBSITE OPENING

driver.get(FORM_URL)
request = requests.get(FORM_URL)
soup = BeautifulSoup(request.content, 'html.parser')

## FORM FILLING

weWriting = driver.find_element(By.XPATH,"//input[@name='username']")
if weWriting.get_attribute("type") == "text":
    weWriting.send_keys("Paolo")


weWriting = driver.find_element(By.XPATH,"//input[@name='password']")
if weWriting.get_attribute("type") == "password":
    weWriting.send_keys("secret")


weWriting = driver.find_element(By.XPATH,"//textarea[@name='comments']")
weWriting.send_keys("This is a simple comment to show you i can write quite a bit :)")


weButton = waitElementByXPath(driver,"//input[@name='submitbutton']",3,10)
if weButton.get_attribute("tag_name") == "input":
    weWriting.click()


# CHECK SUBMIT
weTitle =waitElementByXPath(driver,"//div/h2[text()='Submitted Values']",3,10)





## DATA CLEANING
# empty dictionary to store data, could be a list of anything. i just like dicts
tblData = pd.DataFrame(columns=['Name', 'Link', 'Description'])
#tabData = pd.read_html(objDesiredTable.get_attribute("outerHTML"))[0]
lRows = []

countDATA = 0
for iRow in objDesiredTable.find_elements(By.TAG_NAME,"tr"):
    dictRow=  {"name": "",
                "link": "",
                "description": ""}
    
    aCells = iRow.find_elements(By.TAG_NAME,"td")
    if len(aCells)>0:
        dictRow.update({"name":aCells[0].text})
        dictRow.update({"link":aCells[0].find_element(By.TAG_NAME,"a").get_attribute("href")})
        dictRow.update({"description":aCells[1].text})
        lRows.append(dictRow)
        
        #tabData.iloc(countDATA) = dataRow
        countDATA = countDATA + 1

tblData = pd.DataFrame(lRows)
## DATA PUBLISHING
# do whats needed with data
print(tblData)

#tabData.to_excel("./output/output.xlsx")
tblData.to_csv("./output/output.csv")
##




## REPORTING 


# CLEAN & CLOSE