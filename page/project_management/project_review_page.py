import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 项目审核
class ProjectReviewPage(BasePage):
    HEAD_REQUEST_KIND_BTN = (By.XPATH, '//table/thead/tr/th[1]/div/div')
    HEAD_PROJECT_KIND_BTN = (By.XPATH, '//table/thead/tr/th[2]/div/div')
    HEAD_STATUS_BTN = (By.XPATH, '//table/thead/tr/th[6]/div/div')
    POPUP_MENU_ITEM = '//body/div[2]//div[@data-popper-placement="bottom" and @aria-hidden="false"]//li[text()="{}"]'
    PAGE_SWITCH = (By.XPATH, '//*[@id="app"]//ul[@class="el-pager"]/li')
    RECORDS = (By.XPATH, '//tbody//div[normalize-space(text())]/../..')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('验证当前为项目审核页')
    def verify_page(self):
        return self.waiter.until(EC.url_to_be(conf['base_url'] + 'project/auditproj'))

    @allure.step('获取请求类型')
    def get_request_kind_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[1]/div')).text

    @allure.step('获取项目类型')
    def get_project_kind_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[2]/div')).text

    @allure.step('获取项目名称')
    def get_project_name_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.presence_of_element_located, (By.XPATH, './td[3]/div')).text

    @allure.step('获取发布者')
    def get_publisher_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[4]/div')).text

    @allure.step('获取审核状态')
    def get_status_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[6]/div')).text

    @allure.step('点击查看详情')
    def click_detail_btn_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        self.find_element_by_parent(pel, EC.visibility_of_element_located,
                                    (By.XPATH, './td[5]/div/button')).click()
        from page.project_management.review_detail_page import ReviewDetailPage
        return ReviewDetailPage(self.driver)

    @allure.step('切换到表格最后一页')
    def switch_to_last_page(self):
        time.sleep(0.1)
        arr = self.find_element(EC.visibility_of_all_elements_located, self.PAGE_SWITCH)
        # arr[len(arr)-1].click()
        a = ActionChains(self.driver)
        a.move_to_element(arr[len(arr) - 1]).click().perform()
        time.sleep(0.1)

    @allure.step('表格筛选请求类型')
    def filter_request_kind(self, kind='全选'):
        self.find_element(EC.visibility_of_element_located, self.HEAD_REQUEST_KIND_BTN).click()
        time.sleep(0.1)
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.POPUP_MENU_ITEM.format(kind))).click()
        time.sleep(0.1)

    @allure.step('表格筛选项目类型')
    def filter_project_kind(self, kind='全选'):
        self.find_element(EC.visibility_of_element_located, self.HEAD_PROJECT_KIND_BTN).click()
        time.sleep(0.1)
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.POPUP_MENU_ITEM.format(kind))).click()
        time.sleep(0.1)

    @allure.step('表格筛选审核状态')
    def filter_status(self, status='全选'):
        self.find_element(EC.visibility_of_element_located, self.HEAD_STATUS_BTN).click()
        time.sleep(0.1)
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.POPUP_MENU_ITEM.format(status))).click()
        time.sleep(0.1)

    @allure.step('获取当前页所有请求类型')
    def get_all_request_kind_in_page(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        kinds = set()
        for pel in arr:
            t = self.find_element_by_parent(pel, EC.presence_of_element_located, (By.XPATH, './td[1]/div')).text
            kinds.add(t)
        return kinds

    @allure.step('获取当前页所有项目类型')
    def get_all_project_kind_in_page(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        kinds = set()
        for pel in arr:
            t = self.find_element_by_parent(pel, EC.presence_of_element_located, (By.XPATH, './td[2]/div')).text
            kinds.add(t)
        return kinds

    @allure.step('获取当前页所有审核状态')
    def get_all_status_in_page(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        kinds = set()
        for pel in arr:
            t = self.find_element_by_parent(pel, EC.presence_of_element_located, (By.XPATH, './td[6]/div')).text
            kinds.add(t)
        return kinds


