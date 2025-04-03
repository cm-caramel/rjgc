from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 项目详情共用此页面
class ProjectDetailPage(BasePage):
    PROJECT_NAME = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[1]/div[3]/div')
    PROJECT_KIND = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[2]/div[3]/div')
    TEACHER = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[3]/div[3]/div')
    UPLOAD_TIME = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[4]/div[3]/div')
    EDIT_TIME = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[8]/div[3]/div')
    BTN1_LINK = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[5]/div[4]/a')
    BTN2_LINK = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[6]/div[4]/a')
    BTN3_LINK = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[7]/div[4]/a')
    PROJECT_INTRO = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[2]/div[4]/div/div['
                               '1]/div/div')
    RETURN_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[5]/button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('获取项目名称')
    def get_project_name(self):
        return self.find_element(EC.visibility_of_element_located, self.PROJECT_NAME).text

    @allure.step('获取项目类型')
    def get_project_kind(self):
        return self.find_element(EC.visibility_of_element_located, self.PROJECT_KIND).text

    @allure.step('获取上传教师')
    def get_teacher(self):
        return self.find_element(EC.visibility_of_element_located, self.TEACHER).text

    @allure.step('获取上传时间')
    def get_upload_time(self):
        return self.find_element(EC.visibility_of_element_located, self.UPLOAD_TIME).text

    @allure.step('获取最后修改时间')
    def get_edit_time(self):
        return self.find_element(EC.visibility_of_element_located, self.EDIT_TIME).text

    @allure.step('获取项目简介')
    def get_project_intro(self):
        return self.find_element(EC.visibility_of_element_located, self.PROJECT_INTRO).text

    @allure.step('点击返回按钮')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step('获取项目源码链接')
    def get_source_code_link(self):
        link = self.find_element(EC.presence_of_element_located, self.BTN1_LINK).get_attribute('href')
        return link.split(f"{conf['base_url']}project/")[1]

    @allure.step('获取项目文档链接')
    def get_document_link(self):
        link = self.find_element(EC.presence_of_element_located, self.BTN2_LINK).get_attribute('href')
        return link.split(f"{conf['base_url']}project/")[1]

    @allure.step('获取评分细则链接')
    def get_score_link(self):
        link = self.find_element(EC.presence_of_element_located, self.BTN3_LINK).get_attribute('href')
        return link.split(f"{conf['base_url']}project/")[1]
