# -*- coding:UTF-8 -*-

# Exit status:
#   _VALUE_ - _EXPLANATION_

# Standard library imports
# import standard libraries here
import sys
import os
import time
import argparse
import re
from datetime import datetime, timedelta

# Third party library imports
# import third party libraries here
import requests
from bs4 import BeautifulSoup

# Local application imports
# import self defined applications here
from general_pkg import env
from general_pkg import prep
from general_pkg import search

from module_pkg import conf_mod
from module_pkg import driver

logger = env.LOGGER

# --- CODING BLOCKS ---
# --- ------------- ---

def main():
    """
    USAGE: booking.py -c config-file BOOKING_TYPE
    """

    # arguments definition
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('type', choices=['daan-sport'], help='Booking running type')
    arg_parser.add_argument('-c', '--config', help='Specify configuration file')
    arg_parser.add_argument('--free', help='Show available courts', action='store_true')
    arg_parser.add_argument('--freetime', help='Test free court at specific time', action='store_true')
    arg_parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(env.VERSION))
    args = arg_parser.parse_args()

    # Positional argument: type
    logger.info('Booking type: {}'.format(args.type))
    if args.type == 'daan-sport':
        data_section = 'DAAN_SPORT'

    # Optional argument: config
    if args.config:
        config_file = [args.config]
    else:
        config_file = env.CONFIG_FILE
    logger.info('Config file: {}'.format(config_file))

    try:
        config = conf_mod.Config(config_file)
    except conf_mod.ConfigNotFoundError as err:
        logging = 'Config file config.ini not found: {}'.format(err)
        logger.info(logging)
        sys.exit(11)

    if args.free:
        elected = search.search(config, data_section)
        for available_time, available_court in elected:
            logger.info('Available time: {}, court: {}'.format(available_time ,available_court))
        logger.info('Show free courts executed')
        sys.exit(0)

    if args.freetime:
        elected = search.search_time(config, data_section)
        for available_time, available_court in elected:
            logger.info('Available time: {}, court: {}'.format(available_time ,available_court))
        logger.info('Show free time courts executed')
        sys.exit(0)

    # Read config file settings
    try:
        # driver_count = config.driver_count()
        cookie_duration = config.cookie_duration()
        submit_count = config.submit_count()
        execution_delta = config.execution_delta()
        submit_time = config.submit_time(data_section)
        vision_cred = config.vision_cred()
        submit_time_sleep = config.submit_time_sleep()
        submit_time_offset = config.submit_time_offset()
        driver_time_sleep = config.driver_time_sleep()
    except conf_mod.MissingFileError as err:
        logging = 'file not found in current path: {}'.format(err.message)
        logger.warning(logging)
        sys.exit(15)
    except conf_mod.NoSectionError as err:
        logging = 'config file section error: {}'.format(err.message)
        logger.warning(logging)
        sys.exit(12)
    except conf_mod.NoOptionError as err:
        logging = 'config file option error: {}'.format(err.message)
        logger.warning(logging)
        sys.exit(13)
    except conf_mod.OptionFormatError as err:
        logging = 'config file option format error: {}'.format(err.message)
        logger.warning(logging)
        sys.exit(14)

    # browsers = []
    # for _ in range(driver_count):
    #     browsers.append(driver.Driver())
    browser = driver.Driver()

    try:
        browser.read_conf(config, data_section)
        # for browser in browsers:
        #     browser.read_conf(config, data_section)
    except conf_mod.MissingFileError as err:
        logging = 'file not found in current path: {}'.format(err.message)
        logger.warning(logging)
        sys.exit(15)
    except conf_mod.NoSectionError as err:
        logging = 'config file section error: {}'.format(err.message)
        logger.warning(logging)
        sys.exit(12)
    except conf_mod.NoOptionError as err:
        logging = 'config file option error: {}'.format(err.message)
        logger.warning(logging)
        sys.exit(13)
    except conf_mod.OptionFormatError as err:
        logging = 'config file option format error: {}'.format(err.message)
        logger.warning(logging)
        sys.exit(14)

    execute_time = datetime.strptime(submit_time, '%Y/%m/%d-%H:%M:%S') - timedelta(minutes=execution_delta)

    logger.info('Submit count: {}'.format(submit_count))
    logger.info('Submit time: {}'.format(submit_time))
    logger.info('Execution time: {}'.format(execute_time))
    logger.info('Submit time sleep: {}'.format(submit_time_sleep))
    logger.info('Submit time offset: {}'.format(submit_time_offset))
    logger.info('Driver time sleep: {}'.format(driver_time_sleep))
    logger.info('Booking date: {}'.format(browser.booking_date))
    logger.info('Booking section: {}'.format(browser.booking_section))
    logger.info('Booking time: {}'.format(browser.booking_time))
    logger.info('Booking court: {} {}'.format(browser.booking_court['court'], browser.booking_court['code']))
    # logger.info('Booking date: {}'.format(browsers[0].booking_date))
    # logger.info('Booking section: {}'.format(browsers[0].booking_section))
    # logger.info('Booking time: {}'.format(browsers[0].booking_time))
    # logger.info('Booking court: {}'.format(browsers[0].booking_court))

    # Start drivers on execution_time
    logger.info('Waiting for execution time...')
    while datetime.now() < execute_time:
        time.sleep(10)

    # Browser preparation
    # for browser in browsers:
    #     prep.sport_prep(browser, vision_cred)
    # prep.sport_prep(browser, vision_cred)

    # browser.get_cookie(env.COOKIE_NAME)
    # session = requests.Session()
    # session.headers.update({'Cookie': f'{env.COOKIE_NAME}={browser.cookie}'})
    # booking_link = '{link}&QPid={court}&QTime={time}&PT=1&D={date}'.format(
    #     link=browser.booking_link,
    #     court=browser.booking_court['code'],
    #     time=browser.booking_time,
    #     date=browser.booking_date
    # )

    # Save cookie - Save cookie for repeat usage
    create_cookie = False
    cookie_filepath = f'/tmp/{browser.login_user}.cookie'
    if os.path.exists(cookie_filepath):
        cookie_ctime = datetime.fromtimestamp(os.path.getctime(cookie_filepath))
        now_datetime = datetime.now()
        time_delta = now_datetime - cookie_ctime
        if time_delta > timedelta(minutes=cookie_duration):
            create_cookie = True
    else:
        create_cookie = True

    if create_cookie:
        logger.info(f'Create new cookie file: {cookie_filepath}')
        prep.sport_prep(browser, vision_cred)
        browser.get_cookie(env.COOKIE_NAME)
        with open(cookie_filepath, 'w') as writer:
            writer.write(browser.cookie)
    else:
        logger.info(f'Read cookie file: {cookie_filepath}')
        with open(cookie_filepath, 'r') as reader:
            browser.cookie = reader.readline()

    session = requests.Session()
    session.headers.update({'Cookie': f'{env.COOKIE_NAME}={browser.cookie}'})
    booking_link = '{link}&QPid={court}&QTime={time}&PT=1&D={date}'.format(
        link=browser.booking_link,
        court=browser.booking_court['code'],
        time=browser.booking_time,
        date=browser.booking_date
    )

    logger.info(f'cookie: {browser.cookie}')
    logger.info(f'submit url: {booking_link}')

    # Find target booking button
    # valid_browsers = []
    # for browser in browsers:
    #     try:
    #         browser.find_booking_btn(env.TARGETS_SELECTOR, browser.booking_time, browser.booking_court)
    #         valid_browsers.append(browser)
    #     except driver.FindElementError as err:
    #         logger.info(err)
    #         browser.down()

    # final_browsers = []
    # for browser in valid_browsers:
    #     if browser.booking_button.get_attribute('title') == '':
    #         logger.info('Booking available')
    #         final_browsers.append(browser)
    #     else:
    #         logger.info('Booking not available')

    submit_time = datetime.strptime(submit_time, '%Y/%m/%d-%H:%M:%S')
    while datetime.now() < submit_time:
        time.sleep(submit_time_sleep)

    responses = []
    for _ in range(submit_count):
        response = session.get(booking_link)
        responses.append(response.text)
        time.sleep(driver_time_sleep)

    pattern = re.compile("tp03[^']*")
    for index, text in enumerate(responses):
        soup = BeautifulSoup(text, 'html.parser')
        href = soup.find('script').string
        match = pattern.search(href)
        # print(soup.prettify())
        # print(f'Href: {href}')
        # print(f'Match: {match.group()}')
        result_link = f'{env.DOMAIN_LINK}/{match.group()}'
        response = session.get(result_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        messages = soup.find(id='ContentPlaceHolder1_Step3Info_lab').find_all('span')
        print(f'Driver {index + 1}:')
        for message in messages:
            print(message.text)

    # print('Start', datetime.now())
    # time.sleep(submit_time_offset)
    # for browser in final_browsers:
    #     browser.booking_button.click()
    #     print('Clicked', datetime.now())
    #     browser.accept_alert()
    #     time.sleep(driver_time_sleep)

    # for browser in final_browsers:
    #     result = browser.driver.find_element_by_id(env.ID_RESULT_MESSAGE)
    #     logging = 'Result: {}'.format(result.text)
    #     logger.info(logging)
    #     print('')

    print('Done.')


    # Press Enter to quit
    input('Press Enter to quit.\n')


if __name__ == '__main__':
    # Rund codes
    main()
