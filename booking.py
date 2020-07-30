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
from general_pkg import prep

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

    browsers = [driver.Driver(), driver.Driver()]
    try:
        for browser in browsers:
            browser.read_conf(config, data_section)
        submit_time = config.submit_time(data_section)
        vision_cred = config.vision_cred()
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
    logger.info('Booking date: {}'.format(browsers[0].booking_date))
    logger.info('Booking section: {}'.format(browsers[0].booking_section))
    logger.info('Booking time: {}'.format(browsers[0].booking_time))
    logger.info('Booking court: {}'.format(browsers[0].booking_court))

    # Run driver 3 minutes before submit time
    logger.info('Waiting for execution time...')
    execute_time = datetime.strptime(submit_time, '%Y/%m/%d-%H:%M:%S') - timedelta(minutes=3)
    while datetime.now() < execute_time:
        time.sleep(10)

    # Browser preparation
    for browser in browsers:
        prep.sport_prep(browser, vision_cred)


    # Find target booking button
    valid_browsers = []
    for browser in browsers:
        try:
            browser.find_target(env.TARGETS_SELECTOR, browser.booking_time, browser.booking_court)
            valid_browsers.append(browser)
        except driver.FindElementError as err:
            logger.info(err)
            browser.down()

    final_browsers = []
    for browser in valid_browsers:
        if browser.booking_button.get_attribute('title') == '':
            logger.info('Booking available')
            final_browsers.append(browser)
        else:
            logger.info('Booking not available')

    submit_time = datetime.strptime(submit_time, '%Y/%m/%d-%H:%M:%S')
    while datetime.now() < submit_time:
        time.sleep(0.3)

    print('Start', datetime.now())
    time.sleep(0.4)
    for browser in final_browsers:
        browser.booking_button.click()
        print('Clicked', datetime.now())
        browser.accept_alert()
        time.sleep(0.3)
    
        

    # Press Enter to quit
    input('Press Enter to quit.\n')


if __name__ == '__main__':
    # Rund codes
    main()