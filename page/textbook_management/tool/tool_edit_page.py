import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 工具编辑页。入口：工具列表编辑模式，点击编辑按钮。
class ToolEditPage(BasePage):
    TOOL_KIND = (By.XPATH, '//*[@id="app"]//div[@class="EditBox"]//main/div[1]//input')
    OPT_KIND = (By.XPATH, '//*[@id="app"]//div[@class="EditBox"]//main/div[1]/div[5]/span')
    ADD_BTN = (By.XPATH, '//*[@id="app"]//div[@class="EditBox"]//main/div[1]/div[6]/span/button')
    RETURN_BTN = (By.XPATH, '//*[@id="app"]//div[@class="EditBox"]//main/div[1]/div[7]/button')
    CONFIRM_BTN = (By.XPATH, '//*[@id="app"]//div[@class="EditBox"]//main/div[1]/div[8]/button')
    CUR_PAGE = '//*[@id="app"]//div[@class="EditBox"]//div[contains(@class,"is-active")]'
    SWITCH_BTN = (By.XPATH, '//*[@id="app"]//div[@class="EditBox"]//main/div[2]/ul/li')
    TOOL_NAME = (By.XPATH, CUR_PAGE + '/div[2]//input[@placeholder="工具名称"]')
    TOOL_LINK = (By.XPATH, CUR_PAGE + '/div[2]//input[@placeholder="工具下载链接"]')
    CLOSE_BTN = (By.XPATH, CUR_PAGE + '/div[2]//button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('获取工具类型')
    def get_tool_kind(self):
        return self.find_element(EC.visibility_of_element_located, self.TOOL_KIND).get_attribute('value')

    @allure.step('修改工具类型')
    def input_tool_kind(self, kind):
        el = self.find_element(EC.visibility_of_element_located, self.TOOL_KIND)
        el.clear()
        el.send_keys(kind)

    @allure.step('获取操作类型')
    def get_opt_kind(self):
        return self.find_element(EC.visibility_of_element_located, self.OPT_KIND).text

    @allure.step('点击新建按钮')
    def click_add_btn(self):
        self.find_element(EC.visibility_of_element_located, self.ADD_BTN).click()

    @allure.step('点击返回按钮')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step('点击确认按钮')
    def click_confirm_btn(self):
        self.find_element(EC.visibility_of_element_located, self.CONFIRM_BTN).click()

    @allure.step('获取工具数量')
    def get_tool_cnt(self):
        return len(self.find_element(EC.visibility_of_all_elements_located, self.SWITCH_BTN))

    @allure.step('切换工具页')
    def switch_tool_page(self, index):
        el = self.find_element(EC.visibility_of_all_elements_located, self.SWITCH_BTN)[index]
        ActionChains(self.driver).move_to_element(el).perform()

    @allure.step('输入工具名称')
    def input_tool_name(self, name):
        el = self.find_element(EC.visibility_of_element_located, self.TOOL_NAME)
        el.clear()
        el.send_keys(name)

    @allure.step('输入工具链接')
    def input_tool_link(self, link):
        el = self.find_element(EC.visibility_of_element_located, self.TOOL_LINK)
        el.clear()
        el.send_keys(link)

    @allure.step('点击工具右上角删除按钮')
    def click_close_btn(self):
        self.find_element(EC.visibility_of_element_located, self.CLOSE_BTN).click()


