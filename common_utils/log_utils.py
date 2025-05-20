# -*- coding: utf-8 -*-
# @Author  : 白苏子_
# @File    : log_utils.py
"""
日志工具封装
"""

import datetime
import os
import time
import logging
import colorlog
from logging.handlers import RotatingFileHandler
from common_utils.config_parse_utils import conf

# 日志文件存放路径，后期通过配置文件配置
log_file_path = conf.get_file_path('logs')

# 目录下不存在日志文件存放路径时，创建logs文件夹
if not os.path.exists(log_file_path):
    os.mkdir(log_file_path)

# 日志文件名称格式
log_name = log_file_path + r"\{}.log".format(time.strftime("%Y-%m-%d"))


class LogHandler:

    def setting_log_color(self):
        log_color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'ERROR': 'red',
            'WARNING': 'yellow',
            'CRITICAL': 'red',
        }
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s %(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s',
            log_colors=log_color_config
        )

        return formatter

    def output_logs(self):
        # 实例化对象
        logger = logging.getLogger(__name__)
        stream_format = self.setting_log_color()
        if not logger.handlers:
            # 设置日志默认打印级别
            logger.setLevel(logging.DEBUG)
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s'
            )
            # 将日志输出到控制台上
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            # 控制台输出的是带颜色的日志
            sh.setFormatter(stream_format)
            logger.addHandler(sh)

            # 将日志输出到文件
            # 追加模式，最大字节数1024*1024=1MB，最多保留backupCount个日志文件,自动生成test.log、test.log.1、test.log.2等
            fh = RotatingFileHandler(filename=log_name, mode='a', encoding='utf-8', maxBytes=1024 * 1024 * 20,
                                     backupCount=7)
            fh.setLevel(logging.DEBUG)
            # 文件中输出的不带颜色的日志
            fh.setFormatter(log_format)
            logger.addHandler(fh)

        return logger


loghandler = LogHandler()
logs = loghandler.output_logs()

