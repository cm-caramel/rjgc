import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 首页上方菜单-个人信息弹窗
class PersonalInfoPage(BasePage):
    BASE_PATH = '//*[@id="app"]//div[@class="el-dialog__body"]/div'
    USER_NAME = (By.XPATH, f'{BASE_PATH}/form/div[1]//div[@class="el-form-item__content"]//input')
    USER_ACCOUNT = (By.XPATH, f'{BASE_PATH}/form/div[2]//div[@class="el-form-item__content"]//input')
    USER_SEX = (By.XPATH, f'{BASE_PATH}/form/div[3]//div[@class="el-form-item__content"]//input')
    SCHOOL_NAME = (By.XPATH, f'{BASE_PATH}/form/div[4]//div[@class="el-form-item__content"]//input')
    USER_TEL = (By.XPATH, f'{BASE_PATH}/form/div[5]//div[@class="el-form-item__content"]//input')
    USER_EMAIL = (By.XPATH, f'{BASE_PATH}/form/div[6]//div[@class="el-form-item__content"]//input')
    ROLE_NAME = (By.XPATH, f'{BASE_PATH}/form/div[7]//div[@class="el-form-item__content"]//input')
    SAVE_BTN = (By.XPATH, f'{BASE_PATH}/button')
    OUTSIDE_BLANK = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/div')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("获取用户名")
    def get_user_name(self):
        return self.find_element(EC.presence_of_element_located, self.USER_NAME).get_attribute('value')

    @allure.step("获取工号")
    def get_user_account(self):
        return self.find_element(EC.presence_of_element_located, self.USER_ACCOUNT).get_attribute('value')

    @allure.step("获取性别")
    def get_user_sex(self):
        return self.find_element(EC.presence_of_element_located, self.USER_SEX).get_attribute('value')

    @allure.step("修改性别")
    def input_user_sex(self, sex):
        el = self.find_element(EC.presence_of_element_located, self.USER_SEX)
        el.clear()
        el.send_keys(sex)

    @allure.step("获取学校")
    def get_school_name(self):
        return self.find_element(EC.presence_of_element_located, self.SCHOOL_NAME).get_attribute('value')

    @allure.step("获取手机号")
    def get_user_tel(self):
        return self.find_element(EC.presence_of_element_located, self.USER_TEL).get_attribute('value')

    @allure.step("修改手机号")
    def input_user_tel(self, tel):
        el = self.find_element(EC.presence_of_element_located, self.USER_TEL)
        el.clear()
        el.send_keys(tel)

    @allure.step("获取邮箱")
    def get_user_email(self):
        return self.find_element(EC.presence_of_element_located, self.USER_EMAIL).get_attribute('value')

    @allure.step("修改邮箱")
    def input_user_email(self, email):
        el = self.find_element(EC.presence_of_element_located, self.USER_EMAIL)
        el.clear()
        el.send_keys(email)

    @allure.step("获取用户类型")
    def get_role_name(self):
        return self.find_element(EC.presence_of_element_located, self.ROLE_NAME).get_attribute('value')

    @allure.step("点击保存按钮")
    def click_save_btn(self):
        self.find_element(EC.element_to_be_clickable, self.SAVE_BTN).click()

    @allure.step("点击空白处关闭弹窗")
    def click_outside_close(self):
        self.click_element_position(EC.presence_of_element_located, self.OUTSIDE_BLANK)

    def close_if_open(self):
        el = self.find_element(EC.presence_of_element_located, (By.XPATH, '//body'))
        if el.get_attribute('class') == 'el-popup-parent--hidden':
            self.click_outside_close()

