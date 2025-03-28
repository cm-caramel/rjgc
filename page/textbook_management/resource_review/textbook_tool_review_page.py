from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from common.exceptions import *
from page.base_page import BasePage
from page.textbook_management.resource_review.review_detail_page import ReviewDetailPage


# 教材、工具审核页面（共用）
class TextbookToolReviewPage(BasePage):
    PAGE_TITLE = (By.XPATH, '//*[@id="app"]//div[contains(@class, "is-active")]/div/span/div/div/div[2]')
    LEFT_ARROW = (By.XPATH, '//button[@class="el-carousel__arrow el-carousel__arrow--left"]')
    RIGHT_ARROW = (By.XPATH, '//button[@class="el-carousel__arrow el-carousel__arrow--right"]')
    PAGE_SWITCH = (By.XPATH, '//*[@id="app"]//div[contains(@class, "is-active")]//footer//ul/li')
    RECORDS = (
    By.XPATH, '//*[@id="app"]//div[contains(@class, "is-active")]//tbody//div[normalize-space(text())]/../..')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('验证当前页面为资源审核页')
    def verify_page(self):
        return self.waiter.until(EC.url_to_be(conf['base_url'] + 'audit'))

    @allure.step('验证当前页面为教材审核页')
    def verify_textbook_review_page(self):
        f = self.verify_page()
        title = self.find_element(EC.visibility_of_element_located, self.PAGE_TITLE).text
        return f and title == '教材审核请求列表'

    @allure.step('验证当前页面为工具审核页')
    def verify_tool_review_page(self):
        f = self.verify_page()
        title = self.find_element(EC.visibility_of_element_located, self.PAGE_TITLE).text
        return f and title == '工具审核请求列表'

    @allure.step('点击左箭头')
    def click_left_arrow(self):
        self.click_element_position(EC.presence_of_element_located, self.PAGE_TITLE)
        self.click_element_position(EC.presence_of_element_located, self.LEFT_ARROW)

    @allure.step('点击右箭头')
    def click_right_arrow(self):
        self.click_element_position(EC.presence_of_element_located, self.PAGE_TITLE)
        self.click_element_position(EC.presence_of_element_located, self.RIGHT_ARROW)

    @allure.step('切换到教材审核页')
    def switch_to_textbook_review(self):
        if not self.verify_textbook_review_page():
            self.click_left_arrow()

    @allure.step('切换到工具审核页')
    def switch_to_tool_review(self):
        if self.verify_tool_review_page():
            self.click_right_arrow()

    @allure.step('切换到表格最后一页')
    def switch_to_last_page(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.PAGE_SWITCH)
        # arr[len(arr)-1].click()
        a = ActionChains(self.driver)
        a.move_to_element(arr[len(arr) - 1]).click().perform()

    def get_last_record(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        return arr[len(arr) - 1]

    @allure.step('获取最新记录的请求类型')
    def get_last_record_kind(self):
        pel = self.get_last_record()
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[1]/div')).text

    @allure.step('获取最新记录的章节')
    def get_last_record_textbook_label(self):
        pel = self.get_last_record()
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[2]/div')).text

    @allure.step('获取最新记录的章节名称')
    def get_last_record_textbook_title(self):
        pel = self.get_last_record()
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[3]/div')).text

    @allure.step('获取最新记录的工具序号')
    def get_last_record_tool_label(self):
        return self.get_last_record_textbook_label()

    @allure.step('获取最新记录的工具名称')
    def get_last_record_tool_title(self):
        return self.get_last_record_textbook_title()

    @allure.step('获取最新记录的请求来源')
    def get_last_record_source(self):
        pel = self.get_last_record()
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[4]/div')).text

    @allure.step('获取最新记录的审核状态')
    def get_last_record_status(self):
        pel = self.get_last_record()
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[6]/div')).text

    @allure.step('点击最新记录的查看详情')
    def click_last_record_detail(self):
        pel = self.get_last_record()
        self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[5]/div/button')).click()
        return ReviewDetailPage(self.driver)

    def get_second_last_record(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        if len(arr) >= 2:
            return arr[-2]
        self.switch_to_last_page()
        arr = self.find_element(EC.visibility_of_all_elements_located, self.PAGE_SWITCH)
        if len(arr) < 2:
            raise TechnicalException('没有倒数第二条记录')
        a = ActionChains(self.driver)
        a.move_to_element(arr[-2]).click().perform()
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        return arr[-1]

    @allure.step('获取倒数第二条记录的信息')
    def get_second_last_record_info(self):
        pel = self.get_second_last_record()
        kind = self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[1]/div')).text
        label = self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[2]/div')).text
        title = self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[3]/div')).text
        source = self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[4]/div')).text
        status = self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[6]/div')).text
        btn = self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[5]/div/button'))
        res = {
            'kind': kind,
            'label': label,
            'title': title,
            'source': source,
            'status': status,
            'btn': btn
        }
        return res
