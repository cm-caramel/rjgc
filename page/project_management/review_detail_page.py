import time
import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 项目审核-审核详情页
class ReviewDetailPage(BasePage):
    FROM_USER = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[2]/span[2]')
    REQUEST_KIND = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[4]/span[2]')
    STATUS = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[5]/span[2]')
    RETURN_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[6]/button')
    PROJECT_NAME = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[1]/div[3]//input')
    PROJECT_KIND = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[2]/div[3]//input')
    UPLOAD_TEACHER = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[3]/div[3]//input')
    PROJECT_INTRO = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[2]/div[5]/div/div['
                               '1]/div/div/p')
    CONFIRM_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[8]/div[2]/span/button')
    REJECT_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[8]/div[3]/span/button')
    CONFIRM_BTN_P = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[8]/div[2]')
    REJECT_BTN_P = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[8]/div[3]')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('获取来自用户')
    def get_from_user(self):
        return self.find_element(EC.visibility_of_element_located, self.FROM_USER).text

    @allure.step('获取请求类型')
    def get_request_kind(self):
        return self.find_element(EC.visibility_of_element_located, self.REQUEST_KIND).text

    @allure.step('获取请求状态')
    def get_status(self):
        return self.find_element(EC.visibility_of_element_located, self.STATUS).text

    @allure.step('获取项目名称')
    def get_project_name(self):
        return self.find_element(EC.visibility_of_element_located, self.PROJECT_NAME).get_attribute('value')

    @allure.step('获取项目类型')
    def get_project_kind(self):
        return self.find_element(EC.visibility_of_element_located, self.PROJECT_KIND).get_attribute('value')

    @allure.step('获取上传教师')
    def get_upload_teacher(self):
        return self.find_element(EC.visibility_of_element_located, self.UPLOAD_TEACHER).get_attribute('value')

    @allure.step('获取项目简介')
    def get_project_intro(self):
        return self.find_element(EC.visibility_of_element_located, self.PROJECT_INTRO).text

    @allure.step('点击确认按钮')
    def click_confirm_btn(self):
        self.find_element(EC.element_to_be_clickable, self.CONFIRM_BTN).click()

    @allure.step('点击拒绝按钮')
    def click_reject_btn(self):
        self.find_element(EC.element_to_be_clickable, self.REJECT_BTN).click()

    @allure.step('点击返回按钮')
    def click_return_btn(self):
        self.find_element(EC.element_to_be_clickable, self.RETURN_BTN).click()

    @allure.step('获取确认按钮的显示状态')
    def is_confirm_btn_visible(self):
        p = self.find_element(EC.presence_of_element_located, self.CONFIRM_BTN_P)
        return p.get_attribute("innerHTML").strip() != ''

    @allure.step('获取否决按钮的显示状态')
    def is_reject_btn_visible(self):
        p = self.find_element(EC.presence_of_element_located, self.REJECT_BTN_P)
        return p.get_attribute("innerHTML").strip() != ''
