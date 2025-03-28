import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 教材删除二次确认弹窗。入口：教材编辑模式，点击删除按钮
class TextbookDeletePage(BasePage):
    BASE_PATH = '//div[@class="textbookdeletebox"]'
    TEXTBOOK_TITLE = (By.XPATH, BASE_PATH + '/div[2]/div[3]/div')
    TEXTBOOK_LABEL = (By.XPATH, BASE_PATH + '/div[3]/div[3]/div')
    DELETE_BTN = (By.XPATH, BASE_PATH + '/div[4]/div[2]/button')
    RETURN_BTN = (By.XPATH, BASE_PATH + '/div[4]/div[4]/button')
    OUTSIDE_BLANK = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/div')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("获取章节名称")
    def get_textbook_title(self):
        return self.find_element(EC.visibility_of_element_located, self.TEXTBOOK_TITLE).text

    @allure.step("获取章节标签")
    def get_textbook_label(self):
        return self.find_element(EC.visibility_of_element_located, self.TEXTBOOK_LABEL).text

    @allure.step("点击删除按钮")
    def click_delete_btn(self):
        self.find_element(EC.visibility_of_element_located, self.DELETE_BTN).click()

    @allure.step("点击返回按钮")
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step("点击空白处关闭弹窗")
    def click_outside_close(self):
        self.click_element_position(EC.presence_of_element_located, self.OUTSIDE_BLANK)

    def close_if_open(self):
        el = self.find_element(EC.presence_of_element_located, (By.XPATH, '//body'))
        if el.get_attribute('class') == 'el-popup-parent--hidden':
            self.click_outside_close()
