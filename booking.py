# -*- coding:UTF-8 -*-

# Exit status:
#   _VALUE_ - _EXPLANATION_

# Standard library imports
# import standard libraries here
import sys, time
import argparse
from datetime import datetime, timedelta

# Third party library imports
# import third party libraries here
from selenium import webdriver

# Local application imports
# import self defined applications here
from general_pkg import env
from general_pkg import uncaptcha

from module_pkg import logging_class as logcl
from module_pkg import conf_mod
from module_pkg import driver

logger = logcl.PersonalLog('booking', env.LOG_DIR)

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


    # Read config file settings
    try:
        config = conf_mod.Config(config_file) 
    except conf_mod.ConfigNotFoundError as err:
        logging = 'Config file config.ini not found: {}'.format(err)
        logger.info(logging)
        sys.exit(11)

    try:
        login_link = config.login_link()
        booking_link = config.booking_link()
        vision_cred = config.vision_cred()
        login_user = config.login_user()
        login_password = config.login_password()
        submit_time = config.submit_time(data_section)
        booking_date = config.date(data_section)
        booking_section = config.section(data_section)
        booking_time = config.time(data_section)
        booking_court = config.court(data_section)
    except conf_mod.NoSectionError as err:
        logging = 'config file section error: {}'.format(err)
        logger.warning(logging)
        sys.exit(12)
    except conf_mod.NoOptionError as err:
        logging = 'config file option error: {}'.format(err)
        logger.warning(logging)
        sys.exit(13)
    except conf_mod.OptionFormatError as err:
        logging = 'config file option format error: {}'.format(err)
        logger.warning(logging)
        sys.exit(14)

    logger.info('Submit time: {}'.format(submit_time))
    logger.info('Booking date: {}'.format(booking_date))
    logger.info('Booking section: {}'.format(booking_section))
    logger.info('Booking time: {}'.format(booking_time))
    logger.info('Booking court: {}'.format(booking_court))

    # Run driver 3 minutes before submit time
    logger.info('Waiting for execution time...')
    execute_time = datetime.strptime(submit_time, '%Y/%m/%d-%H:%M:%S') - timedelta(minutes=3)
    while datetime.now() < execute_time:
        time.sleep(10)

    # Run selenium driver
    # User login
    browser = driver.Driver()
    browser.get(login_link)

    browser.accept_alert()
    browser.accept_alert()

    browser.insert_text(env.ID_LOGIN, login_user)
    browser.insert_text(env.ID_PASSWD, login_password)

    # Uncaptcha
    try:
        captcha_ans = uncaptcha.uncaptcha_sport(browser.driver, vision_cred)
        browser.insert_text(env.ID_CAPTCHA, captcha_ans)
    except uncaptcha.NoMatchTextError as err:
        logger.info(err)
        sys.exit(21)

    browser.click(env.ID_LOGIN_BTN)

    # Directing to booking page
    booking_link = '{link}&D={date}&D2={section}'.format(link=booking_link, date=booking_date, section=booking_section)
    browser.get(booking_link)

    # Find target booking button
    try:
        booking_button = browser.find_target(env.TARGETS_SELECTOR, booking_time, booking_court)
    except driver.FindElementError as err:
        logger.info(err)
        sys.exit(31)

    if booking_button.get_attribute('title') == '':
        logger.info('Booking available')
        submit_time = datetime.strptime(submit_time, '%Y/%m/%d-%H:%M:%S')
        # Loop check submit once after submit time
        while datetime.now() < submit_time:
            time.sleep(0.3)
        # Offset time before submit
        time.sleep(0.5)
        booking_button.click()
        browser.accept_alert()
    else:
        logger.info('Booking not available')
    

    # Press Enter to quit
    input('Press Enter to quit.\n')


if __name__ == '__main__':
    # Rund codes
    main()