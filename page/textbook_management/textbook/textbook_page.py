from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage
from common.utils import *


# 教材章节页
class TextbookPage(BasePage):
    PARENT_TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[1]/span/button/span/span')
    TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[1]/div[1]/span')
    EDIT_MODE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[1]/div[4]/span/button')
    TEXTBOOK = '//span[contains(@class, "el-tree-node__label")]/span'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.home.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('验证当前页面为教材章节页')
    def verify_page(self):
        return self.waiter.until(EC.url_to_be(conf['base_url'] + 'text'))

    @allure.step('点击编辑模式')
    def click_edit_mode(self):
        self.find_element(EC.visibility_of_element_located, self.EDIT_MODE).click()
        from page.textbook_management.textbook.textbook_edit_mode_page import TextbookEditModePage
        return TextbookEditModePage(self.driver)

    def get_textbook_path(self, label, title):
        return f'{self.TEXTBOOK}[text()="{label} {title}"]'

    @allure.step('点击一个章节')
    def click_textbook(self, label, title):
        arr = self.get_all_textbook()
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.get_textbook_path(label, title))).click()
        from page.textbook_management.textbook.textbook_detail_page import TextbookDetailPage
        return TextbookDetailPage(self.driver, arr)

    @allure.step('搜索教材')
    def search_textbook(self, text):
        self.top_side_bar.input_search(text)
        self.top_side_bar.click_search()

    @allure.step('获取所有教材章节')
    def get_all_textbook(self):
        try:
            arr = self.find_element(EC.visibility_of_all_elements_located, (By.XPATH, self.TEXTBOOK))
            return [i.text for i in arr]
        except Exception as e:
            return []

