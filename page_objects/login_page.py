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



class LoginPage(Common):
    # 啟動App元素定位
    # 允許系統彈窗
    agreeBtn = (By.ID, 'com.android.permissioncontroller:id/permission_allow_button')
    # 略過啟動圖
    skipBtn = (By.XPATH, '//android.widget.TextView[@text="略过"]')
    # 廣告
    adBtn = (By.XPATH, '//android.view.ViewGroup[@resource-id="__CAROUSEL_ITEM_0_READY__"]')
    # 廣告關閉按鈕
    adCloseBtn = (By.XPATH, '//android.view.ViewGroup[@resource-id="__CAROUSEL_ITEM_0_READY__"]//android.widget.ImageView')

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
    # 登入操作
    @allure.step("執行正常登入操作")
    def login_action(self):
        """mobile登入操作"""
        logging.info('==========mobile_login===========')
        try:
            time.sleep(2)
            self.start_app()  # 啟動App

            time.sleep(2)
            self.find_element(*self.loginBtn).click()  # 點擊登入按鈕
            # 向上滑動頁面到最底部
            self.swipeUp()
            self.find_element(*self.personalData).click()  # 點擊個人資料收集框
            self.find_element(*self.agreeCheck).click()  # 同意 S+ REWARDS服務條款框
            self.find_element(*self.agreeCheck1).click()  # 同意 S+ REWARDS隱私政策
            self.find_element(*self.acceptBtn).click()  # 接受按鈕
            self.find_element(*self.mobileBtn).click()  # 點擊手機號碼登入按鈕
            self.find_element(*self.mobileInput).send_keys(paramet.login['mobile'])  # 手機號碼輸入框
            logging.info('mobile is:%s' % paramet.login['mobile'])

            self.find_element(*self.getCodeBtn).click()  # 獲取驗證碼按鈕
            self.find_element(*self.codeInput).send_keys(paramet.login['code'])  # 驗證碼輸入框
            logging.info('code is:%s' % paramet.login['code'])
            time.sleep(2)
            self.find_element(*self.myReward).click()
            time.sleep(5)
            return True
        except NoSuchElementException:
            logging.error('登入失敗')
            self.getScreenShot('登入失敗')
            return False

    # 啟動App
    @allure.step("啟動App並處理彈窗/廣告")
    def start_app(self, x=953, y=279):
        """啟動App後處理彈窗、廣告、跳過頁等，保證流程健壯"""
        # 處理允許權限彈窗
        try:
            btn = self.find_element(*self.agreeBtn)
            btn.click()
            logging.info("點擊允許權限彈窗")
        except NoSuchElementException:
            logging.info("未出現允許權限彈窗")

        # 處理跳過啟動圖
        try:
            skip = self.find_element(*self.skipBtn)
            skip.click()
            logging.info("點擊跳過啟動圖")
        except NoSuchElementException:
            logging.info("未出現跳過啟動圖")

        # 處理廣告（如有）
        try:
            ad = self.find_element(*self.adBtn)
            time.sleep(2)  # 等待廣告元素穩定
            logging.info("廣告元素已找到，準備點擊關閉按鈕")
            self.getScreenShot('廣告彈窗_出現')

            # 顯式等待關閉按鈕可見
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            wait = WebDriverWait(self.driver, 8, 0.5)
            close_btn = wait.until(EC.element_to_be_clickable(self.adCloseBtn))

            # 調試：打印關閉按鈕屬性
            try:
                logging.info(f"關閉按鈕屬性: location={close_btn.location}, size={close_btn.size}, id={close_btn.get_attribute('resource-id')}, enabled={close_btn.is_enabled()}")
            except Exception as e:
                logging.warning(f"無法獲取關閉按鈕屬性: {e}")

            self.getScreenShot('廣告關閉前')
            try:
                close_btn.click()
                logging.info("點擊廣告右上角關閉按鈕")
            except Exception as e:
                logging.warning(f"常規click失敗，嘗試W3C Action: {e}")
                try:
                    from selenium.webdriver.common.actions.pointer_input import PointerInput
                    from selenium.webdriver.common.actions.action_builder import ActionBuilder
                    actions = ActionBuilder(self.driver)
                    pointer = PointerInput(interaction.POINTER_TOUCH, "touch")
                    actions.add_action(pointer.create_pointer_move(duration=0, x=close_btn.location['x']+close_btn.size['width']//2, y=close_btn.location['y']+close_btn.size['height']//2))
                    actions.add_action(pointer.create_pointer_down())
                    actions.add_action(pointer.create_pointer_up())
                    actions.perform()
                    logging.info("W3C Action 點擊廣告關閉按鈕成功")
                except Exception as e2:
                    logging.error(f"W3C Action 點擊廣告關閉按鈕失敗: {e2}")
                    self.getScreenShot('廣告關閉失敗')
                    raise
            self.getScreenShot('廣告關閉後')
            return True
        except NoSuchElementException:
            logging.info("未出現廣告彈窗")
            return False
        except Exception as e:
            logging.error(f"處理廣告彈窗異常: {e}")
            self.getScreenShot('廣告處理異常')
            return False

            # --- 調試：遍歷廣告區域下所有ImageView，打印屬性並截圖 ---
            imageviews = self.driver.find_elements(By.XPATH, "//android.view.ViewGroup[@resource-id='__CAROUSEL_ITEM_0_READY__']//android.widget.ImageView")
            logging.info(f"廣告區域下ImageView數量: {len(imageviews)}")
            for idx, iv in enumerate(imageviews):
                try:
                    desc = iv.get_attribute('content-desc')
                    resid = iv.get_attribute('resource-id')
                    size = iv.size
                    loc = iv.location
                    clickable = iv.get_attribute('clickable')
                    enabled = iv.is_enabled()
                    logging.info(f"[ImageView {idx}] desc={desc}, id={resid}, size={size}, loc={loc}, clickable={clickable}, enabled={enabled}")
                    self.getScreenShot(f'廣告ImageView_{idx}')
                except Exception as e:
                    logging.warning(f"獲取ImageView屬性失敗: {e}")
            # --- 調試結束 ---