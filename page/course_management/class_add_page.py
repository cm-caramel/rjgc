import time

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 添加班级弹窗。课程详情页-班级列表左下角按钮。
class ClassAddPage(BasePage):
    CLASS_SELECT = (By.XPATH, '//div[@class="el-dialog__body"]/div/div[2]//input')
    CLASS_NAME = (By.XPATH, '//div[@class="el-dialog__body"]/div/div[3]//input')
    CONFIRM_BTN = (By.XPATH, '//div[@class="el-dialog__body"]/div/div[4]/div[2]/button')
    CLASSES = (By.XPATH, '//div[@data-popper-placement="bottom-start" and @aria-hidden="false"]//span['
                         'normalize-space(text())]')
    CLASS_ITEM = '//div[@data-popper-placement="bottom-start" and @aria-hidden="false"]//span[text()="{}"]'
    RETURN_BTN = (By.XPATH, '//div[@class="el-dialog__body"]/div/div[4]/div[4]/button')
    OUTSIDE_BLANK = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/div')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def click_class_select(self):
        self.find_element(EC.visibility_of_element_located, self.CLASS_SELECT).click()

    @allure.step("选择班级")
    def select_class(self, class_names):
        for name in class_names:
            self.find_element(EC.visibility_of_element_located, (By.XPATH, self.CLASS_ITEM.format(name))).click()

    @allure.step("选择班级")
    def select_class_by_index(self, index):
        self.find_element(EC.visibility_of_all_elements_located, self.CLASSES)[index].click()

    @allure.step('获取所有行政班级')
    def get_all_classes(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.CLASSES)
        return [el.text for el in arr]

    @allure.step("输入班级名称")
    def input_class_name(self, class_name):
        el = self.find_element(EC.visibility_of_element_located, self.CLASS_NAME)
        el.clear()
        el.send_keys(class_name)

    @allure.step("点击确定按钮")
    def click_confirm_btn(self):
        self.find_element(EC.visibility_of_element_located, self.CONFIRM_BTN).click()

    @allure.step("点击返回按钮")
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step("点击空白处关闭弹窗")
    def click_outside_close(self):
        self.click_element_position(EC.presence_of_element_located, self.OUTSIDE_BLANK)

    def close_if_open(self):
        el = self.find_element(EC.presence_of_element_located, (By.XPATH, '//body'))
        if el.get_attribute('class') == 'el-popup-parent--hidden':
            self.click_outside_close()
