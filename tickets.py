#!/usr/bin/python3

import sys, os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

def main():

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
    except AssertionError:
        print('Cannot connect to url.')
        sys.exit(3)

    # Form filling
    _text_input(driver, 'person_id', 'A123456789')
    _select_input(driver, 'getin_date', '2018/08/09-14')
    _select_input(driver, 'from_station', '100')
    _select_input(driver, 'to_station', '051')
    _text_input(driver, 'train_no', '248')
    _elem_click(driver, 'label[for="order_qty_str"]')
    _select_input(driver, 'n_order_qty_str', '3')

    # submit = driver.find_element_by_css_selector('button[type="submit"]')
    # submit.submit()
    _elem_click(driver, 'button[type="submit"]')
    _elem_click(driver, '#randInput')

    # _text_input(driver, 'randInput', rand_input)
    # _select_input(driver, 'n_order_qty_str', '1')
    # for _ in range(5):
    #     try:
    #         getin_date = Select(driver.find_element_by_id('getin_date'))
    #         getin_date.select_by_value('2018/08/09-14')
    #     except:
    #         continue
    #     else:
    #         break
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
    # if test_time == 5:
    #     sys.exit(3)

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
