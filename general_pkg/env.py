# -*- conding: UTF-8 -*-

# Standard library imports
import os
import datetime

# Global variable definitions
VERSION = 'v3.1.0a'

CONFIG_FILE = ['config.ini']
LOG_DIR = os.path.join(os.getcwd(), 'log')

# Web DOM variables definition
ID_LOGIN = 'ContentPlaceHolder1_loginid'
ID_PASSWD = 'loginpw'
ID_CAPTCHA = 'ContentPlaceHolder1_Captcha_text'
ID_CAPTCHA_IMAGE = 'ContentPlaceHolder1_CaptchaImage'
ID_LOGIN_BTN = 'login_but'
ID_RESULT_MESSAGE = 'ContentPlaceHolder1_Step3Info_lab'
TARGETS_SELECTOR = 'td.tWord'
