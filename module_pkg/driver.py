
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

        