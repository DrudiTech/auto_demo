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



####### BEAUTIFUL SOUP
# Wrong object, should get the children
# objSDesiredTbl = soup.find_all("li", {"class": "tab-link", "data-tab":sDesiredTabTag})


objDesiredTable = driver.find_element(By.XPATH,"//div[@id='"+sIdMainTable+"']/table")

# f = open("oHTML.txt", "a")
# f.write(str(objDesiredTable))
# f.close()

g = open("raw_text.txt", "a")
g.write(objDesiredTable.get_attribute("outerHTML"))
g.close()


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