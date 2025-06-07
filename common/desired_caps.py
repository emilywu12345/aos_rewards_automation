# -*- coding: UTF-8 -*-
import yaml
import logging.config
from appium import webdriver
from appium.options.android import UiAutomator2Options
import os

# 定義日誌文件路徑，並確保目錄和文件存在
log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs/run.log'))
if not os.path.exists(os.path.dirname(log_file_path)):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as f:
        f.write('')

# 從指定的配置文件加載日誌配置
CON_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/log.conf'))
logging.config.fileConfig(CON_LOG)

# 創建一個日誌記錄器實例，用於記錄日誌消息
logging = logging.getLogger()


def appium_desired():
    caps_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/caps.yaml'))
    with open(caps_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    desired_caps = {}
    desired_caps['udid'] = data['udid']
    desired_caps['platformName'] = data['platformName']

    desired_caps['platformVersion'] = data['platformVersion']
    desired_caps['deviceName'] = data['deviceName']

    base_dir = os.path.dirname(os.path.dirname(__file__))
    app_path = os.path.join(base_dir, 'app', data['appname'])
    desired_caps['app'] = app_path

    # "True"默認不會重置會話
    desired_caps['noReset'] = False
    desired_caps['newCommandTimeout'] = data['newCommandTimeout']

    # Send_keys()傳入中文時需要在capability中配置
    desired_caps['unicodeKeyboard'] = data['unicodeKeyboard']
    desired_caps['resetKeyboard'] = data['resetKeyboard']

    desired_caps['appPackage'] = data['appPackage']
    desired_caps['appActivity'] = data['appActivity']

    logging.info('start run app...')
    options = UiAutomator2Options()
    options.load_capabilities(desired_caps)
    driver = webdriver.Remote('http://' + str(data['ip']) + ':' + str(data['port']), options=options)

    driver.implicitly_wait(40)
    return driver


if __name__ == '__main__':
    appium_desired()
