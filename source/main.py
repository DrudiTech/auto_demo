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

weWriting = waitElementByXPath(driver,"//input[@name='username']",3,10)
if weWriting.get_attribute("type") == "text":
    weWriting.clear()
    weWriting.send_keys("Paolo")


weWriting = waitElementByXPath(driver,"//input[@name='password']",3,10)
if weWriting.get_attribute("type") == "password":
    weWriting.clear()
    weWriting.send_keys("secret")


weWriting = waitElementByXPath(driver,"//textarea[@name='comments']",3,10)
weWriting.clear()
weWriting.send_keys("This is a simple comment to show you i can write quite a bit :)")


weButton = waitElementByXPath(driver,"//input[@value ='submit']",3,10)
weButton.click()


# CHECK SUBMIT
weTitle =waitElementByXPath(driver,"//div/h2[text()='Submitted Values']",3,10)

weResultForm = waitElementByXPath(driver, "//div[@class='centered form-results']")
#weAllResultsValue = waitChildrenElementByXPath(weResultForm, "//li")
#weAllResultsField = waitChildrenElementByXPath(weResultForm, "//p/strong")

weAllResultsCell = waitChildrenElementByXPath(weResultForm,"./div")

tblDataResult = pd.DataFrame(columns=['Field', 'Value'])
lRows = []

for i in range(len(weAllResultsCell)):
    dictRow = {"Field":"",
                "Value":""}
    try:
        weField = waitChildrenElementByXPath(weAllResultsCell[i], "./p/strong")[0]
    except:
        next

    dictRow.update({"Field":weField.text})
    if weAllResultsCell[i].get_attribute("data-hasvalue") == "yes":
        dictRow.update({"Value":waitChildrenElementByXPath(weAllResultsCell[i], "./ul/li")[0].text})
    lRows.append(dictRow)
        
tblDataResult = pd.DataFrame(lRows)



## DATA PUBLISHING
# do whats needed with data
print(tblDataResult)

#tabData.to_excel("./output/output.xlsx")
tblDataResult.to_csv("./output/output.csv")
##




## REPORTING 


# CLEAN & CLOSE