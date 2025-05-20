# -*- coding: utf-8 -*-
# @Author  : 白苏子_
# @File    : run.py
import os
import shutil

import pytest

from common_utils.allure_report_utils import environment_setting, set_report_executer_on_results


def clean_dir(directory):
    root_path = r"D:\Desktop\autoUI\ui_framework"
    if directory in os.listdir(root_path):
        shutil.rmtree(os.path.join(root_path, directory))
        os.mkdir(os.path.join(root_path, directory))
    else:
        os.mkdir(os.path.join(root_path, directory))


if __name__ == '__main__':
    # 每次执行前先清空screenshots与logs目录下文件
    clean_dir("logs")
    clean_dir("screenshots")

    # import放在这个位置是为了避免加载module时无法对logs和screenshots下的文件进行清除
    # 导入以下模块会占用logs下文件的读取进程，故清除该目录下文件时会报错
    from common_utils.config_parse_utils import conf
    from common_utils.log_utils import logs
    from common_utils.yaml_utils import read_yaml, clean_yaml
    try:
        # config.yaml是否存在
        if r"D:\Desktop\autoUI\ui_framework\config.yaml":
            # 更改测试网址后，自动清除cookie.yaml中的cookie数据
            cookie_yaml_path = conf.get_file_path("cookie.yaml")
            if read_yaml(cookie_yaml_path):
                cookie_yaml_url = read_yaml(cookie_yaml_path)["domain"]
                config_host_url = conf.get_host()
                if cookie_yaml_url != config_host_url:
                    clean_yaml(cookie_yaml_path)

            pytest.main()
            environment_setting()  # 将配置文件中需要展示的东西展示在报告环境变量中
            # 将allure报告中的环境变量配置文件放到temp文件夹中
            shutil.copy("./environment.properties","./reports/temp")
            # 将allure报告中的分类模块配置文件放到temp文件夹中
            # shutil.copy("./categories.json", "./reports/temp")
            # shutil.copy("./executor.json", "./reports/temp")
            # generate: 指定生成报告所用到的数据源（json文件）存放路径
            # -o: output,自动生成allure报告的路径，默认是在当前路径下创建allure-report文件夹
            # ./reports/allure_report: 指定-o创建测试报告存放路径 --clean:清除上次的报告
            os.system('allure generate ./reports/temp -o ./reports/allure_report --clean')
    except Exception as e:
        logs.error("未找到系统配置文件config.yaml")
        raise e
