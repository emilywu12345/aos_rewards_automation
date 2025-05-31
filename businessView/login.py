#!/usr/bin/env python
# coding:utf-8

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from common.desired_caps import appium_desired
from common.common_fun import Common
from data import paramet
import logging
import time


class LoginView(Common):
    def email_login(self):
        """email登入操作"""
        logging.info('==========email_login===========')
        try:
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//android.widget.TextView[@text="My Account"]').click()
            self.driver.find_element(By.XPATH, '//android.widget.TextView[@text="Join Now"]').click()
            self.driver.find_element(By.XPATH, '//android.widget.TextView[@text="Login / Join S⁺ REWARDS"]').click()

            self.swipeUp(20)

            self.driver.find_element(By.XPATH, '(//android.widget.TextView[@resource-id="RNE__Checkbox__Icon"])[1]').click()
            self.driver.find_element(By.XPATH, '(//android.widget.TextView[@resource-id="RNE__Checkbox__Icon"])[2]').click()
            self.driver.find_element(By.XPATH, '(//android.widget.TextView[@resource-id="RNE__Checkbox__Icon"])[3]').click()

            self.driver.find_element(By.XPATH, '//android.view.ViewGroup[@content-desc="Accept"]').click()
            self.driver.find_element(By.XPATH, '//android.widget.TextView[@text="Mobile Number"]').click()

            未寫完
            self.driver.find_element(By.ID, 'RNE__Input__text-input').send_keys(paramet.login['mobile'])
            logging.info('mobile is:%s' % paramet.login['mobile'])
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//android.view.ViewGroup[@content-desc="testID_NextButton"]/android.widget.TextView').click()
            time.sleep(1)

            # 填寫登入信息
            self.driver.find_element(By.XPATH, '//android.widget.EditText[@text="• • • • • • • •"]').send_keys(paramet.login['password'])
            logging.info('password is:%s' % paramet.login['password'])
            time.sleep(2)
            self.driver.find_element_by_android_uiautomator('new UiSelector().text("SHOW")').click()

            # 提交
            self.driver.find_element_by_xpath(
                '(//android.view.ViewGroup[@content-desc="testID_NextButton"])[2]/android.widget.TextView').click()
            time.sleep(3)
            self.pop_up()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//android.widget.TextView[@text="home"]')
        except NoSuchElementException:
            logging.error('登入失敗')
            self.getScreenShot('登入失敗')
            return False
        else:
            logging.info('登入成功')
            return True

    def pop_up(self):
        """查找pop up message（首次進入會出現）"""
        try:
            self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android'
                '.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android'
                '.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup['
                '1]/android.view.ViewGroup/android.widget.TextView[1]')
            self.driver.keyevent(4)
            self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android'
                '.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android'
                '.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup['
                '1]/android.view.ViewGroup/android.widget.TextView[1]')
        except NoSuchElementException:
            pass
        else:
            time.sleep(1)
            self.driver.keyevent(4)


if __name__ == '__main__':
    driver = appium_desired()
    l = LoginView(driver)
    l.email_login()
