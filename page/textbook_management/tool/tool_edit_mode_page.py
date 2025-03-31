import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 工具列表页-编辑模式
class ToolEditModePage(BasePage):
    EXIT_EDIT_MODE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div[1]/div[4]/span/button')
    ADD_KIND = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div[1]/div[2]/span/button')
    EDIT_BTN = '//span[contains(@class, "el-tree-node__label")]/span[text()="{}"]/../div//button[1]'
    DELETE_BTN = '//span[contains(@class, "el-tree-node__label")]/span[text()="{}"]/../div//button[2]'
    EDIT_BTNS = (By.XPATH, '//span[contains(@class, "el-tree-node__label")]/div/div[2]/button[1]')
    DELETE_BTNS = (By.XPATH, '//span[contains(@class, "el-tree-node__label")]/div/div[2]/button[2]')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('点击退出编辑')
    def click_exit_edit_mode(self):
        self.find_element(EC.visibility_of_element_located, self.EXIT_EDIT_MODE).click()
        from page.textbook_management.tool.tool_page import ToolPage
        return ToolPage(self.driver)

    @allure.step('点击新增分类')
    def click_add_kind(self):
        self.find_element(EC.visibility_of_element_located, self.ADD_KIND).click()
        from page.textbook_management.tool.tool_add_page import ToolAddPage
        return ToolAddPage(self.driver)

    @allure.step('点击编辑按钮')
    def click_edit_btn_by_title(self, title):
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.EDIT_BTN.format(title))).click()
        from page.textbook_management.tool.tool_edit_page import ToolEditPage
        return ToolEditPage(self.driver)

    @allure.step('点击删除按钮')
    def click_delete_btn_by_title(self, title):
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.DELETE_BTN.format(title))).click()
        from page.textbook_management.tool.tool_delete_page import ToolDeletePage
        return ToolDeletePage(self.driver)

    @allure.step('点击编辑按钮')
    def click_edit_btn_by_index(self, index):
        self.find_element(EC.visibility_of_all_elements_located, self.EDIT_BTNS)[index].click()
        from page.textbook_management.tool.tool_edit_page import ToolEditPage
        return ToolEditPage(self.driver)

    @allure.step('点击删除按钮')
    def click_delete_btn_by_index(self, index):
        self.find_element(EC.visibility_of_all_elements_located, self.DELETE_BTNS)[index].click()
        from page.textbook_management.tool.tool_delete_page import ToolDeletePage
        return ToolDeletePage(self.driver)

