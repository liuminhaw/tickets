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
    """
    Web driver for automation usage when running ticket program
    """

    def __init__(self):
        self.driver = None
        self.booking_button = None

        self.login_link = None
        self.booking_link = None
        self.login_user = None
        self.login_password = None
        self.headless = None
        self.booking_date = None
        self.booking_section = None
        self.booking_time = None
        self.booking_court = None

    def driver_up(self, headless):
        """
        Create selenium driver
        Param:
            headless - headless mode [boolean]
        """
        if headless:
            options = Options()
            options.headless = headless
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            self.driver = webdriver.Chrome()

    def down(self):
        """
        Close selenium driver (self.driver)
        """
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

    def find_booking_btn(self, selector, time, court):
        """
        Find booking button according to given date and court
        Exception:
            FindElementError
        """
        candidates = self.driver.find_elements_by_css_selector(selector)

        for i, _ in enumerate(candidates):
            if candidates[i].text == time and candidates[i+1].text == court:
                self.booking_button = candidates[i+3].find_element_by_tag_name('img')
                break
                # return candidates[i+3].find_element_by_tag_name('img')
        else:
            FindElementError(DriverError)

    def read_conf(self, config, section, action='book'):
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
        self.headless = config.headless()
        self.booking_date = config.date(section)
        self.booking_section = config.section(section)

        if action == 'book':
            self.booking_time = config.time(section)
            self.booking_court = config.court(section)


# Exceptions
class DriverError(Exception):
    """
    Base class of driver exception
    """

class FindElementError(DriverError):
    """
    Raised if failed to locate element
    """
