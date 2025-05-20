# -*- coding: utf-8 -*-
# @Author  : 白苏子_
# @File    : test_cases_actuator.py
import os

import allure
import pytest

from common_utils.case_data_parse_utils import case_data_prase, generate_random_letters
from common_utils.config_parse_utils import conf
from common_utils.log_utils import logs
from common_utils.yaml_utils import read_yaml

"""
用例执行器
"""
class TestCase:
    pass


def creat_test_actuator():
    # 获取测试数据
    raw_case_yaml_data = read_yaml(os.path.join(data_yaml_path, data_yaml_name))
    random_letter_data = generate_random_letters(5)
    case_data = case_data_prase(raw_case_yaml_data["用例步骤"],random_letter_data)
    cases_data_list = [{
        "用例名称": case_name,
        "用例步骤": case_data
    }]

    # 创建用例执行器
    @allure.feature(raw_case_yaml_data["所属模块"])
    @allure.description(raw_case_yaml_data["用例描述"])
    @pytest.mark.parametrize("data", cases_data_list)
    def test_cases_actuator(self, data, Keywords):
        logs.info(raw_case_yaml_data["用例名称"])
        logs.info(f"参数化数据{data}")
        allure.dynamic.title(data["用例名称"])  # 在测试报告中展示用例名称
        # 遍历数据，得到用例名称和用例步骤
        for cases_step_name, cases_step_args in data["用例步骤"].items():
            with allure.step(cases_step_name):  # 将测试步骤名称添加进报告中
                for keys, values in cases_step_args.items():
                    # 通过"关键字"获取关键字对象
                    key_func = Keywords.__getattribute__(keys)
                    # del cases_step_args["关键字"]  # 删除数据中的"关键字"键值对
                    # 执行自动化操作，如点击、输入等
                    if isinstance(values, list):
                        key_func(values)
                    elif isinstance(values, dict):
                        key_func(**values)

    return test_cases_actuator


# 用例yaml文件存放的绝对路径
case_yaml_path = conf.get_file_path('cases')
# case_yaml_path = r"D:\Desktop\autoUI\ui_framework\cases_yaml"

case_level_list = conf.get_case_level()

# 遍历cases_yaml文件夹下的文件夹
for filename in os.listdir(case_yaml_path):
    data_yaml_path = os.path.join(case_yaml_path, filename)  # 存放yaml文件的文件夹路径
    # 遍历每个文件夹中的yaml文件
    for data_yaml_name in os.listdir(data_yaml_path):
        # 用例等级
        case_level = data_yaml_name.split("_")[0]
        if case_level in case_level_list:
            # 用例步骤名称
            case_name = data_yaml_name.split("_")[1].split(".")[0]

            test_case = "test_" + case_name
            setattr(TestCase, test_case, creat_test_actuator())
