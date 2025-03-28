import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 教材章节页-编辑模式（学生无权限，不显示）
class TextbookEditModePage(BasePage):
    PARENT_TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[1]/span/button/span/span')
    TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[1]/div[1]/span')
    TEXTBOOK_ADD = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[1]/div[2]/span/button')
    EXIT_EDIT_MODE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[1]/div[4]/span/button')
    EDIT_BTN = '//span[contains(@class, "el-tree-node__label")]/span[text()="{}"]/../div//button[1]'
    ADD_BTN = '//span[contains(@class, "el-tree-node__label")]/span[text()="{}"]/../div//button[2]'
    DELETE_BTN = '//span[contains(@class, "el-tree-node__label")]/span[text()="{}"]/../div//button[3]'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('验证当前页面为教材章节页')
    def verify_page(self):
        t1 = self.find_element(EC.visibility_of_element_located, self.PARENT_TITLE).text
        t2 = self.find_element(EC.visibility_of_element_located, self.TITLE).text
        return t1 == '教材管理' and t2 == '教材章节'

    @allure.step('点击退出编辑')
    def click_exit_edit_mode(self):
        self.find_element(EC.visibility_of_element_located, self.EXIT_EDIT_MODE).click()
        from page.textbook_management.textbook.textbook_page import TextbookPage
        return TextbookPage(self.driver)

    @allure.step('点击添加新书')
    def click_textbook_add(self):
        self.find_element(EC.visibility_of_element_located, self.TEXTBOOK_ADD).click()
        from page.textbook_management.textbook.textbook_edit_page import TextbookEditPage
        return TextbookEditPage(self.driver)

    @allure.step('点击编辑章节按钮')
    def click_edit_btn(self, label, title):
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.EDIT_BTN.format(f'{label} {title}'))).click()
        from page.textbook_management.textbook.textbook_edit_page import TextbookEditPage
        return TextbookEditPage(self.driver)

    @allure.step('点击添加章节按钮')
    def click_add_btn(self, label, title):
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.ADD_BTN.format(f'{label} {title}'))).click()
        from page.textbook_management.textbook.textbook_edit_page import TextbookEditPage
        return TextbookEditPage(self.driver)

    @allure.step('点击删除章节按钮')
    def click_delete_btn(self, label, title):
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.DELETE_BTN.format(f'{label} {title}'))).click()
        from page.textbook_management.textbook.textbook_delete_page import TextbookDeletePage
        return TextbookDeletePage(self.driver)
