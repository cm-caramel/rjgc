import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 项目上传功能共用此页面
class ProjectUploadPage(BasePage):
    RETURN_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[5]/button')
    CONFIRM_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[7]/div[2]/button')
    PROJECT_NAME = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[1]/div[3]/div/div/input')
    PROJECT_KIND = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[2]/div[3]/div/div/input')
    EASY_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[3]/div[3]/div/label[1]')
    MID_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[3]/div[3]/div/label[2]')
    DIF_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div[3]/div[3]/div/label[3]')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('点击返回')
    def click_return_btn(self):
        self.find_element(EC.element_to_be_clickable, self.RETURN_BTN).click()

    @allure.step('点击确认')
    def click_confirm_btn(self):
        self.find_element(EC.element_to_be_clickable, self.CONFIRM_BTN).click()

    @allure.step('输入项目名称')
    def input_project_name(self, name):
        el = self.find_element(EC.visibility_of_element_located, self.PROJECT_NAME)
        el.clear()
        el.send_keys(name)

    @allure.step('获取项目类型')
    def get_project_kind(self):
        return self.find_element(EC.visibility_of_element_located, self.PROJECT_KIND).get_attribute('value')

    @allure.step('选择简单')
    def click_easy_btn(self):
        self.find_element(EC.visibility_of_element_located, self.EASY_BTN).click()

    @allure.step('选择中等')
    def click_mid_btn(self):
        self.find_element(EC.visibility_of_element_located, self.MID_BTN).click()

    @allure.step('选择困难')
    def click_difficult_btn(self):
        self.find_element(EC.visibility_of_element_located, self.DIF_BTN).click()

    @allure.step('输入项目简介')
    def input_project_intro(self, content):
        self.find_element(EC.frame_to_be_available_and_switch_to_it,
                          (By.XPATH, '//div[@class="projinfobox"]//iframe'))
        time.sleep(2)
        el = self.find_element(EC.presence_of_element_located, (By.ID, 'tinymce'))
        el.clear()
        el.send_keys(content)
        self.driver.switch_to.default_content()


