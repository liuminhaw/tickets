"""
Program:
    Check if an Taiwan id is valid
Author:
    haw
"""

import sys, re
from tickets_pkg import logging_class as lgcl
# import logging_class as lgcl

LETTERS = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14,
           'F': 15, 'G': 16, 'H': 17, 'I': 34, 'J': 18,
           'K': 19, 'L': 20, 'M': 21, 'N': 22, 'O': 35,
           'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27,
           'U': 28, 'V': 29, 'W': 32, 'X': 30, 'Y': 31,
           'Z': 33}

logger = lgcl.PersonalLog('id_identifier')


def webdriver_check(web_driver):
    """
    Web driver validation

    Return value:
        True - Supported web driver
        False - Not supported web driver
    """
    return web_driver.lower() == 'chrome' or web_driver.lower() == 'firefox'


def time_interval_check(interval):
    """
    Time interval validation

    Return value:
        True - Valid time interval
        False - Invalid time interval
    """
    # Valid type
    try:
        interval = int(interval)
    except ValueError:
        return False

    # Valid range
    return interval >= 1 and interval <= 60


def section_exist_check(sections):
    """
    Section existence validation

    Return value:
        True - Section exist
        False - No section exist
    """
    return sections != []


def id_check(personal_id):
    """
    ID validation

    Return value:
        True - Valid id
        False - Invalid id
    """
    checksum = 0

    # Check personal id syntax
    re_pattern = re.compile(r'^[a-zA-Z][0-9]{9}')
    re_match = re_pattern.fullmatch(personal_id)

    if re_match == None:
        return False

    # Alphabet number transform
    alpha_num = LETTERS[personal_id[0].upper()]
    checksum = (alpha_num // 10) + (alpha_num % 10) * 9

    multiplier = 8
    for num in personal_id[1:]:
        checksum += multiplier * int(num)
        multiplier -= 1
    checksum += int(personal_id[-1])

    # Result
    return checksum % 10 == 0


def date_check(date):
    """
    Date format YYYY/MM/DD validation

    Return value:
        True - Correct format
        False - Incorrect format
    """

    # Check date syntax
    re_pattern = re.compile(r'^\d\d\d\d/\d\d/\d\d$')
    re_match = re_pattern.fullmatch(date)

    return re_match != None


def train_number_check(train_number):
    """
    Train number validation

    Return value:
        True - Valid train number
        False - Invalid train number
    """
    # Valid type
    try:
        number = int(train_number)
    except ValueError:
        return False

    # Valid range
    return number > 0 and number < 10000


def quantity_check(quantity):
    """
    Tickets quantity validation

    Return value:
        True - Valid ticket quantity
        False - Invalid ticket quantity
    """
    # Valid type
    try:
        quantity = int(quantity)
    except ValueError:
        return False

    # Valid range
    return quantity >= 1 and quantity <= 6


# def puyoma_check(puyoma):
#     """
#     Yes / No validation
#
#     Return value:
#         True - Valid option
#         False - Invalid option
#     """
#     return puyoma.lower() == 'yes' or puyoma.lower() == 'no'



if __name__ == '__main__':
    # Test id_check()
    if id_check('A123456689'):
        print('Valid ID')
    else:
        print('Invalid ID')

    # Test date_check()
    if date_check('2018/8/23'):
        print('Valid date')
    else:
        print('Invalid date')

    # Test train_number_check()
    if train_number_check('441'):
        print('Valid train number')
    else:
        print('Invalid train number')
