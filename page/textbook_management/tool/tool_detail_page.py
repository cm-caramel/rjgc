import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 工具详情页。入口：工具列表页点击一个工具。
class ToolDetailPage(BasePage):
    TOOL_TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div[1]/div[1]/span')
    RETURN_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/main/div/div[1]/div[2]/button')
    CUR_TOOL_PAGE = (By.XPATH, '//*[@id="app"]//div[@class="toolViewMainBox"]//div[contains(@class,"is-active")]')
    TOOL_SWITCH_BTN = (By.XPATH, '//*[@id="app"]//div[@class="toolViewMainBox"]//ul/li')
    TOOL_NAME = (By.XPATH, '//*[@id="app"]//div[@class="toolViewMainBox"]//div[contains(@class,"is-active")]//span['
                           '@class="toolName"]')
    TOOL_LINK = (By.XPATH, '//*[@id="app"]//div[@class="toolViewMainBox"]//div[contains(@class,"is-active")]//span['
                           '@class="el-link__inner"]')
    DISCUSS_SORT_BTN = (By.XPATH, '//*[@id="app"]//div[@class="discussBox"]/div[1]/div[2]/button')
    DISCUSS_ADD_BTN = (By.XPATH, '//*[@id="app"]//div[@class="discussBox"]/div[1]/div[3]/button')
    NEW_DISCUSS_PUBLISH_BTN = (By.XPATH, '//*[@id="app"]//div[@class="newDiscussBox"]/div[1]/div[2]/button')
    NEW_DISCUSS_CANCEL_BTN = (By.XPATH, '//*[@id="app"]//div[@class="newDiscussBox"]/div[1]/div[3]/button')
    NEW_DISCUSS_INPUT = (By.XPATH, '//*[@id="app"]//div[@class="newDiscussBox"]/div[2]/textarea')
    ALL_DISCUSS = (By.XPATH, '//*[@id="app"]//div[@class="discussBox"]//div[@class="el-scrollbar__view"]/div')
    DISCUSS_USER = (By.XPATH, './div[1]/span')
    DISCUSS_CONTENT = (By.XPATH, './div[2]/span')
    DISCUSS_LIKE_BTN = (By.XPATH, './div[3]/div[2]/button')
    DISCUSS_LIKE_CNT = (By.XPATH, './div[3]/div[2]/span')
    DISCUSS_DEL_BTN = (By.XPATH, './div[3]/div[3]/div/button')
    DISCUSS_DEL_BTN_P = (By.XPATH, './div[3]/div[3]')
    ALL_CATALOG = (By.XPATH, '//span[@class="el-tree-node__label"]')
    CATALOG = '//span[@class="el-tree-node__label" and text()="{}"]'

    def __init__(self, driver, title_lists):
        super().__init__(driver)
        self.driver = driver
        self.title_lists = title_lists

    @allure.step('获取工具标题')
    def get_tool_title(self):
        t = self.find_element(EC.visibility_of_element_located, self.TOOL_TITLE).text
        return t.replace('\u2003', '')

    @allure.step('获取当前工具名')
    def get_tool_name(self):
        return self.find_element(EC.visibility_of_element_located, self.TOOL_NAME).text

    @allure.step('获取当前工具链接')
    def get_tool_link(self):
        return self.find_element(EC.visibility_of_element_located, self.TOOL_LINK).text

    @allure.step('点击返回按钮')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step('点击当前工具链接')
    def click_tool_link(self):
        self.find_element(EC.visibility_of_element_located, self.TOOL_LINK).click()

    @allure.step('切换工具')
    def switch_tool(self, index):
        arr = self.find_element(EC.visibility_of_element_located, self.TOOL_SWITCH_BTN)
        a = ActionChains(self.driver)
        a.move_to_element(arr[index]).perform()

    @allure.step('点击右侧目录')
    def click_catalog_by_index(self, index):
        self.find_element(EC.visibility_of_all_elements_located, self.ALL_CATALOG)[index].click()

    @allure.step('点击右侧目录')
    def click_catalog_by_title(self, title):
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.CATALOG.format(title))).click()

    @allure.step('点击评论区新建按钮')
    def click_discuss_add_btn(self):
        self.find_element(EC.visibility_of_element_located, self.DISCUSS_ADD_BTN).click()

    @allure.step('点击评论区发表按钮')
    def click_discuss_publish_btn(self):
        self.find_element(EC.visibility_of_element_located, self.NEW_DISCUSS_PUBLISH_BTN).click()

    @allure.step('点击评论区取消按钮')
    def click_discuss_cancel_btn(self):
        self.find_element(EC.visibility_of_element_located, self.NEW_DISCUSS_CANCEL_BTN).click()

    @allure.step('输入评论内容')
    def input_discuss_content(self, content):
        el = self.find_element(EC.visibility_of_element_located, self.NEW_DISCUSS_INPUT)
        el.clear()
        el.send_keys(content)

    @allure.step('获取所有评论信息')
    def get_all_discuss_info(self):
        arr = self.find_element(EC.presence_of_all_elements_located, self.ALL_DISCUSS)
        res = []
        for i in range(len(arr)):
            user = self.find_element_by_parent(arr[i], EC.presence_of_element_located, self.DISCUSS_USER).text
            content = self.find_element_by_parent(arr[i], EC.presence_of_element_located, self.DISCUSS_CONTENT).text
            like_cnt = self.find_element_by_parent(arr[i], EC.presence_of_element_located, self.DISCUSS_LIKE_CNT).text
            el = self.find_element_by_parent(arr[i], EC.presence_of_element_located, self.DISCUSS_DEL_BTN_P)
            has_del_btn = el.get_attribute("innerHTML").strip() != ''
            t = {
                'user': user,
                'content': content,
                'like_cnt': like_cnt,
                'has_del_btn': has_del_btn
            }
            res.append(t)
        return res

    @allure.step('判断是否有该评论')
    def has_this_discuss(self, user, content):
        time.sleep(0.2)
        arr = self.find_element(EC.presence_of_all_elements_located, self.ALL_DISCUSS)
        for i in range(len(arr)):
            u = self.find_element_by_parent(arr[i], EC.presence_of_element_located, self.DISCUSS_USER).text
            c = self.find_element_by_parent(arr[i], EC.presence_of_element_located, self.DISCUSS_CONTENT).text
            if u == user and c == content:
                return True
        return False

    @allure.step('点击评论区排序')
    def click_discuss_sort_btn(self):
        self.find_element(EC.visibility_of_element_located, self.DISCUSS_SORT_BTN).click()

    @allure.step('点击评论点赞按钮')
    def click_discuss_like_btn(self, index):
        pel = self.find_element(EC.presence_of_all_elements_located, self.ALL_DISCUSS)[index]
        self.find_element_by_parent(pel, EC.visibility_of_element_located, self.DISCUSS_LIKE_BTN).click()

    @allure.step('点击评论删除按钮')
    def click_discuss_del_btn(self, index):
        pel = self.find_element(EC.presence_of_all_elements_located, self.ALL_DISCUSS)[index]
        self.find_element_by_parent(pel, EC.visibility_of_element_located, self.DISCUSS_DEL_BTN).click()
