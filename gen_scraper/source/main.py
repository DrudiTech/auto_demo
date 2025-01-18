# MAIN SCRIPT SETUP
import requests
from bs4 import BeautifulSoup
import pandas as pd

# CONFIGURATION SET UP
## Website reference and hooks
 ### URL SITE
MAIN_URL = "https://listingcenter.nasdaq.com/rulebook/nasdaq/rulefilings"
 ### HTML ID of the main table where to get data
sIdMainTable = "NASDAQ-tab-2025"

# MAIN ROUTINE

## WEBSITE OPENING
request = requests.get(MAIN_URL)
soup = BeautifulSoup(request.content, 'html.parser')

## DATA GATHERING
### Force tab selection on last year
objDesiredTab = soup.find_all("li", {"class": "tab-link", "data-table":sIdMainTable})

all_items = soup.find_all("", {"class": "item-list-class"})
## DATA CLEANING
## DATA PUBLISHING

##

# find the main element for each item
all_items = soup.find_all("li", {"class": "item-list-class"})

# empty dictionary to store data, could be a list of anything. i just like dicts
all_data = {}

# initialize key for dict
count = 0

# loop through all_items
for item in all_items:
    # get specific fields
    item_name = item.find("h2", {"class": "item-name-class"})
    item_url = item.find("a", {"class": "item-link-class"})

    # save to dict
    all_data[count] = {
        # get the text
        "item_name": item_name.get_text(),
        # get a specific attribute
        "item_url": item_url.attrs["href"]
    }

    # increment dict key
    count += 1

# do whats needed with data
print(all_data)





## REPORTING 


# CLEAN & CLOSE