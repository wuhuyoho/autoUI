# -*- coding: utf-8 -*-
# @Author  : 白苏子_
# @File    : yaml_utils.py
"""
yaml文件解析工具
"""
import yaml

from common_utils.config_parse_utils import conf
from common_utils.log_utils import logs

# 用例yaml文件存放的绝对路径
case_yaml_path = conf.get_file_path('cases')


def read_yaml(yaml_file_path: str) -> list:
    """
    读取数据
    :param yaml_file_path: 数据文件路径
    :return: pytest参数化所需数据列表
    """
    try:
        with open(yaml_file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)
        logs.info(f"case.yaml文件数据{yaml_data}")
        return yaml_data
    except Exception as e:
        logs.error(f"读取{yaml_file_path}文件数据失败，错误原因：{e}")
        raise e


def write_yaml(yaml_file_path, dict_data):
    """
    将dict数据写入yaml问价
    :param yaml_file_path:
    :param dict_data:
    :return:
    """
    with open(yaml_file_path, 'w', encoding='utf-8') as f:
        yaml.dump(stream=f, data=dict_data, allow_unicode=True, sort_keys=False)


def clean_yaml(yaml_file_path):
    """
    清空yaml文件
    :param yaml_file_path:
    :return:
    """
    with open(yaml_file_path, 'w', encoding='utf-8') as f:
        f.truncate()



