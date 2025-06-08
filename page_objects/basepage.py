# -*- coding: UTF-8 -*-
import yaml
import logging.config
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os



class BasePage():
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def find_elements(self, *loc):
        return self.driver.find_elements(*loc)

    def get_window_size(self):
        return self.driver.get_window_size()

    def swipe(self, start_x, start_y, end_x, end_y, duration):
        return self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def find_element_wait(self, locator, timeout=10):
        """顯式等待元素出現並返回元素"""
        wait = WebDriverWait(self.driver, timeout, 0.5)
        return wait.until(EC.presence_of_element_located(locator))

