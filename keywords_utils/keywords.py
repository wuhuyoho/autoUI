# -*- coding: utf-8 -*-
# @Author  : 白苏子_
# @File    : keywords.py

import os.path
from time import sleep

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from common_utils.config_parse_utils import conf
from common_utils.log_utils import logs
from common_utils.yaml_utils import write_yaml, read_yaml

"""
selenium浏览器操作关键字封装
"""


class KeyWords:

    def __init__(self, webdriver):
        self.driver = webdriver

    def 打开网址(self, url: str) -> None:
        """
        打开测试网址
        :param url: 测试系统地址
        :return: None
        """
        try:
            self.driver.get(url)
            logs.info(f"打开网址成功，url:{url}")
        except Exception as e:
            raise logs.error(f"打开网址失败，url:{url}，错误原因{e}")

    def 元素定位器(self, xpath_data: str):
        try:
            return self.driver.find_element(By.XPATH, xpath_data)
        except Exception as e:
            logs.error("元素定位失败，请检查xpath路径")
            raise e

    # ############ 获取页面或元素信息 ###########

    def 获取页面标题(self):
        try:
            logs.info(f"页面标题:{self.driver.title}")
            return self.driver.title
        except Exception as e:
            logs.error(f"获取页面标题失败，错误原因:{e}")
            raise e

    def 获取当前页面url(self):
        try:
            logs.info(f"当前页面url:{self.driver.current_urle}")
            return self.driver.current_urle
        except Exception as e:
            logs.error(f"获取当前页面url失败，错误原因:{e}")
            raise e

    def 获取页面源码(self):
        try:
            logs.info(f"页面源码:{self.driver.page_source}")
            return self.driver.page_source
        except Exception as e:
            logs.error(f"获取页面源码失败，错误原因:{e}")
            raise e

    # ########### 页面或元素操作 ##################

    def 获取cookie(self):
        """
        获取cookie并写入cookie.yaml
        :return:
        """
        try:
            cookies = self.driver.get_cookies()[0]
            write_yaml(conf.get_file_path("cookie.yaml"), cookies)
            logs.info(f"cookie:{cookies}")
            return cookies
        except Exception as e:
            logs.error(f"获取cookie！错误原因:{e}")
            raise e

    def 添加cookie(self):
        """
        删除cookie，将cookie.yaml中的数据添加到页面
        :return:
        """
        try:
            self.driver.delete_all_cookies()  # 删除所有cookie
            cookie = read_yaml(conf.get_file_path("cookie.yaml"))
            self.driver.add_cookie(cookie)
            sleep(1)
            self.刷新()
            logs.info("cookie保持登录成功！")
        except Exception as e:
            logs.error(f"添加cookie失败！错误原因:{e}")
            raise e

    def 刷新(self):
        self.driver.refresh()

    def 返回(self):
        self.driver.back()

    def 点击(self, **kwargs) -> None:
        """
        左键单击
        yaml中数据格式:
         step_name:
            点击:
                元素对象: ele_obj
        :param kwargs: 元素对象: str
        :return: None
        """
        try:
            # self.driver.find_element(By.XPATH, kwargs["元素对象"]).click()
            self.元素定位器(kwargs["元素对象"]).click()
            logs.info(f"点击成功，元素对象：{kwargs["元素对象"]}")
        except Exception as e:
            logs.error(f"点击失败，元素对象:{kwargs["元素对象"]}，错误原因{e}")
            raise e

    def 发送数据(self, **kwargs) -> None:
        """
        发送数据
        yaml中数据格式:
         step_name:
            发送数据:
                元素对象: ele_obj
                数据对象: data_obj
        :param kwargs: 元素对象: str
                       数据对象: str or int
        :return: None
        """
        try:
            # 先对输入框进行清空，再发送数据
            # self.driver.find_element(By.XPATH, kwargs["元素对象"]).clear()
            # self.driver.find_element(By.XPATH, kwargs["元素对象"]).send_keys(kwargs["数据对象"])
            self.元素定位器(kwargs["元素对象"]).clear()
            self.元素定位器(kwargs["元素对象"]).send_keys(kwargs["数据对象"])
            logs.info(f"发送数据成功，元素对象:{kwargs["元素对象"]}，数据对象:{kwargs["数据对象"]}")
        except Exception as e:
            logs.error(f"发送数据失败，元素对象:{kwargs["元素对象"]}，数据对象:{kwargs["数据对象"]}，错误原因{e}")
            raise e

    def 下拉框选择(self, **kwargs):
        """
        下拉框选项单选或多选
        yaml中数据格式:
         step_name:
            下拉框选择:
                元素对象: ele_obj
                选项: ["选项名称1","选项名称2"....]
        :param kwargs: 元素对象、选项
        :return:
        """
        try:
            s = Select(kwargs["元素对象"])  # 实例化Select对象
            if list(kwargs["选项"]):
                for item in kwargs["选项"].items():
                    s.select_by_visible_text(item)  # 根据文字进行选择，kwargs["选项"]:list,list中至少一个选项
                logs.info(f"下拉选择选项{kwargs["选项"]}成功！")
            else:
                raise "下拉框中未选择选项，请检查数据是否正确！"
        except Exception as e:
            logs.error(f"下拉框单选失败，元素对象:{kwargs["元素对象"]},选项{kwargs["选项"]},错误原因:{e}")
            raise e

    def 下拉框取消选择(self, **kwargs):
        """
        取消选择下拉框某个或某几个选项
        yaml中数据格式:
         step_name:
            下拉框取消选择:
                元素对象: ele_obj
                选项: ["选项名称1","选项名称2"....]
        :param kwargs:
        :return:
        """
        try:
            s = Select(kwargs["元素对象"])  # 实例化Select对象
            if list(kwargs["选项"]):
                for item in kwargs["选项"].items():
                    s.deselect_by_visible_text(item)  # 根据文字进行选择，kwargs["选项"]:list,list中至少一个选项
                logs.info(f"下拉框取消选择选项{kwargs["选项"]}成功！")
            else:
                raise "下拉框中未取消选择任何选项，请检查数据是否正确！"
        except Exception as e:
            logs.error(f"下拉框取消选择失败，元素对象:{kwargs["元素对象"]},选项{kwargs["选项"]},错误原因:{e}")
            raise e

    def 下拉框取消全选(self, **kwargs):
        """
        取消选择下拉框内所有选项
        yaml中数据格式:
         step_name:
            下拉框取消全选:
                元素对象: ele_obj
        :param kwargs:
        :return:
        """
        try:
            s = Select(kwargs["元素对象"])
            s.deselect_all()
            logs.info("下拉框取消选项所有选项成功！")
        except Exception as e:
            logs.error(f"下拉框取消全选失败，元素对象:{kwargs["元素对象"]}")
            raise e

    # ########### 逻辑处理 ##################

    def 显性等待(self, **kwargs) -> object:
        """
         利用显性等待，元素可见时返回元素对象
         yaml中数据格式:
         step_name:
            显性等待:
                等待时间: int_num
                元素对象: ele_obj
        :param kwargs: 等待时间、元素对象
        :return:
        """
        try:
            WebDriverWait(self.driver, timeout=kwargs["等待时间"]).until(
                EC.visibility_of_element_located((By.XPATH, kwargs["元素对象"])))
        except Exception as e:
            logs.error(f"元素{kwargs["元素对象"]}不可见，无法定位，错误原因{e}")
            raise e

    def 暂停(self, **kwargs) -> None:
        """
        强制暂停
        yaml中数据格式:
         step_name:
            暂停:
                暂停时长: int_num
        :param kwargs: 暂停时长
        :return: None
        """
        try:
            sleep(int(kwargs["暂停时长"]))
            logs.info(f"脚本暂停{kwargs["暂停时长"]}s")
        except Exception as e:
            logs.error(f"暂停无效，time:{kwargs["暂停时长"]}，错误原因{e}")
            raise e

    def 截图(self, **kwargs) -> None:
        """
        截图
        :return:
        """

        screenshot_name = kwargs["图片名称"] + ".png"
        screenshots_path = os.path.join(conf.get_file_path('screenshots'), screenshot_name)
        try:
            self.driver.save_screenshot(screenshots_path)
            allure.attach.file(
                source=screenshots_path,
                name=kwargs["图片名称"],
                attachment_type=allure.attachment_type.PNG
            )
            logs.info(f"保存截图成功{screenshots_path}")
        except Exception as e:
            logs.error(f"保存截图失败{screenshots_path}，错误原因{e}")
            raise e

    def 切人iframe框架(self, iframe_ele_list):
        """
        切人iframe框架，切人一层需要调用一次
        yaml中数据格式：
        step_name:
            切入iframe:
                -
                    iframe_ele_01
                -
                    iframe_ele_02
                ...
        :param iframe_ele_list: [第一层，第二层，第三层....]
        :return:
        """
        for item in iframe_ele_list:
            try:
                self.driver.switch_to.frame(self.元素定位器(item))
                logs.info(f"切人iframe框架成功,{item}")
            except Exception as e:
                logs.error(f"切入框架失败，元素对象:{item},错误原因{e}")
                raise e

    def 切出iframe框架(self):
        """
        切出到主窗口，而不是父级iframe
        :return:
        """
        try:
            self.driver.switch_to.default_content()
            logs.info("切出至主窗口成功")
        except Exception as e:
            logs.error(f"切出至主窗口失败,错误原因{e}")
            raise e

    # ############# 断言操作 #################

    def 断言页面标题是否正确(self, **kwargs):
        """
        yaml中数据格式:
         step_name:
            断言页面标题是否正确:
                期望值: expectations
                实际值: Actual
        :param kwargs: 期望值、实际值
        :return:
        """
        try:
            expectations = str(kwargs["期望值"])
            actual = str(self.driver.title)
            assert expectations == actual
            logs.info(f"断言成功：期望值{expectations}，实际值{actual}")
        except Exception as e:
            logs.error(f"断言失败！错误原因{e}")
            raise e

    def 断言元素是否可见(self, **kwargs):
        """
        yaml中数据格式:
         step_name:
            断言元素是否可见:
                元素对象：ele_obj
        :param kwargs: 元素对象
        :return:
        """
        try:
            ele = self.元素定位器(kwargs["元素对象"])
            assert ele.is_displayed
            logs.info("断言成功，元素可见！")
        except Exception as e:
            logs.error(f"断言失败，失败原因{e}")
            raise e

    def 断言元素文本是否正确(self, **kwargs):
        """
        断言位置固定的文本是否在页面中，假如新增数据一直在列表中的第n行显示，
        则可判断数据名称与第n行元素的text是否一致来进行断言
        :param kwargs:
        :return:
        """
        try:
            logs.info(f"{self.获取页面源码()}")
            expectations = str(kwargs["数据对象"])
            actual = self.元素定位器(kwargs["元素对象"]).text
            assert expectations == actual
            logs.info(f"断言成功：期望值{expectations}，实际值{actual}")
        except Exception as e:
            logs.error(f"断言失败！期望值{expectations}，实际值{actual},错误原因{e}")
            raise e

    def 断言文本是否在页面源码中(self, **kwargs):
        """
        断言位置不固定的文本是否在页面中，假如新增数据在列表中的位置是不固定显示的，
        则需要判断新增数据的名称是否在页面源码中来进行断言
        :param kwargs:
        :return:
        """
        try:
            assert kwargs["数据对象"] in self.获取页面源码()
            logs.info(f"断言成功：{kwargs["数据对象"]} in {self.获取页面源码()}")
        except Exception as e:
            logs.error(f"断言文本是否在页面源码中失败，错误原因：{e}")
            raise e
