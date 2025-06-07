#!/usr/bin/env python
# coding:utf-8

import pytest
import allure
from common.myunit import StartEnd
from page_objects.login_page import LoginPage
from data import paramet
import logging

@allure.feature("登入")
class TestLogin(StartEnd):
    @allure.story("成功登入")
    @allure.title("使用有效賬號登入")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_mobile_login(self):
        """檢查會員能否正常通過手機號登入"""
        logging.info('=======test_mobile_login=========')
        l = LoginPage(self.driver)
        mobile = paramet.login['mobile']
        code = paramet.login['code']
        with allure.step(f"使用帳號 {mobile} 登入系統"):
            result = l.login_action()
            assert result, "登入失敗"
            logging.info("登入測試完成，成功登入系統")
