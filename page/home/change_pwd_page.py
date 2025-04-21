import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


class ChangePwdPage(BasePage):
    OLD_PWD = (By.XPATH, '//*[@id="app"]//div[@class="el-dialog__body"]/div/div/div[1]/div[2]//input')
    NEW_PWD = (By.XPATH, '//*[@id="app"]//div[@class="el-dialog__body"]/div/div/div[2]/div[2]//input')
    CONFIRM_PWD = (By.XPATH, '//*[@id="app"]//div[@class="el-dialog__body"]/div/div/div[3]/div[2]//input')
    CONFIRM_BTN = (By.XPATH, '//*[@id="app"]//div[@class="el-dialog__body"]/div/div/div[4]/div[2]/button')
    CANCEL_BTN = (By.XPATH, '//*[@id="app"]//div[@class="el-dialog__body"]/div/div/div[4]/div[4]/button')
    OUTSIDE_BLANK = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/div')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("输入旧密码")
    def input_old_pwd(self, pwd):
        el = self.find_element(EC.presence_of_element_located, self.OLD_PWD)
        el.clear()
        el.send_keys(pwd)

    @allure.step("输入新密码")
    def input_new_pwd(self, pwd):
        el = self.find_element(EC.presence_of_element_located, self.NEW_PWD)
        el.clear()
        el.send_keys(pwd)

    @allure.step("输入确认密码")
    def input_confirm_pwd(self, pwd):
        el = self.find_element(EC.presence_of_element_located, self.CONFIRM_PWD)
        el.clear()
        el.send_keys(pwd)

    @allure.step("点击确认按钮")
    def click_confirm_btn(self):
        self.find_element(EC.presence_of_element_located, self.CONFIRM_BTN).click()

    @allure.step("点击取消按钮")
    def click_cancel_btn(self):
        self.find_element(EC.presence_of_element_located, self.CANCEL_BTN).click()

    @allure.step("点击空白处关闭弹窗")
    def click_outside_close(self):
        self.click_element_position(EC.presence_of_element_located, self.OUTSIDE_BLANK)

    def close_if_open(self):
        el = self.find_element(EC.presence_of_element_located, (By.XPATH, '//body'))
        if el.get_attribute('class') == 'el-popup-parent--hidden':
            self.click_outside_close()

