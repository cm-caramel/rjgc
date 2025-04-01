import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


class UserDeletePage(BasePage):
    NAME = (By.XPATH, '//div[@class="projectdeletebox"]/div[2]/div[3]/div')
    ACCOUNT = (By.XPATH, '//div[@class="projectdeletebox"]/div[3]/div[3]/div')
    KIND = (By.XPATH, '//div[@class="projectdeletebox"]/div[4]/div[3]/div')
    DEL_BTN = (By.XPATH, '//div[@class="projectdeletebox"]/div[5]/div[2]/button')
    RETURN_BTN = (By.XPATH, '//div[@class="projectdeletebox"]/div[5]/div[4]/button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('获取姓名')
    def get_name(self):
        return self.find_element(EC.visibility_of_element_located, self.NAME).text

    @allure.step('获取工号')
    def get_account(self):
        return self.find_element(EC.visibility_of_element_located, self.ACCOUNT).text

    @allure.step('获取类型')
    def get_kind(self):
        return self.find_element(EC.visibility_of_element_located, self.KIND).text

    @allure.step('点击删除')
    def click_delete_btn(self):
        self.find_element(EC.visibility_of_element_located, self.DEL_BTN).click()

    @allure.step('点击返回')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()
