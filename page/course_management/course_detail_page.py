import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 课程详情页。课程管理页点击课程进入
class CourseDetailPage(BasePage):
    CLASS_LIST_TAB = (By.ID, 'tab-0')
    TASK_MANAGEMENT_TAB = (By.ID, 'tab-1')
    COURSE_DETAIL_TAB = (By.ID, 'tab-2')
    DELETE_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[3]/button')
    RETURN_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[4]/button')
    COURSE_NAME = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/div['
                             '2]/span/div/section/main/div[1]/div[3]/div/div/input')
    COURSE_TIME = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/div['
                             '2]/span/div/section/main/div[2]/div[3]/div/div/input')
    COURSE_INFO = (By.XPATH, '//*[@id="app"]//textarea')
    COURSE_CONFIRM_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/div['
                                    '2]/span/div/section/main/div[4]/div[2]/button')
    CLASS_ADD_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/div['
                               '2]/span/div/section/footer/div/div/div[2]/button')
    TASK_ADD_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/div['
                              '2]/span/div/section/footer/div/div/div[2]/button')
    TABLE_RECORDS = (By.XPATH, '//tbody//span[normalize-space(text())]/../../..')
    TABLE_PAGE_SWITCH = (By.XPATH, '//*[@id="app"]//ul[@class="el-pager"]/li')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("点击班级列表tab")
    def click_class_list_tab(self):
        self.find_element(EC.visibility_of_element_located, self.CLASS_LIST_TAB).click()

    @allure.step("点击作业管理tab")
    def click_task_management_tab(self):
        self.find_element(EC.visibility_of_element_located, self.TASK_MANAGEMENT_TAB).click()

    @allure.step("点击课程详情tab")
    def click_course_detail_tab(self):
        self.find_element(EC.visibility_of_element_located, self.COURSE_DETAIL_TAB).click()

    @allure.step("点击删除按钮")
    def click_delete_btn(self):
        self.find_element(EC.element_to_be_clickable, self.DELETE_BTN).click()
        from page.course_management.delete_page import DeletePage
        return DeletePage(self.driver)

    @allure.step("点击返回按钮")
    def click_return_btn(self):
        self.find_element(EC.element_to_be_clickable, self.RETURN_BTN).click()

    @allure.step("获取课程名称")
    def get_course_name(self):
        return self.find_element(EC.presence_of_element_located, self.COURSE_NAME).get_attribute('value')

    @allure.step("获取课程时间")
    def get_course_time(self):
        return self.find_element(EC.presence_of_element_located, self.COURSE_TIME).get_attribute('value')

    @allure.step("获取课程信息")
    def get_course_info(self):
        return self.find_element(EC.presence_of_element_located, self.COURSE_INFO).get_attribute('value')

    @allure.step('输入课程名称')
    def input_course_name(self, name):
        el = self.find_element(EC.visibility_of_element_located, self.COURSE_NAME)
        el.clear()
        el.send_keys(name)

    @allure.step('输入课程时间')
    def input_course_time(self, t):
        el = self.find_element(EC.visibility_of_element_located, self.COURSE_TIME)
        el.clear()
        el.send_keys(t)

    @allure.step('输入课程信息')
    def input_course_info(self, info):
        el = self.find_element(EC.visibility_of_element_located, self.COURSE_INFO)
        el.clear()
        el.send_keys(info)

    @allure.step('点击确认按钮')
    def click_course_confirm_btn(self):
        self.find_element(EC.element_to_be_clickable, self.COURSE_CONFIRM_BTN).click()

    @allure.step('点击添加班级')
    def click_class_add_btn(self):
        self.find_element(EC.visibility_of_element_located, self.CLASS_ADD_BTN).click()
        from page.course_management.class_add_page import ClassAddPage
        return ClassAddPage(self.driver)

    @allure.step('点击添加作业')
    def click_task_add_btn(self):
        self.find_element(EC.visibility_of_element_located, self.TASK_ADD_BTN).click()

    @allure.step('切换到表格最后一页')
    def switch_to_last_page(self):
        time.sleep(0.1)
        arr = self.find_element(EC.visibility_of_all_elements_located, self.TABLE_PAGE_SWITCH)
        a = ActionChains(self.driver)
        a.move_to_element(arr[len(arr) - 1]).click().perform()
        time.sleep(0.1)

    @allure.step('获取教学班级')
    def get_class_name_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.TABLE_RECORDS)[index]
        return self.find_element_by_parent(pel, EC.presence_of_element_located, (By.XPATH, './td[2]/div')).text

    @allure.step('点击详情')
    def click_class_detail_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.TABLE_RECORDS)[index]
        self.find_element_by_parent(pel, EC.visibility_of_element_located,
                                    (By.XPATH, './td[3]/div/div/div[1]/button')).click()
        from page.course_management.class_detail_page import ClassDetailPage
        return ClassDetailPage(self.driver)

    @allure.step('点击删除')
    def click_class_delete_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.TABLE_RECORDS)[index]
        self.find_element_by_parent(pel, EC.visibility_of_element_located,
                                    (By.XPATH, './td[3]/div/div/div[2]/button')).click()
        from page.course_management.delete_page import DeletePage
        return DeletePage(self.driver)

