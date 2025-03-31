import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from common.utils import conf
from page.base_page import BasePage
from page.home_page import HomePage


# 登录页面
class LoginPage(BasePage):
    SCHOOL_BTN = (By.XPATH, '//*[@id="app"]/div/section/main/div/div[2]/div/div/div[1]/div/div/div/div/span[2]/span/i')
    SCHOOL_LIST = (By.XPATH, '//*[@class="el-scrollbar__view el-select-dropdown__list"]/li')
    USER_INPUT = (By.XPATH, '//*[@id="app"]/div/section/main/div/div[2]/div/div/div[2]/div/div/input')
    PWD_INPUT = (By.XPATH, '//*[@id="app"]/div/section/main/div/div[2]/div/div/div[3]/div/div/input')
    LOGIN_BTN = (By.XPATH, '//*[@id="app"]/div/section/main/div/div[3]/button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('验证当前页面为登录页')
    def verify_page(self):
        return self.waiter.until(EC.url_to_be(conf['base_url']))

    @allure.step('验证没有发生页面跳转')
    def maintain_page(self):
        try:
            return not WebDriverWait(self.driver, conf['wait_time'] / 4).until(
                EC.url_changes(conf['base_url'])
            )
        except TimeoutException as e:
            return True
        except Exception as e:
            raise e

    def click_school_btn(self):
        self.find_element(EC.element_to_be_clickable, LoginPage.SCHOOL_BTN).click()

    @allure.step('选择学校')
    def select_school(self, school_name):
        self.click_school_btn()
        time.sleep(0.1)
        location = (By.XPATH, f'//span[text()="{school_name}"]')
        self.find_element(EC.visibility_of_element_located, location).click()

    @allure.step('输入用户名')
    def input_user(self, user):
        self.find_element(EC.presence_of_element_located, LoginPage.USER_INPUT).send_keys(user)

    @allure.step('输入密码')
    def input_pwd(self, pwd):
        self.find_element(EC.presence_of_element_located, LoginPage.PWD_INPUT).send_keys(pwd)

    @allure.step('点击登录按钮')
    def click_login_btn(self):
        self.find_element(EC.element_to_be_clickable, LoginPage.LOGIN_BTN).click()
        return HomePage(self.driver)

    def login(self, school='', user='', pwd=''):
        if school:
            self.select_school(school)
        if user:
            self.input_user(user)
        if pwd:
            self.input_pwd(pwd)
        return self.click_login_btn()
