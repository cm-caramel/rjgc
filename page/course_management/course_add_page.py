import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 新建课程页。课程管理点击新建课程
class CourseAddPage(BasePage):
    EXIT_EDIT_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[3]/span/button')
    CONFIRM_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/span/div[4]/div[2]/button')
    COURSE_NAME = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/span/div[1]/div[3]/div/div/input')
    COURSE_TIME = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/span/div[2]/div[3]/div/div/input')
    COURSE_INFO = (By.XPATH, '//*[@id="app"]//textarea')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('点击退出编辑')
    def click_exit_edit_btn(self):
        self.find_element(EC.element_to_be_clickable, self.EXIT_EDIT_BTN).click()

    @allure.step('点击确认')
    def click_confirm_btn(self):
        self.find_element(EC.element_to_be_clickable, self.CONFIRM_BTN).click()

    @allure.step('输入课程名称')
    def input_course_name(self, name):
        el = self.find_element(EC.visibility_of_element_located, self.COURSE_NAME)
        el.clear()
        el.send_keys(name)

    @allure.step('输入课程时间')
    def input_course_time(self, t):
        el = self.find_element(EC.visibility_of_element_located, self.COURSE_TIME)
        el.clear()
        el.send_keys(t)

    @allure.step('输入课程信息')
    def input_course_info(self, content):
        el = self.find_element(EC.visibility_of_element_located, self.COURSE_INFO)
        el.clear()
        el.send_keys(content)
