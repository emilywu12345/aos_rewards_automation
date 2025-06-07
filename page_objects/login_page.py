#!/usr/bin/env python
# coding:utf-8

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from common.desired_caps import appium_desired
from common.common_fun import Common
from data import paramet
import logging
import time
import allure
import pytest
from page_objects.basepage import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class LoginPage(Common):
    # 啟動App元素定位
    # 允許系統彈窗
    agreeBtn = (By.ID, 'com.android.permissioncontroller:id/permission_allow_button')
    # 略過啟動圖
    skipBtn = (By.XPATH, '//android.widget.TextView[@text="略过"]')
   
    # 廣告關閉按鈕
    adCloseBtn = (By.XPATH, '//android.view.ViewGroup[@resource-id="__CAROUSEL_ITEM_0_READY__"]//android.widget.ImageView')

    # 返回按鈕
    backBtn = (By.XPATH, '//android.widget.Button[@content-desc="Go back"]/android.widget.ImageView')
    # 登入元素定位
    # 首頁登入按鈕
    loginBtn = (By.XPATH, '//android.widget.TextView[@text="登入或注册以探索更多！"]')
    
    #  個人資料收集框
    personalData = (By.XPATH, '(//android.widget.TextView[@resource-id="RNE__Checkbox__Icon"])[1]')
    #  同意S+ REWARDS服務條款框
    agreeCheck = (By.XPATH, '(//android.widget.TextView[@resource-id="RNE__Checkbox__Icon"])[2]')
    #  同意S+ REWARDS隱私政策
    agreeCheck1 = (By.XPATH, '(//android.widget.TextView[@resource-id="RNE__Checkbox__Icon"])[3]')
    # 接受按鈕
    acceptBtn = (By.XPATH, '//android.view.ViewGroup[@content-desc="接受"]')
    # 手機號碼登入按鈕
    mobileBtn = (By.XPATH, '//android.widget.Button[@content-desc="手机号码"]')
    # 手機號碼輸入框
    mobileInput = (By.XPATH, '//android.widget.EditText[@resource-id="RNE__Input__text-input"]')
    # 獲取驗證碼按鈕
    getCodeBtn = (By.XPATH, '//android.widget.Button[@content-desc="取得验证码"]')
    # 驗證碼輸入框
    codeInput = (By.XPATH, '//android.widget.EditText[@resource-id="RNE__Input__text-input"]')
    # 首頁我的獎賞
    myReward = (By.XPATH, '//android.widget.TextView[@text="我的奖赏"]')
    # 判斷是否已登入，返回True/False
    def is_logged_in(self):
        """判斷是否已登入，返回True/False"""
        try:
            self.find_element_wait(self.myReward, timeout=5)
            return True
        except Exception:
            return False

    def find_element_wait(self, locator, timeout=10):
        """顯式等待元素出現並返回元素"""
        wait = WebDriverWait(self.driver, timeout, 0.5)
        return wait.until(EC.presence_of_element_located(locator))

    # 登入操作
    @allure.step("執行正常登入操作")
    def login_action(self):
        logging.info('==========mobile_login===========')
        try:
            time.sleep(2)
            self.start_app()
            time.sleep(2)
            self.find_element_wait(self.loginBtn).click()
            self.swipeUp()
            self.find_element_wait(self.personalData).click()
            self.find_element_wait(self.agreeCheck).click()
            self.find_element_wait(self.agreeCheck1).click()
            self.find_element_wait(self.acceptBtn).click()
            self.find_element_wait(self.mobileBtn).click()
            self.find_element_wait(self.mobileInput).send_keys(paramet.login['mobile'])
            logging.info('mobile is:%s' % paramet.login['mobile'])
            self.find_element_wait(self.getCodeBtn).click()
            self.find_element_wait(self.codeInput).send_keys(paramet.login['code'])
            logging.info('code is:%s' % paramet.login['code'])
            time.sleep(2)
            self.find_element_wait(self.myReward).click()
            time.sleep(5)
            return True
        except Exception as e:
            logging.error(f'登入失敗: {e}')
            self.getScreenShot('登入失敗')
            return False

    # 啟動App
    @allure.step("啟動App並處理彈窗/廣告")
    def start_app(self):
        """啟動App後處理彈窗、廣告、跳過頁面等"""
        logging.info('==========start_app===========')

        try:
            # 處理允許權限彈窗
            self.find_element(*self.agreeBtn).click()
            logging.info("點擊允許權限彈窗")
            # 處理跳過啟動圖
            self.find_element(*self.skipBtn).click()
            logging.info("點擊跳過啟動圖")
            # 等待廣告元素出現並點擊關閉
            time.sleep(5)  # 等待廣告元素加載
            wait = WebDriverWait(self.driver, 5, 0.5)
            wait.until(EC.element_to_be_clickable(self.adCloseBtn)).click()
            time.sleep(4)
            self.find_element(*self.backBtn).click()  # 點擊返回按鈕
            time.sleep(2)
            return True
        except NoSuchElementException:
            logging.info("未出現廣告彈窗")
            return False

    # 啟動App（未登入狀態）
    @allure.step("啟動App-未登入狀態")
    def start_app_unlogin(self):
        logging.info('==========start_app_unlogin===========')
        try:
            self.start_app()
            if self.is_logged_in():
                logging.info('檢測到已登入，執行登出流程')
                # TODO: 補充登出操作
                # self.logout_action()
            else:
                logging.info('當前為未登入狀態')
        except Exception as e:
            logging.error(f'start_app_unlogin異常: {e}')
            self.getScreenShot('異常_start_app_unlogin')
            raise
        return self

    # 啟動App（已登入狀態）
    @allure.step("啟動App-已登入狀態")
    def start_app_login(self):
        logging.info('==========start_app_login===========')
        try:
            self.start_app()
            if not self.is_logged_in():
                logging.info('未登入，執行登入流程')
                if not self.login_action():
                    raise Exception('登入流程失敗')
            else:
                logging.info('已處於登入狀態')
        except Exception as e:
            logging.error(f'start_app_login異常: {e}')
            self.getScreenShot('異常_start_app_login')
            raise
        return self
