import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 添加作业页，作业管理点击左下角添加作业
class TaskAddPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
