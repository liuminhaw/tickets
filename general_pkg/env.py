# -*- conding: UTF-8 -*-

# Standard library imports
import os
import datetime

# Global variable definitions
VERSION = 'v3.0.0'

CONFIG_FILE = ['config.ini']
LOG_DIR = os.path.join(os.getcwd(), 'log')

# Web DOM variables definition
ID_LOGIN = 'ContentPlaceHolder1_loginid'
ID_PASSWD = 'loginpw'
ID_CAPTCHA = 'ContentPlaceHolder1_Captcha_text'
ID_CAPTCHA_IMAGE = 'ContentPlaceHolder1_CaptchaImage'
ID_LOGIN_BTN = 'login_but'
TARGETS_SELECTOR = 'td.tWord'
