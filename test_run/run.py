#!/usr/bin/env python
# coding:utf-8

import HTMLTestRunner
import os
import time
import unittest


def all_case():
    # 执行测试用例的目录(当前目录)
    case_dir = r"..\tests"
    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir, pattern='test*.py', top_level_dir=None)
    # discover方法筛选出来的用例，循环添加到测试套件中
    for test_suit in discover:
        for test_case in test_suit:
            # 添加用例到testcase
            testcase.addTest(test_case)
    print(testcase)
    return testcase


if __name__ == "__main__":
    # 返回实例
    # runner = unittest.TextTestRunner()
    # 生成测试报告
    # 选择指定时间格式
    timestr = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    # 定义测试报告存放路径和报告名称
    Report = os.path.join(os.path.dirname(os.getcwd()), r'reports\report_' + timestr + '.html')
    with open(Report, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, verbosity=2, title='测试报告', description='测试用例执行情况')
        # run所有用例
        runner.run(all_case())
        f.close()
