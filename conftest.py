import os
import shutil
import pytest
from page_objects.login_page import LoginPage

@pytest.fixture(scope="session", autouse=True)
def clean_reports_and_screenshots():
    """每次運行測試前，自動清理 reports/allure-results 和 screenshots 目錄內容"""
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports', 'allure-results')
    screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    for folder in [reports_dir, screenshots_dir]:
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

@pytest.fixture(scope="function")
def app_unlogin():
    """啟動App並確保未登入狀態，供用例調用"""
    page = LoginPage()
    page.start_app_unlogin()
    yield page
    # 測試結束後自動關閉App
    if hasattr(page, 'driver'):
        page.driver.quit()

@pytest.fixture(scope="function")
def app_login():
    """啟動App並確保已登入狀態，供用例調用"""
    page = LoginPage()
    page.start_app_login()
    yield page
    # 測試結束後自動關閉App
    if hasattr(page, 'driver'):
        page.driver.quit()
