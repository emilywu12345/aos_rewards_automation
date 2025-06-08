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
    # 我的賬戶菜單按鈕（根据 Inspector 精准 class+content-desc）
    myAccountBtn = (By.XPATH, '//android.view.View[@content-desc="我的帐户"]')
    # 立即加入
    joinNowBtn = (By.XPATH, '//android.view.ViewGroup[@content-desc="立即加入"]')

    # 登入或註冊按鈕
    loginBtn = (By.XPATH, '//android.view.ViewGroup[@content-desc="登入 / 加入 S⁺ REWARDS"]')

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
        """判斷是否已登入,返回True/False"""
        try:
            self.find_element_wait(self.myReward, timeout=5)
            return True
            self.getScreenShot
        except Exception:
            return False
            self.getScreenShot('未登入狀態')


    @allure.step("執行正常登入操作")
    def login_action(self):
        logging.info('==========mobile_login==========='
)
        try:
            time.sleep(1)
            # self.start_app()
            # 允許權限彈窗
            self.find_element(*self.agreeBtn).click()
            time.sleep(2)
            # 跳過啟動圖
            self.find_element(*self.skipBtn).click()
            # time.sleep(5)
            # # 點擊廣告
            # self.find_element(*self.adCloseBtn).click()
            # # 點擊返回按鈕
            # time.sleep(2)
            # self.find_element(*self.backBtn).click()
            time.sleep(2)
            self.find_element(*self.myAccountBtn).click()
            self.find_element(*self.joinNowBtn).click()
            time.sleep(1)
            self.find_element(*self.loginBtn).click()
            time.sleep(10)
            # 向上滑動多次，確保元素可見
            for _ in range(20):
                self.swipeUp()
                time.sleep(0.3)
            # 點擊個人資料收集框、同意服務條款和隱私政策
            self.find_element(*self.personalData).click()
            self.find_element(*self.agreeCheck).click()
            self.find_element(*self.agreeCheck1).click()
            self.find_element(*self.acceptBtn).click()
            self.find_element(*self.mobileBtn).click()
            self.find_element(*self.mobileInput).send_keys(paramet.login['mobile'])
            logging.info('mobile is:%s' % paramet.login['mobile'])
            self.find_element(*self.getCodeBtn).click()
            self.find_element(*self.codeInput).send_keys(paramet.login['code'])
            logging.info('code is:%s' % paramet.login['code'])
            time.sleep(1)  
            self.find_element(*self.myReward).click()
            time.sleep(2)  
            return True
        except NoSuchElementException as e:
            logging.error(f'登入過程中未找到某些元素: {e}')
            self.getScreenShot('登入元素未找到')
            return False    
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
            time.sleep(2)
            # 處理允許權限彈窗
            self.find_element(*self.agreeBtn).click()
            time.sleep(2)
            # 處理跳過啟動圖
            self.find_element(*self.skipBtn).click()
            time.sleep(5)
            # 等待廣告元素出現並點擊關閉
            WebDriverWait(self.driver, 3, 0.5).until(EC.element_to_be_clickable(self.adCloseBtn)).click()
            # 點擊返回按鈕
            time.sleep(2)
            self.find_element(*self.backBtn).click()
            logging.info('App啟動並處理彈窗/廣告成功')
        except NoSuchElementException as e:
            logging.info(f'啟動App時未找到某些元素: {e}')
            self.getScreenShot('啟動App元素未找到')

    def start_app_unlogin(self):
        """启动App并确保未登录状态"""
        # self.start_app()
        # 可在此处补充确保未登录的逻辑，如检测/退出已登录账号
        # 例如：如果已登录则执行登出操作
        if self.is_logged_in():
            # TODO: 可补充登出操作
            logging.info("检测到已登录，建议补充登出操作")
        else:
            logging.info("已处于未登录状态")

    def start_app_login(self):
        """启动App并确保已登录状态"""
        # self.start_app()
        if not self.is_logged_in():
            self.login_action()
        else:
            logging.info("已处于已登录状态")

