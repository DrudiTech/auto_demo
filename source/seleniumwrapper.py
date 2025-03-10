from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

DEFAULT_WAITING_SEC = 2
DEFAULT_N_TRIES = 3

ENABLE_LOG= False

def print_with_switch(text):
    if ENABLE_LOG:
        print(text)



class CustomElementNotFound(Exception):
    """"Raised when element is not found

    Attributes:
        sElementReference -- input salary which caused the error
        message -- explanation of the error
    """

    def __init__(self, sElementReference, message="Element not found ion the given range"):
        self.sElementReference = sElementReference
        self.message = message
        super().__init__(self.message)




def waitElementByXPath(driver,sXPath,waitingSecs=DEFAULT_WAITING_SEC,nMaxTry=DEFAULT_N_TRIES):
    i = 0
    while i<=nMaxTry:
        driver.implicitly_wait(waitingSecs)
        print_with_switch('Search '+sXPath+' tentative nr :' + str(i+1))
        try:
             result = driver.find_element(By.XPATH,sXPath)
             print_with_switch('End of search '+sXPath+' : SUCCESSFUL')
             return result
        except:
            continue
    print_with_switch('End of search '+sXPath+' : UNSUCCESSFUL')
    raise CustomElementNotFound(sXPath)

def waitChildrenElementByXPath(weParent,sXPath,waitingSecs=DEFAULT_WAITING_SEC,nMaxTry=DEFAULT_N_TRIES):
    i = 0
    driver = weParent.parent
    while i<=nMaxTry:
        driver.implicitly_wait(waitingSecs)
        print_with_switch('Search '+sXPath+' tentative nr :' + str(i+1))
        try:
             result = weParent.find_elements(By.XPATH,sXPath)
             print_with_switch('End of search '+sXPath+' : SUCCESSFUL')
             return result
        except:
            continue
    print_with_switch('End of search '+sXPath+' : UNSUCCESSFUL')
    raise CustomElementNotFound(sXPath)


    