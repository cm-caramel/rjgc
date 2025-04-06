import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 导入学生页。班级详情页左下角导入用户按钮
class ImportStudentPage(BasePage):
    RETURN_BTN = (By.XPATH, '//div[@class="el-dialog__body"]/div/div/div[4]/button')
    RECORDS = (By.XPATH, '//div[@class="el-dialog__body"]//tbody//div[normalize-space(text())]/../..')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('点击返回按钮')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step('获取姓名')
    def get_name_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[1]/div')).text

    @allure.step('获取学号')
    def get_account_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[2]/div')).text

    @allure.step('获取行政班')
    def get_class_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[3]/div')).text

    @allure.step('获取添加按钮显示状态')
    def is_add_btn_visible_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        el = self.find_element_by_parent(pel, EC.presence_of_element_located, (By.XPATH, './td[4]/div'))
        return el.get_attribute("innerHTML").strip() != '' and el.get_attribute("innerHTML").strip() != '<!---->'

    @allure.step('点击添加')
    def click_add_btn_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[4]/div/button')).click()