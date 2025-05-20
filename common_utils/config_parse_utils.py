# -*- coding: utf-8 -*-
# @Author  : 白苏子_
# @File    : config_parse_utils.py
"""
config.yaml配置文件解析工具
"""
import os.path
import sys

import yaml


# 获取根目录路径
DIR_PATH = os.path.dirname(os.path.dirname(__file__))
# 将根目录添加到系统默认环境变量中
# 其他模块引用时，会在系统默认环境变量中搜索该路径
sys.path.append(DIR_PATH)


class ConfigParse:
    """
    解析config.yaml配置文件
    """

    def __init__(self, config_path=r"D:\Desktop\autoUI\ui_framework\config.yaml"):
        self.config_path = config_path
        self.read_config()

    def read_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)
        return yaml_data

    def get_host(self):
        """
        获取测试地址
        :return:
        """
        host = self.read_config()["Host"]
        return host["host"]

    def get_username(self):
        """
        获取测试用账号
        :return:
        """
        host = self.read_config()["Host"]
        return host["username"]

    def get_passwd(self):
        """
        获取测试用账号密码
        :return:
        """
        host = self.read_config()["Host"]
        return host["passwd"]

    def get_browser(self):
        """
        获取测试浏览器
        :return:
        """
        browser = self.read_config()["Browser"]
        return browser["browser"]

    def get_case_level(self):
        """
        获取需要执行的用例的等级
        :return:
        """
        case_level_list = []
        for keys, values in self.read_config()["CaseLevel"].items():
            if values == 1:
                case_level_list.append(keys)
        return case_level_list

    def get_file_path(self, var):
        """
        获取文件或文件夹路径
        :param var:
        :return:
        """
        file_path_dict = self.read_config()["SystemFilePath"]
        return os.path.join(DIR_PATH, file_path_dict[var])


conf = ConfigParse()

