import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


class UserImportPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
