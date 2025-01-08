from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .find_elements import *
from .invoke_api import *
from .get_driver import *

import os

download_dir = "C:\\TMPIMGGI\\LAST_IMG\\"
download_kit = "C:\\TMPIMGKIT\\"
download_ggi = "C:\\TMPIMGGI\\"
driver = None
By = By


def create_dirs():
    global download_dir, download_kit, download_ggi
    for directory in [download_dir, download_kit, download_ggi]:

        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f" - Diretório criado: {directory}")

def initialize_driver():
    global driver
    if driver is None:
        driver = get_driver.backcode__dont_use__launch_browser(download_dir)
        return driver

def get(link):
    global driver
    if driver != None:
        get_driver.backcode__dont_use__get(driver, link)

def find_element_with_wait(by, value, timeout=10, parent=None):
    global driver
    if driver != None:
        return find_elements.find_element_with_wait_backcode(driver, by.lower(), value, timeout, parent)

    else: raise ValueError("Error: Driver is None")

def find_elements_with_wait(by, value, timeout=10, parent=None):
    global driver
    if driver != None:
        return find_elements.find_elements_with_wait_backcode(driver, by.lower(), value, timeout, parent)

    else: raise ValueError("Error: Driver is None")