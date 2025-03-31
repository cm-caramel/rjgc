from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 工具列表页
class ToolPage(BasePage):
    EDIT_MODE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div[1]/div[4]/span/button')
    PAGE_TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div[1]/div[1]/span')
    TOOL = '//span[contains(@class, "el-tree-node__label")]/span'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('验证当前页面为工具列表页')
    def verify_page(self):
        t = self.find_element(EC.visibility_of_element_located, self.PAGE_TITLE).text
        return self.waiter.until(EC.url_to_be(conf['base_url'] + 'tool')) and t == '工具列表'

    @allure.step('点击编辑模式')
    def click_edit_mode(self):
        self.find_element(EC.visibility_of_element_located, self.EDIT_MODE).click()
        from page.textbook_management.tool.tool_edit_mode_page import ToolEditModePage
        return ToolEditModePage(self.driver)

    @allure.step('点击工具')
    def click_tool_by_title(self, title):
        self.find_element(EC.visibility_of_element_located, (By.XPATH, f'{self.TOOL}[text()="{title}"]')).click()
        from page.textbook_management.tool.tool_detail_page import ToolDetailPage
        return ToolDetailPage(self.driver)

    @allure.step('点击工具')
    def click_tool_by_index(self, index):
        l = self.get_all_tool()
        arr = self.find_element(EC.visibility_of_all_elements_located, (By.XPATH, self.TOOL))
        arr[index].click()
        from page.textbook_management.tool.tool_detail_page import ToolDetailPage
        return ToolDetailPage(self.driver, l)

    @allure.step('获取所有工具')
    def get_all_tool(self):
        try:
            arr = self.find_element(EC.visibility_of_all_elements_located, (By.XPATH, self.TOOL))
            return [i.text for i in arr]
        except Exception as e:
            return []
