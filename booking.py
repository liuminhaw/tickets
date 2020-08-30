# -*- coding:UTF-8 -*-

# Exit status:
#   _VALUE_ - _EXPLANATION_

# Standard library imports
# import standard libraries here
import sys, os, time 
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

    try:
        browsers = [driver.Driver()] * config.driver_count()
        execution_delta = config.execution_delta()
        submit_time = config.submit_time(data_section)
        vision_cred = config.vision_cred()
        submit_time_sleep = config.submit_time_sleep()
        submit_time_offset = config.submit_time_offset()
        driver_time_sleep = config.driver_time_sleep()
    except conf_mod.FileNotFoundError as err:
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

    try:
        for browser in browsers:
            browser.read_conf(config, data_section)
    except conf_mod.FileNotFoundError as err:
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

    logger.info('Submit time: {}'.format(submit_time))
    logger.info('Execution time: {}'.format(execute_time))
    logger.info('Submit time sleep: {}'.format(submit_time_sleep))
    logger.info('Submit time offset: {}'.format(submit_time_offset))
    logger.info('Driver time sleep: {}'.format(driver_time_sleep))
    logger.info('Booking date: {}'.format(browsers[0].booking_date))
    logger.info('Booking section: {}'.format(browsers[0].booking_section))
    logger.info('Booking time: {}'.format(browsers[0].booking_time))
    logger.info('Booking court: {}'.format(browsers[0].booking_court))

    # Start drivers on execution_time
    logger.info('Waiting for execution time...')
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
        time.sleep(submit_time_sleep)

    print('Start', datetime.now())
    time.sleep(submit_time_offset)
    for browser in final_browsers:
        browser.booking_button.click()
        print('Clicked', datetime.now())
        browser.accept_alert()
        time.sleep(driver_time_sleep)

    for browser in final_browsers:
        result = browser.driver.find_element_by_id(env.ID_RESULT_MESSAGE)
        logging = 'Result: {}'.format(result.text)
        logger.log(logging)
        print('')


    # Press Enter to quit
    input('Press Enter to quit.\n')


if __name__ == '__main__':
    # Rund codes
    main()