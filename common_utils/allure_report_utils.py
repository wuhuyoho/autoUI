# -*- coding: utf-8 -*-
# @Author  : 白苏子_
# @File    : allure_report_utils.py
"""
allure报告相关配置工具封装
"""
import json

from common_utils.config_parse_utils import conf


def environment_setting():
    """
    将配置文件中需要在allure报告中展示的配置展示在报告中
    :return:
    """
    # 需要展示什么就在这个字典中加入什么即可
    setting_dict = {
        "baseUrl": conf.get_host(),
        "Browser": conf.get_browser()
    }
    # 先对文件进行清空
    with open(conf.get_file_path('environment.properties'), "w", encoding="utf-8") as f:
        f.truncate()
    # 将数据写入文件
    with open(conf.get_file_path('environment.properties'), "a", encoding="utf-8") as f:
        for keys, values in setting_dict.items():
            setting_data = f"{keys}={values}\n"
            f.write(setting_data)


def set_report_executer_on_results():
    """
    在allure-results报告的目录下生成一个写入了执行人的文件：executor.json
    @return:
    """
    # 需要写入的环境信息
    allure_executor = {
        "name": "张三",
        "type": "jenkins",
        "url": "http://localhost:63342/ui_framework/reports/allure_report/index.html",  # allure报告的地址
        "buildOrder": 3,
        "buildName": "allure-report_deploy#1",
        "buildUrl": "http://helloqa.com/#1",
        "reportUrl": "http://helloqa.com/#1/AllureReport",
        "reportName": "张三 Allure Report"
    }
    # allure_env_file = os.path.join({你的自动生成allureresult报告目录}, 'executor.json')
    with open(r"D:\Desktop\autoUI\ui_framework\reports\temp", 'w', encoding='utf-8') as f:
        f.write(str(json.dumps(allure_executor, ensure_ascii=False, indent=4)))

