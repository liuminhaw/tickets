# -*- coding:UTF-8 -*-

# Exit status:
#   _VALUE_ - _EXPLANATION_

# Standard library imports
# import standard libraries here
import sys
import argparse

# Third party library imports
# import third party libraries here
from selenium import webdriver

# Local application imports
# import self defined applications here
from general_pkg import env

from module_pkg import logging_class as logcl
from module_pkg import conf_mod

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
        login_user = config.login_user()
        login_password = config.login_password()
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

    logger.info(booking_date)
    logger.info(booking_section)
    logger.info(booking_time)
    logger.info(booking_court)

    # Run selenium driver
    driver = webdriver.Chrome()
    driver.get(login_link)

    alert_obj = driver.switch_to.alert
    alert_obj.accept()
    alert_obj = driver.switch_to.alert
    alert_obj.accept()

    elem = driver.find_element_by_id(env.ID_LOGIN)
    elem.send_keys(login_user)
    elem = driver.find_element_by_id(env.ID_PASSWD)
    elem.send_keys(login_password)
    elem = driver.find_element_by_id(env.ID_CAPTCHA)
    elem.click()

    # Manual insert captcha value
    input('Press Enter to continue.')

    elem = driver.find_element_by_id(env.ID_LOGIN_BTN)
    elem.click()

    # Press Enter to quit
    input('Press Enter to quit.\n')


if __name__ == '__main__':
    # Rund codes
    main()