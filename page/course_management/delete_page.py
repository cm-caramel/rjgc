import time

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 课程删除弹窗。课程详情页点击右上角删除。
# 班级删除弹窗-共用。班级列表点击班级右侧的删除。
# 学生删除弹窗-共用。班级详情点击删除一个学生。
class DeletePage(BasePage):
    TITLE =(By.XPATH, '//div[@class="el-dialog__body"]/div/div/div[3]/span')
    INFO_1 = (By.XPATH, '//div[@class="el-dialog__body"]/div/div[2]/div[3]/div')
    INFO_2 = (By.XPATH, '//div[@class="el-dialog__body"]/div/div[3]/div[3]/div')
    DELETE_BTN = (By.XPATH, '//div[@class="el-dialog__body"]/div/div[4]/div[2]/button')
    RETURN_BTN = (By.XPATH, '//div[@class="el-dialog__body"]/div/div[4]/div[4]/button')
    OUTSIDE_BLANK = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/div')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('获取课程名称')
    def get_course_name(self):
        return self.find_element(EC.visibility_of_element_located, self.INFO_1).text

    @allure.step('获取课程时间')
    def get_course_time(self):
        return self.find_element(EC.visibility_of_element_located, self.INFO_2).text

    @allure.step('获取所属课程')
    def get_class_course_name(self):
        return self.find_element(EC.visibility_of_element_located, self.INFO_1).text

    @allure.step('获取班级名称')
    def get_class_name(self):
        return self.find_element(EC.visibility_of_element_located, self.INFO_2).text

    @allure.step('点击删除按钮')
    def click_delete_btn(self):
        self.find_element(EC.element_to_be_clickable, self.DELETE_BTN).click()

    @allure.step('点击返回按钮')
    def click_return_btn(self):
        self.find_element(EC.element_to_be_clickable, self.RETURN_BTN).click()

    def click_outside_close(self):
        self.click_element_position(EC.presence_of_element_located, self.OUTSIDE_BLANK)

    def close_if_open(self):
        el = self.find_element(EC.presence_of_element_located, (By.XPATH, '//body'))
        if el.get_attribute('class') == 'el-popup-parent--hidden':
            self.click_outside_close()
