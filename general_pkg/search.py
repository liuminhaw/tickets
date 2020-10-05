# -*- coding:UTF-8 -*-
"""
Search for available courts with option --free and --freetime
"""

# Standard library imports
import sys
import re

# Third party library imports
import selenium

# Local application imports
from general_pkg import env
from general_pkg import prep

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
    for i, candidate in enumerate(candidates):
        try:
            element = candidate.find_element_by_tag_name('img')
            if element.get_attribute('src') == env.AVAILABLE_BTN_SRC:
                available_time = candidates[i-3].text
                available_court = candidates[i-2].text
                if re.compile(r'[0-2]\d:00~[0-2]\d:00').fullmatch(available_time) is not None:
                    elected.append((available_time, available_court))
        except selenium.common.exceptions.NoSuchElementException:
            pass

    return elected


def search_time(config, section):
    """
    Search for available courts at specific time
    """
    candidates = search(config, section)
    booking_time = _config_test(config.time, section)

    elected = []
    for available_time, available_court in candidates:
        if booking_time == available_time:
            elected.append((available_time, available_court))

    return elected


def _config_test(func, *args):
    try:
        ret_val = func(*args)
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

    return ret_val
