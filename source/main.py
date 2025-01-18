# LIBs SETUP
import requests
from bs4 import BeautifulSoup
import numpy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import psutil



# CONFIGURATION SET UP
BROWSERPROCNAME = "chrome.exe"

## Website reference and hooks
 ### URL SITE
MAIN_URL = "https://listingcenter.nasdaq.com/rulebook/nasdaq/rulefilings"
DRIVER_PATH = "/usr/local/bin/chromedriver"
 ### HTML ID of the main table where to get data
sDesiredTabTag = "NASDAQ-tab-2025"
sIdMainTable = "NASDAQ-tab-2025"

##
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == BROWSERPROCNAME:
        proc.kill()

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.




# MAIN ROUTINE

## WEBSITE OPENING

driver.get(MAIN_URL)
request = requests.get(MAIN_URL)
soup = BeautifulSoup(request.content, 'html.parser')

## DATA GATHERING
### Force tab selection on last year
objDesiredTab = driver.find_element(By.XPATH,"//li[@data-tab='"+sDesiredTabTag+"']")
if objDesiredTab.get_attribute("class") != "tab-link current":
    objDesiredTab.click()

objSDesiredTab = soup.find_all("li", {"class": "tab-link", "data-tab":sDesiredTabTag})

objDesiredTable = driver.find_element(By.XPATH,"//div[@id='"+sIdMainTable+"']/table")


## DATA CLEANING
# empty dictionary to store data, could be a list of anything. i just like dicts
tabData = pd.DataFrame(columns=['Name', 'Link', 'Description'])
#tabData = pd.read_html(objDesiredTable.get_attribute("outerHTML"))[0]
row_list = []

countDATA = 0
for row in objDesiredTable.find_elements(By.TAG_NAME,"tr"):
    dictrow=  {"name": "",
                "link": "",
                "description": ""}
    
    cells = row.find_elements(By.TAG_NAME,"td")
    if len(cells)>0:
        dataRow = [cells[0].text,cells[0].find_element(By.TAG_NAME,"a").get_attribute("href"),cells[1].text]
        dictrow.update({"name":cells[0].text})
        dictrow.update({"link":cells[0].find_element(By.TAG_NAME,"a").get_attribute("href")})
        dictrow.update({"description":cells[1].text})
        row_list.append(dictrow)
        
        #tabData.iloc(countDATA) = dataRow
        countDATA = countDATA + 1

tabData = pd.DataFrame(row_list)
## DATA PUBLISHING
# do whats needed with data
print(tabData)

tabData.to_excel("./output/output.xlsx")
tabData.to_csv("./output/output.csv")
##













## REPORTING 


# CLEAN & CLOSE