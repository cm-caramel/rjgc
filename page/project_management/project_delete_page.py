import time
import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 项目删除弹窗
class ProjectDeletePage(BasePage):
    NAME = (By.XPATH, '//div[@class="projectdeletebox"]/div[2]/div[3]/div')
    TEACHER = (By.XPATH, '//div[@class="projectdeletebox"]/div[3]/div[3]/div')
    DIFFICULTY = (By.XPATH, '//div[@class="projectdeletebox"]/div[4]/div[3]/div')
    DELETE_BTN = (By.XPATH, '//div[@class="projectdeletebox"]/div[5]/div[2]/button')
    RETURN_BTN = (By.XPATH, '//div[@class="projectdeletebox"]/div[5]/div[4]/button')
    OUTSIDE_BLANK = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/div')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("获取项目名称")
    def get_project_name(self):
        return self.find_element(EC.visibility_of_element_located, self.NAME).text

    @allure.step("获取上传教师")
    def get_upload_teacher(self):
        return self.find_element(EC.visibility_of_element_located, self.TEACHER).text

    @allure.step("获取项目难度")
    def get_project_difficulty(self):
        return self.find_element(EC.visibility_of_element_located, self.DIFFICULTY).text

    @allure.step("点击删除按钮")
    def click_delete_btn(self):
        self.find_element(EC.visibility_of_element_located, self.DELETE_BTN).click()

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
