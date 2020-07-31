
# -*- coding: UTF-8 -*-
"""
Program:
    Driver class for selenium driver
Author:
    haw
"""

# Third party library imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Driver():
    
    def __init__(self):
        pass

    def up(self):
        options = Options()
        options.headless = True
        #self.driver = webdriver.Chrome(chrome_options=options)
        self.driver = webdriver.Chrome()

    def down(self):
        self.driver.close()

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
                self.booking_button = candidates[i+3].find_element_by_tag_name('img')
                break
                # return candidates[i+3].find_element_by_tag_name('img')
        else: 
            FindElementError(driverError)

    def read_conf(self, config, section):
        """
        Read in config settings
        Exception:
            conf_mod.NoSectionError
            conf_mod.NoOptionError
            conf_mod.OptionFormatError
        """
        self.login_link = config.login_link()
        self.booking_link = config.booking_link()
        self.login_user = config.login_user()
        self.login_password = config.login_password()
        self.booking_date = config.date(section)
        self.booking_section = config.section(section)
        self.booking_time = config.time(section)
        self.booking_court = config.court(section)


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