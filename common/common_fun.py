#!/usr/bin/env python
# coding:utf-8

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from appium.webdriver import WebElement
from common.desired_caps import appium_desired
import logging.config
from baseView.basicView import BaseView
import datetime
from datetime import datetime
import time
import os
import re


class Common(BaseView):

    def __init__(self, driver):
        super().__init__(driver)
        self.allow = None

    def get_screenSize(self):
        """获取屏幕尺寸"""
        x = self.get_window_size()['width']
        y = self.get_window_size()['height']
        return x, y

    # 相對坐標適用于頁面等比例縮放
    def autoCoord(self, x, y):
        width, height = self.get_screenSize()
        a = int((x * width) / 1080)
        b = int((y * height) / 1920)
        return a, b

    def swipeLeft(self):
        """向左滑動"""
        logging.info('swipeLeft')
        l = self.get_screenSize()
        y1 = int(l[1] * 0.5)
        x1 = int(l[0] * 0.95)
        x2 = int(l[0] * 0.25)
        self.swipe(x1, y1, x2, y1, 1000)

    def swipeUp(self):
        """向上滑動"""
        logging.info('swipeUp')
        l = self.get_screenSize()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.9)
        x2 = int(l[0] * 0.5)
        y2 = int(l[1] * 0.2)
        self.driver.swipe(x1, y1, x2, y2, 1000)

    def swipeDown(self):
        """日歷控件年份向下滑動"""
        logging.info('swipeDown')
        l = self.get_screenSize()
        # 738（寬）/898（高）是年份元素坐標
        x1 = int(l[0] * 738 / 1080)
        y1 = int(l[1] * 898 / 1920)
        x2 = int(l[0] * 738 / 1080)
        y2 = int(l[1] * 1600 / 1920)
        self.driver.swipe(x1, y1, x2, y2, 1000)

    def screen_pinch(self):
        """缩小地圖"""
        x, y = self.get_screenSize()
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(int(x * 0.2), int(y * 0.2))
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(int(x * 0.4), int(x * 0.4))
        actions.w3c_actions.pointer_action.release()
        logging.info('start pinch ......')
        actions.perform()

    def screen_zoom(self):
        """放大地圖"""
        x, y = self.get_screenSize()
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(int(x * 0.4), int(y * 0.4))
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(int(x * 0.8), int(y * 0.8))
        actions.w3c_actions.pointer_action.release()
        logging.info('start zoom ......')
        actions.perform()

    @staticmethod
    def getTime():
        """獲取當前時間"""
        now = time.strftime("%Y-%m-%d %H-%M-%S")
        return now

    def current_time(self):
        """獲取當前時間"""
        tz = '(UTC +8)'
        dt = datetime.datetime.now().strftime('%d-%b-%Y %H:%M')
        now_time = ('%s %s' % (dt, tz))
        print(now_time)
        return now_time

    def getScreenShot(self, module):
        """截圖"""
        time = self.getTime()
        image_file = os.path.dirname(os.path.dirname(__file__)) + '/screenshots/%s_%s.png' % (module, time)
        logging.info('get %s screenshot' % module)
        self.driver.get_screenshot_as_file(image_file)

    def startApp(self):

        """啟動 APP"""
        logging.info('============startApp===============')
        self.driver.find_element(By.ID, 'com.android.permissioncontroller:id/permission_allow_button').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//android.widget.TextView[@text="Skip"]').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup').click()
        time.sleep(1)
        
        #通過坐標點擊廣告“關閉”按鈕
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(954, 272)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        # 使用 press_keycode + AndroidKey.BACK（键码 4）
        driver.press_keycode(4)  # 4 是返回键的标准键码
        logging.info('進入首頁')

        # 点击键盘返回健收起键盘
        # self.driver.keyevent(4)

    def stopApp(self):
        """停止 APP"""
        logging.info('============stopApp===============')
        self.driver.quit()


if __name__ == '__main__':
    driver = appium_desired()
    driver.implicitly_wait(15)
    A = Common(driver)
    time.sleep(1)
    A.startApp()
