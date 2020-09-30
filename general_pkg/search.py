# -*- coding:UTF-8 -*-

# Standard library imports
import re

# Third party library imports

# Local application imports
from general_pkg import env
from general_pkg import prep

from module_pkg import logging_class as logcl
from module_pkg import conf_mod
from module_pkg import driver

logger = env.LOGGER

def search(config, section):
    """
    Report for available courts
    """

    # Read required config
    vision_cred = _config_test(config.vision_cred)

    browser = driver.Driver()
    _config_test(browser.read_conf, config, section, "action='search'")

    logger.info('Search date: {}'.format(browser.booking_date))
    logger.info('Search section: {}'.format(browser.booking_section))

    prep.sport_prep(browser, vision_cred)

    candidates = browser.driver.find_elements_by_css_selector(env.TARGETS_SELECTOR)
    elected = []
    for i in range(len(candidates)):
        try:
            element = candidates[i].find_element_by_tag_name('img')
            if element.get_attribute('src') == env.AVAILABLE_BTN_SRC:
                available_time = candidates[i-3].text
                available_court = candidates[i-2].text
                if re.compile(r'[0-2]\d:00~[0-2]\d:00').fullmatch(available_time) != None:
                    elected.append((available_time, available_court))
        except:
            pass
    
    return elected


def _config_test(func, *args):
    try:
        ret_val = func(*args)
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

    return ret_val
