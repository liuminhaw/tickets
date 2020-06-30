
# -*- coding: UTF-8 -*-
"""
Program:
    Driver class for selenium driver
Author:
    haw
"""

# Third party library imports
from selenium import webdriver

class Driver():
    
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get(self, url):
        """
        Open url page on driver
        """
        self.driver.get(url)

    def click(self, element_id):
        """
        Click on selected button
        """
        element = self.driver.find_element_by_id(element_id)
        element.click()

    def accept_alert(self):
        """
        Accept driver alert message
        """
        alert = self.driver.switch_to.alert
        alert.accept()

    def insert_text(self, element_id, text):
        """
        Insert text into selected field
        """
        element = self.driver.find_element_by_id(element_id)
        element.send_keys(text)

    def find_target(self, selector, time, court):
        """
        Find target according to given date and court
        Exception:
            FindElementError
        """
        candidates = self.driver.find_elements_by_css_selector(selector)
        
        for i in range(len(candidates)):
            if candidates[i].text == time and candidates[i+1].text == court:
                return candidates[i+3].find_element_by_tag_name('img')
        raise FindElementError(driverError)


# Exceptions
class driverError(Exception):
    """
    Base class of driver exception
    """
    pass

class FindElementError(driverError):
    """
    Raised if failed to locate element
    """
    pass