#!/usr/bin/env python
# coding:utf-8

import pytest
import allure
from page_objects.login_page import LoginPage
from data import paramet
import logging

@allure.feature("登入")
class TestLogin:
    @allure.story("成功登入")
    @allure.title("使用有效賬號登入")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_mobile_login(self):
        """
        測試User使用有效的手機號和Code能否成功登入系統
        
        步驟:
        1. 啟動App
        2. 打開登入頁面
        3. 允許系統彈窗
        4. 略過啟動圖
        5. 關閉廣告
        6. 點擊登入按鈕
        7. 同意個人資料收集 
        8. 同意服務條款和隱私政策
        9. 點擊手機號登入
        10. 輸入有效的手機號
        11. 點擊獲取驗證碼
        12. 輸入有效的驗證碼
        13. 點擊登入按鈕
        14. 驗證是否成功進入系統
        """
        from common.desired_caps import appium_desired
        driver = appium_desired()
        page = LoginPage(driver)
        mobile = paramet.login['mobile']
        code = paramet.login['code']
        with allure.step(f"使用帳號 {mobile} 登入系統"):
            # 驗證首頁已出現“我的獎賞”元素，視為登入成功
            assert page.login_action(), "登入後未找到'我的獎賞'，登入流程失敗"
            logging.info("登入測試完成，成功登入系統")
        driver.quit()
