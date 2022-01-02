# -*- coding: UTF-8 -*-
"""
captcha resolve used in booking program
Author:
    haw
"""

# Standard library imports
import os
import io
import re

# Thire party library imports
from PIL import Image

from google.cloud import vision
from google.oauth2 import service_account

# Local application imports
from . import env
# from ..module_pkg import conf_mod


def uncaptcha_sport(driver, key):
    """
    Solving captcha from sport-center booking site
    Input:
        driver - selenium driver
        cred - credential file location for using vision api
    Error:
        NoMatchTextError
    """

    # Get captcha image
    screenshot = 'tmp/screenshot.png'
    crop_img = 'tmp/crop.jpeg'
    crop_width = 68
    crop_height = 25

    os.makedirs('tmp', exist_ok=True)

    driver.save_screenshot(screenshot)
    location = driver.find_element_by_id(env.ID_CAPTCHA_IMAGE).location
    location_x, location_y = location['x'], location['y']

    img = Image.open(screenshot)
    capture = img.crop((location_x, location_y, location_x+crop_width, location_y+crop_height))
    capture.convert('RGB').save(crop_img, 'JPEG')

    # Resolve captcha image with vision api
    ans = _detect_text(crop_img, key)

    return ans


def _detect_text(img_path, key):
    """
    Detects text in the file
    Error:
        NoMatchTextError
    """

    # Vision api resolve image
    creds = service_account.Credentials.from_service_account_file(key)
    client = vision.ImageAnnotatorClient(credentials=creds)

    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        match_string = re.search(r'\d{5}', text.description)
        if match_string is not None:
            return match_string.group(0)
        raise NoMatchTextError('No match in detected text')



# Exceptions
class NoMatchTextError(Exception):
    """
    Raised if no match found in captcha
    """
