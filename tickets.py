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
#
#   11 - CONFIG section empty error

import sys, os
import datetime, time
import configparser, threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from tickets_pkg import logging_class as logcl
from tickets_pkg import config_class as confcl


logger = logcl.PersonalLog('tickets')

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
    sections = _target_sections()
    threads = []

    for section in sections[:-1]:
        threads.append(threading.Thread(target=_auto_run, args=[target_time, section]))
        threads[-1].start()
        time.sleep(15)
    else:
        try:
            threads.append(threading.Thread(target=_auto_run, args=[target_time, sections[-1]]))
            threads[-1].start()
        except IndexError:
            logger.info('No section set to be read')
            sys.exit(11)

    # thread_one = threading.Thread(target=_auto_run, args=[target_time, 'INFO03'])
    # thread_one.start()
    #
    # time.sleep(15)
    #
    # thread_two = threading.Thread(target=_auto_run, args=[target_time, 'INFO04'])
    # thread_two.start()


# Get target sections
def _target_sections():
    """
    Return a list on sections that have to be read
    """
    config = confcl.Config('train_tickets.ini')
    sections = config.target_sections()

    return sections


# Automation function
def _auto_run(target_time, section):
    config = confcl.Config('train_tickets.ini')

    driver = webdriver.Firefox()

    # Connect to url
    for _ in range(5):
        try:
            driver.get('http://railway.hinet.net/Foreign/TW/etno1.html')
        except:
            continue
        else:
            break

    # Test for success connection
    try:
        assert 'Train' in driver.title
    except AssertionoError:
        print('Cannot connect to url')
        sys.exit(3)

    # Form filling
    _text_input(driver, 'person_id', config.id(section))
    _select_input(driver, 'getin_date', config.date(section))
    _select_input(driver, 'from_station', config.from_station(section))
    _select_input(driver, 'to_station', config.to_station(section))
    _text_input(driver, 'train_no', config.train_number(section))
    _elem_click(driver, 'label[for="order_qty_str"]')
    # _select_input(driver, 'n_order_qty_str', config.quantity(section))
    _select_input(driver, 'order_qty_str', config.quantity(section))

    _elem_click(driver, 'button[type="submit"]')
    _elem_click(driver, '#randInput')

    while datetime.datetime.now() < target_time:
        time.sleep(0.3)

    _elem_click(driver, '#sbutton')

    _geckolog_clean('geckodriver.log')


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
