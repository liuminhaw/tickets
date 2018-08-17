#!/usr/bin/python3
#
# Program:
#   Buy tickets automation
# Author:
#   haw
#
# Exit Code:
#   1 - Usage error
#   3 - Site connection error
#   5 - Auto form filling error
#   7 - Requesting site error
#
#   11 - CONFIG section empty error
#   15 - Error in puyoma key
#   17 - Error in date key
#   19 - Error in station key
#
#   21 - Config file time interval format error
#   23 - Config file web driver type error
#   25 - CONFIG section empty error

import sys, os
import datetime, time
import configparser, threading, re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from tickets_pkg import logging_class as logcl
from tickets_pkg import config_class as confcl


SITE = 'http://railway.hinet.net/Foreign/TW/etno1.html'
CONFIG_FILE = 'train_tickets.ini'

logger = logcl.PersonalLog('tickets')
config = confcl.Config(CONFIG_FILE)

def main():
    message = \
    """
    USAGE:
        tickets.py YYYY-MM-DD HH:MM:SS
    PARAMETER:
        Submit time
    """
    # Check input parameter
    try:
        target_time = datetime.datetime.strptime(' '.join(sys.argv[1:]), '%Y-%m-%d %H:%M:%S')
    except (IndexError, ValueError):
        print(message)
        sys.exit(1)

    # Get target sections
    threads = []
    sections = _target_sections()
    # if sections == []:
    #     logger.info('No section set to be read, please check the config file.')
    #     sys.exit(11)

    # Configuration information
    interval = int(config.time_interval())

    # Program auto countdown
    _countdown_prep(target_time, sections)

    for section in sections[:-1]:
        threads.append(threading.Thread(target=_auto_run, args=[target_time, section]))
        threads[-1].start()
        time.sleep(interval)
    else:
        try:
            threads.append(threading.Thread(target=_auto_run, args=[target_time, sections[-1]]))
            threads[-1].start()
        except IndexError:
            logger.info('No section set to be read')
            sys.exit(11)

    # Press Enter to quit
    input('Enter to quit.')




# Get target sections
def _target_sections():
    """
    Return a list on sections that have to be read
    """
    # config = confcl.Config('train_tickets.ini')
    sections = config.target_sections()

    return sections


# Countdown before web browser launch
def _countdown_prep(target_time, sections):
    """
    Program countdown before firing web-driver
    Input:
        sections - List of sections in config .ini file
    """
    # if sections == []:
    #     logger.info('No section set to be read, please check the config file.')
    #     sys.exit(11)
    interval = int(config.time_interval())
    delta_time = datetime.timedelta(seconds=len(sections) * interval)
    prepare_time = target_time - delta_time

    while datetime.datetime.now() < prepare_time:
        time.sleep(1)


# Automation function
def _auto_run(target_time, section):
    # config = confcl.Config('train_tickets.ini')

    # Web-driver type
    if config.web_driver().lower() == 'chrome':
        driver = webdriver.Chrome()
    elif config.web_driver().lower() == 'firefox':
        driver = webdriver.Firefox()

    # Connect to url
    for _ in range(5):
        try:
            driver.get(SITE)
        except:
            continue
        else:
            break

    # Focus on browser window
    driver.switch_to_window(driver.current_window_handle)

    # Test for success connection
    try:
        assert 'Train' in driver.title
    except AssertionoError:
        print('Cannot connect to url')
        sys.exit(3)

    # Form filling
    _fill_form(driver, section)

    while datetime.datetime.now() < target_time:
        time.sleep(0.3)

    _elem_click(driver, '#sbutton')

    _geckolog_clean('geckodriver.log')


def _fill_form(driver, section):

    # Convert config data for form filling
    date_value, from_station_value, to_station_value = _data_to_form(section)

    # Find date matching option
    # req = requests.get(SITE)
    # try:
    #     req.raise_for_status()
    # except:
    #     logger.info('Request to get railway page failed.')
    #     sys.exit(7)
    #
    # req.encoding = 'utf-8'
    # soup = BeautifulSoup(req.text, 'html.parser')
    #
    # re_date = re.compile(r'{}.{{3}}'.format(config.date(section)))
    # re_from_station = re.compile(r'\d\d\d-{}'.format(config.from_station(section)))
    # re_to_station = re.compile(r'\d\d\d-{}'.format(config.to_station(section)))
    #
    # try:
    #     date_value = soup.find('option', {'value': re_date})['value']
    # except TypeError:
    #     logger.warning('Cannot find matching date {} of {}'.format(config.date(section), section))
    #     sys.exit(17)

    # Filling form
    _text_input(driver, 'person_id', config.id(section))
    _select_input(driver, 'getin_date', date_value)
    _select_input(driver, 'from_station', from_station_value)
    _select_input(driver, 'to_station', to_station_value)
    _text_input(driver, 'train_no', config.train_number(section))
    _elem_click(driver, 'label[for="order_qty_str"]')

    # Check train type
    if config.is_puyoma(section).lower() == 'yes':
        _select_input(driver, 'n_order_qty_str', config.quantity(section))
    elif config.is_puyoma(section).lower() == 'no':
        _select_input(driver, 'order_qty_str', config.quantity(section))
    else:
        logger.warning('Error exist in section {} of .ini config file.'.format(section))
        sys.exit(15)

    _elem_click(driver, 'button[type="submit"]')
    _elem_click(driver, '#randInput')


def _data_to_form(section):
    """
    Convert config information to data that can be use by ticket form

    Return:
        (date, from_station, to_station)
    """

    # Attempt to request for web page
    for attempt in range(5):
        req = requests.get(SITE)

        try:
            req.raise_for_status()
        except:
            logger.info('Request for railway page failed.')
            time.sleep(0.5)
        else:
            req.encoding = 'utf-8'
            soup = BeautifulSoup(req.text, 'html.parser')
            break

    # Regex define
    re_date = re.compile(r'{}.{{3}}'.format(config.date(section)))
    re_from_station = re.compile(r'\d\d\d-{}'.format(config.from_station(section)))
    re_to_station = re.compile(r'\d\d\d-{}'.format(config.to_station(section)))

    # Pattern matching
    try:
        date_value = soup.find('option', {'value': re_date})['value']
    except TypeError:
        logger.warning('Cannot find matching date {} of {}'.format(config.date(section), section))
        sys.exit(17)

    try:
        from_station_value = soup.find('option', string=re_from_station)['value']
    except TypeError:
        logger.warning('Cannot find matching staion {} of {}'.format(config.from_station(section), section))
        sys.exit(19)

    try:
        to_station_value = soup.find('option', string=re_to_station)['value']
    except TypeError:
        logger.warning('Cannot find matching staion {} of {}'.format(config.to_station(section), section))
        sys.exit(19)

    return (date_value, from_station_value, to_station_value)


# Decorator
def form_attempt(func):
    test_time = 0
    while test_time < 5:
        test_time += 1
        try:
            func()
        except:
            continue
        else:
            break

    return func


@form_attempt
def _text_input(driver, id, text):
    elem = driver.find_element_by_id(id)
    elem.send_keys(text)

@form_attempt
def _select_input(driver, id, value):
    elem = Select(driver.find_element_by_id(id))
    elem.select_by_value(value)

@form_attempt
def _elem_click(driver, selector):
    elem = driver.find_element_by_css_selector(selector)
    elem.click()


def _geckolog_clean(geckolog):
    gecko_log = os.path.abspath(geckolog)
    if os.path.isfile(gecko_log):
        os.remove(gecko_log)


if __name__ == '__main__':
    main()
