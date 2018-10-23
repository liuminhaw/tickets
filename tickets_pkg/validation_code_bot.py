"""
Program:
    Fill in validation code automatically using machine learning
Author:
    haw

Note:
    For Taiwan railway system
"""

import numpy as np
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from keras.models import load_model, Model


LETTERSTR = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
SCREEN_IMG = './model/screen.png'
CAPTURE_IMG = './model/capture.jpg'

model_5 = load_model('./model/imitate_5_model.h5')
model_6 = load_model('./model/imitate_6_model.h5')
model_56 = load_model('./model/imitate_56_model.h5')


model_56.predict(np.stack([np.array(Image.open(CAPTURE_IMG))/255.0]))[0][0]
model_5.predict(np.stack([np.array(Image.open(CAPTURE_IMG))/255.0]))
model_6.predict(np.stack([np.array(Image.open(CAPTURE_IMG))/255.0]))


def fill_validation_code(driver):
    """
    Validation code auto filling
    """
    # Initialize
    model = None


    driver.save_screenshot(SCREEN_IMG)
    location = driver.find_element_by_id('idRandomPic').location
    location_x, location_y = location['x'] + 5, location['y'] + 5
    img = Image.open(SCREEN_IMG)
    capture = img.crop((location_x, location_y, location_x+200, location_y+60))
    capture.convert('RGB').save(CAPTURE_IMG, 'JPEG')

    p_56 = model_56.predict(np.stack([np.array(Image.open(CAPTURE_IMG))/255.0]))[0][0]
    if p_56 > 0.5:
        model = model_6
    else:
        model = model_5
    prediction = model.predict(np.stack([np.array(Image.open(CAPTURE_IMG))/255.0]))
    answer = ''
    for predict in prediction:
        answer += LETTERSTR[np.argmax(predict[0])]
    capture_textbox = driver.find_element_by_id('randInput')
    capture_textbox.send_keys(answer)

    # Remove image files
    # os.remove(SCREEN_IMG)
    # os.remove(CAPTURE_IMG)
