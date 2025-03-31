import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 工具种类新增弹窗。入口：工具列表页编辑模式，点击新增分类
class ToolAddPage(BasePage):
    OUTSIDE_BLANK = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/div')
    KIND_INPUT = (By.XPATH, '//*[@id="app"]//div[@class="tooladdbox"]//input')
    CONFIRM_BTN = (By.XPATH, '//*[@id="app"]//div[@class="tooladdbox"]/div[3]/div[2]/button')
    RETURN_BTN = (By.XPATH, '//*[@id="app"]//div[@class="tooladdbox"]/div[3]/div[4]/button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('输入工具种类名称')
    def input_kind_name(self, name):
        el = self.find_element(EC.visibility_of_element_located, self.KIND_INPUT)
        el.clear()
        el.send_keys(name)

    @allure.step('点击确认')
    def click_confirm_btn(self):
        self.find_element(EC.visibility_of_element_located, self.CONFIRM_BTN).click()

    @allure.step('点击返回')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step('点击外部空白关闭弹窗')
    def click_outside_close(self):
        self.click_element_position(EC.presence_of_element_located, self.OUTSIDE_BLANK)

    def close_if_open(self):
        el = self.find_element(EC.presence_of_element_located, (By.XPATH, '//body'))
        if el.get_attribute('class') == 'el-popup-parent--hidden':
            self.click_outside_close()
