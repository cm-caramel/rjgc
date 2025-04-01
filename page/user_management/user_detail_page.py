import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


class UserDetailPage(BasePage):
    BASE_PATH = '//*[@id="app"]//div[@class="el-dialog__body"]/div'
    USER_NAME = (By.XPATH, f'{BASE_PATH}/form/div[1]//div[@class="el-form-item__content"]//input')
    USER_ACCOUNT = (By.XPATH, f'{BASE_PATH}/form/div[2]//div[@class="el-form-item__content"]//input')
    USER_SEX = (By.XPATH, f'{BASE_PATH}/form/div[3]//div[@class="el-form-item__content"]//input')
    SEX_POPUP_MALE = (By.XPATH, '//body/div[2]//div[@data-popper-placement="bottom-start" and '
                                '@aria-hidden="false"]//span[text()="男"]')
    SEX_POPUP_FEMALE = (By.XPATH, '//body/div[2]//div[@data-popper-placement="bottom-start" and '
                                  '@aria-hidden="false"]//span[text()="女"]')
    SCHOOL_NAME = (By.XPATH, f'{BASE_PATH}/form/div[4]//div[@class="el-form-item__content"]//input')
    USER_TEL = (By.XPATH, f'{BASE_PATH}/form/div[5]//div[@class="el-form-item__content"]//input')
    USER_EMAIL = (By.XPATH, f'{BASE_PATH}/form/div[6]//div[@class="el-form-item__content"]//input')
    CONFIRM_BTN = (By.XPATH, f'{BASE_PATH}/div/div[2]/button')
    RESET_PWD_BTN = (By.XPATH, f'{BASE_PATH}/div/div[3]/button')
    RETURN_BTN = (By.XPATH, f'{BASE_PATH}/div/div[4]/button')
    OUTSIDE_BLANK = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/div')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("获取姓名")
    def get_user_name(self):
        return self.find_element(EC.presence_of_element_located, self.USER_NAME).get_attribute('value')

    @allure.step("修改姓名")
    def input_user_name(self, name):
        el = self.find_element(EC.presence_of_element_located, self.USER_NAME)
        el.clear()
        el.send_keys(name)

    @allure.step("获取工号")
    def get_user_account(self):
        return self.find_element(EC.presence_of_element_located, self.USER_ACCOUNT).get_attribute('value')

    @allure.step("修改工号")
    def input_user_account(self, account):
        el = self.find_element(EC.presence_of_element_located, self.USER_ACCOUNT)
        el.clear()
        el.send_keys(account)

    @allure.step("获取性别")
    def get_user_sex(self):
        return self.find_element(EC.presence_of_element_located, self.USER_SEX).get_attribute('value')

    @allure.step("修改性别为男")
    def input_user_sex_male(self):
        self.find_element(EC.visibility_of_element_located, self.USER_SEX).click()
        self.find_element(EC.visibility_of_element_located, self.SEX_POPUP_MALE).click()

    @allure.step("修改性别为女")
    def input_user_sex_female(self):
        self.find_element(EC.visibility_of_element_located, self.USER_SEX).click()
        self.find_element(EC.visibility_of_element_located, self.SEX_POPUP_FEMALE).click()

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

    @allure.step('点击确认')
    def click_confirm_btn(self):
        self.find_element(EC.visibility_of_element_located, self.CONFIRM_BTN).click()

    @allure.step('点击重置密码')
    def click_reset_pwd_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RESET_PWD_BTN).click()

    @allure.step('点击返回')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step("点击空白处关闭弹窗")
    def click_outside_close(self):
        self.click_element_position(EC.presence_of_element_located, self.OUTSIDE_BLANK)

    def close_if_open(self):
        el = self.find_element(EC.presence_of_element_located, (By.XPATH, '//body'))
        if el.get_attribute('class') == 'el-popup-parent--hidden':
            self.click_outside_close()
