# -*- coding: utf-8 -*-
# @Author  : 白苏子_
# @File    : conftest.py
import os
import time
from datetime import timedelta

import allure
import pytest
from selenium import webdriver

from common_utils.config_parse_utils import conf
from common_utils.log_utils import logs
from common_utils.yaml_utils import read_yaml
from keywords_utils.keywords import KeyWords as KW


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    收集测试结果
    :param terminalreporter:
    :param exitstatus:
    :param config:
    :return:
    """
    # 所有用例执行信息
    # all_cases_info = terminalreporter.stats
    # 执行的用例总数
    cases_total = terminalreporter._numcollected
    # 通过的用例总数
    passed_cases_num = len(terminalreporter.stats.get('passed', []))
    # 失败的用例总数
    failed_cases_num = len(terminalreporter.stats.get('failed', []))
    # 错误的用例总数
    error_cases_num = len(terminalreporter.stats.get('error', []))
    # 跳过的用例总数
    # skipped_cases_num = len(terminalreporter.stats.get('skipped', []))
    # 成功率
    passed_ratio = f"{passed_cases_num / cases_total * 100:.0f}%" if cases_total > 0 else "N/A"
    failed_ratio = f"{failed_cases_num / cases_total * 100:.0f}%" if cases_total > 0 else "N/A"
    error_ration = f"{error_cases_num / cases_total * 100:.0f}%" if cases_total > 0 else "N/A"
    # terminalreporter._sessionstarttime 会话开始时间
    duration_total = round(time.time() - terminalreporter._sessionstarttime, 2)
    # 将总秒数格式化为时分秒格式
    duration = str(timedelta(seconds=duration_total)).split('.')[0]
    msg = f"""
        用例总数：{cases_total}
        通过总数：{passed_cases_num} 通过率：{passed_ratio}
        失败总数：{failed_cases_num} 失败率：{failed_ratio}
        错误总数：{error_cases_num} 错误率：{error_ration}
        执行时间：{duration_total}s ({duration})
    """

    print(msg)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    # 钩子函数作用:用例执行失败时截图
    :param item:
    :param call:
    :return:
    """
    try:
        # 什么时候去识别用例的执行结果呢？
        # 后置处理 yield：表示测试用例执行完了
        outcome = yield
        rep = outcome.get_result()  # 获取测试用例执行完成之后的结果
        if rep.when == 'call' and rep.failed:  # 判断用例执行情况：被调用并且失败
            # 实现失败截图并添加到allure附件。截图方法需要使用driver对象，想办法把driver传过来
            # 如果操作步骤过程中有异常，那么用例失败，在这里完成截图操作
            screenshots_path = os.path.join(conf.get_file_path('screenshots'), "执行失败.png")
            driver.save_screenshot(screenshots_path)
            # 将截图展示在allure测试报告上
            allure.attach.file(
                source=screenshots_path,
                name='断言失败或执行异常截图',
                attachment_type=allure.attachment_type.PNG
            )
    except Exception as e:
        logs.error(f"用例失败时保存截图失败，错误原因{e}")
        raise e


@pytest.fixture(scope="session")
def driver():
    """
    用例执行的前后置操作
    :return:
    """
    # 01 用例前置
    # 初始化浏览器
    # 定义全局变量driver，本文件的其他fix也可以用
    global driver
    # 根据config.ini中的[Browser]浏览器，实例化driver
    match conf.get_browser():
        case "Chrome":
            driver = webdriver.Chrome()
        case "Firefox":
            driver = webdriver.Firefox()
    driver.maximize_window()
    # 执行登录操作
    KW(driver).打开网址(conf.get_host())
    if read_yaml(conf.get_file_path("cookie.yaml")):
        KW(driver).添加cookie()
    else:
        KW(driver).点击(**{"元素对象": '//*[@id="account"]/ul/li[1]/a'})
        KW(driver).发送数据(**{"元素对象": '//*[@id="username"]', "数据对象": conf.get_username()})
        KW(driver).发送数据(**{"元素对象": '//*[@id="password"]', "数据对象": conf.get_passwd()})
        KW(driver).点击(**{"元素对象": '//*[@id="login-submit"]'})
        # 登录成功后获取cookie并写入cookie.yaml文件
        KW(driver).获取cookie()
    # 02 用例执行，返回driver
    yield driver
    # 03 用例后置，关闭浏览器
    driver.quit()


@pytest.fixture(scope="session")
def Keywords(driver):
    """
    初始化关键字类对象
    :param driver:
    :return:
    """
    return KW(driver)
