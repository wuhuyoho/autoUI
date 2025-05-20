# -*- coding: utf-8 -*-
# @Author  : 白苏子_
# @File    : case_data_parse_utils.py
"""
测试用例数据解析工具
"""

import random

from common_utils.log_utils import logs


def generate_random_letters(n):
    """
    生成随机小写字母组合
    :param n:
    :return:
    """
    try:
        letters = 'abcdefghijklmnopqrstuvwxyz'
        random_letters = ''.join(random.choice(letters) for _ in range(n))
        logs.info(f"生成随机数据{random_letters}")
        return random_letters
    except Exception as e:
        logs.error(f"随机数据生成失败！错误原因：{e}")
        raise e

def case_data_prase(raw_case_data: dict, random_letter: str):
    """
    对原始的case.yaml文件中的测试步骤数据进行解析，把具有唯一性的数据对象，通过随机数改成唯一数据
    对断言中需要与某一步骤中的数据对象相同的值，进行传递
    :param raw_case_data: 测试步骤数据
    :param random_letter: 随机数据
    :return:
    """
    for key in raw_case_data.keys():
        value = raw_case_data[key]
        value_type = type(value)
        if value_type is dict:
            case_data_prase(value, random_letter)
        else:
            if type(value) is str:
                if value.startswith('$'):
                    new_data = random_letter + '_' + value.replace("$", "", 2)
                    raw_case_data[key] = new_data
                elif value.endswith('$'):
                    new_data = generate_random_letters(5) + '_' + value.replace("$", "", 1)
                    raw_case_data[key] = new_data
                else:
                    raw_case_data[key] = value
    new_case_data = raw_case_data
    return new_case_data


