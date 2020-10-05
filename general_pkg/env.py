# -*- conding: UTF-8 -*-

# Standard library imports
import os

# Local application imports
from module_pkg import logging_class as logcl

# Global variable definitions
VERSION = 'v3.1.1'

CONFIG_FILE = ['config.ini']
LOGGER = logcl.PersonalLog('booking', os.path.join(os.getcwd(), 'log'))

# Web DOM variables definition
ID_LOGIN = 'ContentPlaceHolder1_loginid'
ID_PASSWD = 'loginpw'
ID_CAPTCHA = 'ContentPlaceHolder1_Captcha_text'
ID_CAPTCHA_IMAGE = 'ContentPlaceHolder1_CaptchaImage'
ID_LOGIN_BTN = 'login_but'
ID_RESULT_MESSAGE = 'ContentPlaceHolder1_Step3Info_lab'

TARGETS_SELECTOR = 'td.tWord'
AVAILABLE_BTN_SRC = 'https://scr.cyc.org.tw/img/sche01.png'
OCCUPIED_BTN_SRC = 'https://scr.cyc.org.tw/img/sche02.png'
