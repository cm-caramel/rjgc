import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 教材编辑页。入口：教材编辑模式，点击添加新书、章节编辑或添加按钮。
class TextbookEditPage(BasePage):
    BASE_PATH = '//div[@class="EditBox"]'
    TEXTBOOK_TITLE = (By.XPATH, BASE_PATH + '//input')
    KIND = (By.XPATH, BASE_PATH + '/section/main/div[1]/div[5]/span')
    RETURN_BTN = (By.XPATH, BASE_PATH + '/section/main/div[1]/div[6]/button')
    CONFIRM_BTN = (By.XPATH, BASE_PATH + '/section/main/div[1]/div[7]/button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('获取节名')
    def get_textbook_title(self):
        return self.find_element(EC.presence_of_element_located, self.TEXTBOOK_TITLE).get_attribute('value')

    @allure.step('输入节名')
    def input_textbook_title(self, title):
        el = self.find_element(EC.presence_of_element_located, self.TEXTBOOK_TITLE)
        el.clear()
        el.send_keys(title)

    @allure.step('获取类型')
    def get_kind(self):
        return self.find_element(EC.presence_of_element_located, self.KIND).text

    @allure.step('点击返回')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step('点击确定')
    def click_confirm_btn(self):
        self.find_element(EC.visibility_of_element_located, self.CONFIRM_BTN).click()

    @allure.step('获取章节内容')
    def get_content(self):
        self.find_element(EC.presence_of_element_located, (By.XPATH, self.BASE_PATH + '//iframe'))
        time.sleep(2)
        return self.driver.execute_script("return tinymce.activeEditor.getContent();")

    @allure.step('输入章节内容')
    def input_content(self, content):
        self.find_element(EC.frame_to_be_available_and_switch_to_it,
                          (By.XPATH, self.BASE_PATH + '//iframe'))
        time.sleep(2)
        el = self.find_element(EC.presence_of_element_located, (By.ID, 'tinymce'))
        el.clear()
        el.send_keys(content)
        self.driver.switch_to.default_content()

    @allure.step('追加章节内容')
    def append_content(self, content):
        self.find_element(EC.frame_to_be_available_and_switch_to_it,
                          (By.XPATH, self.BASE_PATH + '//iframe'))
        time.sleep(2)
        self.find_element(EC.visibility_of_element_located, (By.ID, 'tinymce')).send_keys(content)
        self.driver.switch_to.default_content()
        # self.driver.execute_script(f"tinymce.activeEditor.insertContent('<p>{content}</p>')")
