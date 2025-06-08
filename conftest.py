import os
import shutil
import pytest
from page_objects.login_page import LoginPage
from common.desired_caps import appium_desired

@pytest.fixture(scope="session", autouse=True)
def clean_logs_reports_screenshots():
    """每次運行測試前，自動清理 logs、reports/allure-results 和 screenshots 目錄內容"""
    base_dir = os.path.dirname(__file__)
    logs_dir = os.path.join(base_dir, 'logs')
    reports_dir = os.path.join(base_dir, 'reports', 'allure-results')
    screenshots_dir = os.path.join(base_dir, 'screenshots')
    for folder in [logs_dir, reports_dir, screenshots_dir]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

# @pytest.fixture(scope="function")
# def login_flow():
#     """每次都完整執行一次登入流程，適用於登入功能測試用例"""
#     driver = appium_desired()
#     page = LoginPage(driver)
#     page.start_app_unlogin()
#     page.login_action()
#     yield page
#     driver.quit()

@pytest.fixture(scope="session")
def app_logged_in():
    """只在本輪測試會話首次登入，後續用例共用已登入App，適用於登入後功能測試"""
    driver = appium_desired()
    page = LoginPage(driver)
    page.start_app_login()
    yield page
    driver.quit()

@pytest.fixture(scope="function")
def app_unlogin():
    """啟動App並確保未登入狀態,供用例調用（如需未登入場景）"""
    driver = appium_desired()
    page = LoginPage(driver)
    page.start_app_unlogin()
    yield page
    driver.quit()
