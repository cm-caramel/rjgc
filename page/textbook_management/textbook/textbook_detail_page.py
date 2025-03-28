from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 教材章节详情页。入口：教材章节页，点击一个章节
class TextbookDetailPage(BasePage):
    RETURN_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div/div[1]/div[2]/button')
    TEXTBOOK_TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div/div[1]/div[1]')
    LOAD_FILE_NAME = '//span[@class="el-upload-list__item-file-name" and text()="{}"]'
    LOAD_FILE_NAMES = (By.XPATH, '//span[@class="el-upload-list__item-file-name"]')
    SELECT_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div/section/main/div[2]/div[1]/div/button')
    LOAD_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div/section/main/div[2]/div[2]/button')
    PRE_BTN_PARENT = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div/div[4]/div[2]')
    NEXT_BTN_PARENT = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div/div[4]/div[3]')
    PRE_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div/div[4]/div[2]/span/button')
    NEXT_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div/div[4]/div[3]/span/button')
    CATALOG = (By.XPATH, '//span[@class="el-tree-node__label"]')

    def __init__(self, driver, title_lists):
        super().__init__(driver)
        self.driver = driver
        self.title_lists = title_lists

    @allure.step('验证当前页面为教材章节详情页')
    def verify_page(self):
        return self.waiter.until(EC.url_contains(conf['base_url'] + 'textbook?id='))

    @allure.step('点击返回章节列表')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step('获取教材章节标题')
    def get_textbook_title(self):
        t = self.find_element(EC.visibility_of_element_located, self.TEXTBOOK_TITLE).text
        return t.replace('\u2003', ' ')

    @allure.step('点击选择文件')
    def click_select_btn(self):
        self.find_element(EC.visibility_of_element_located, self.SELECT_BTN).click()

    @allure.step('点击上传文件')
    def click_load_btn(self):
        self.find_element(EC.visibility_of_element_located, self.LOAD_BTN).click()

    @allure.step('获取所有上传的文件名')
    def get_load_files(self):
        try:
            arr = self.find_element(EC.visibility_of_all_elements_located, self.LOAD_FILE_NAMES)
            return [i.text for i in arr]
        except Exception as e:
            return []

    @allure.step('获取上一节按钮的显示状态')
    def is_pre_btn_visible(self):
        p = self.find_element(EC.presence_of_element_located, self.PRE_BTN_PARENT)
        return p.get_attribute("innerHTML").strip() != ''

    @allure.step('获取下一节按钮的显示状态')
    def is_next_btn_visible(self):
        p = self.find_element(EC.presence_of_element_located, self.NEXT_BTN_PARENT)
        return p.get_attribute("innerHTML").strip() != ''

    @allure.step('点击上一节')
    def click_pre_btn(self):
        self.find_element(EC.visibility_of_element_located, self.PRE_BTN).click()

    @allure.step('点击下一节')
    def click_next_btn(self):
        self.find_element(EC.visibility_of_element_located, self.NEXT_BTN).click()

    @allure.step('点击右侧目录中的章节')
    def click_catalog_by_index(self, index):
        if 0 <= index < len(self.title_lists):
            self.find_element(EC.visibility_of_all_elements_located, self.CATALOG)[index].click()
        else:
            raise Exception('num不合法。')

    def click_catalog_by_title(self, label, title):
        name = f'{label} {title}'
        if name in self.title_lists:
            self.click_catalog_by_index(self.title_lists.index(name))

    def get_current_index(self):
        return self.title_lists.index(self.get_textbook_title())
