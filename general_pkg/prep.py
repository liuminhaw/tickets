# -*- coding:UTF-8 -*-
"""
Browser action for booking program
Author:
    haw
"""

# Standard library imports
# import standard libraries here

# Third party library imports
# import third party libraries here

# Local application imports
# import self defined applications here
from general_pkg import env
from general_pkg import uncaptcha

def sport_prep(browser, credential):
    """
    Sport center booking preparation before submit
    Exception:
        uncaptcha.NoMatchTextError
    """
    browser.driver_up(browser.headless)
    browser.get(browser.login_link)
    browser.accept_alert()
    browser.accept_alert()
    browser.insert_text(env.ID_LOGIN, browser.login_user)
    browser.insert_text(env.ID_PASSWD, browser.login_password)

    # Uncaptcha
    try:
        captcha_ans = uncaptcha.uncaptcha_sport(browser.driver, credential)
        browser.insert_text(env.ID_CAPTCHA, captcha_ans)
    except uncaptcha.NoMatchTextError as err:
        raise PreparationError(err) from err

    browser.click(env.ID_LOGIN_BTN)

    # Directing to booking page
    print("Logging: Direct to booking page")
    booking_link = '{link}&D={date}&D2={section}'.format(
        link=browser.booking_link,
        date=browser.booking_date,
        section=browser.booking_section)
    browser.get(booking_link)



# Exceptions
class PreparationError(Exception):
    """
    Raised when preparation step failed
    """
