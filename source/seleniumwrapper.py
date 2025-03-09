from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



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




def waitElementByXPath(driver,sXPath,waitingSecs,nMaxTry):
    i = 0
    while i<=nMaxTry:
        driver.implicitly_wait(waitingSecs)
        try:
             result = driver.find_element(By.XPATH,sXPath)
             print('End of search '+sXPath+' : SUCCESSFUL')
             return result
        except:
            print('Search '+sXPath+' tentative nr :' + i+1)
    print('End of search '+sXPath+' : UNSUCCESSFUL')
    raise CustomElementNotFound(sXPath)


    