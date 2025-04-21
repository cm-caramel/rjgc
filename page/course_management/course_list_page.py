from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 课程管理页
class CourseListPage(BasePage):
    ADD_COURSE_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[3]/span/button')
    COURSES = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/span/div/div[2]/div/div/div')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.home.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('验证当前在课程管理页')
    def verify_page(self):
        return self.waiter.until(EC.url_to_be(conf['base_url'] + 'coursemanage'))

    @allure.step("点击新建课程")
    def click_add_course_btn(self):
        self.find_element(EC.visibility_of_element_located, self.ADD_COURSE_BTN).click()
        from page.course_management.course_add_page import CourseAddPage
        return CourseAddPage(self.driver)

    @allure.step("点击课程")
    def click_course_by_index(self, index):
        el = self.find_element(EC.presence_of_all_elements_located, self.COURSES)[index]
        self.driver.execute_script("arguments[0].scrollIntoView();", el)
        el.click()
        from page.course_management.course_detail_page import CourseDetailPage
        return CourseDetailPage(self.driver)

    @allure.step('获取课程名称')
    def get_course_name_by_index(self, index):
        pel = self.find_element(EC.presence_of_all_elements_located, self.COURSES)[index]
        return self.find_element_by_parent(pel, EC.presence_of_element_located,
                                           (By.XPATH, './/h2')).text

    @allure.step('获取课程时间')
    def get_course_time_by_index(self, index):
        pel = self.find_element(EC.presence_of_all_elements_located, self.COURSES)[index]
        return self.find_element_by_parent(pel, EC.presence_of_element_located,
                                           (By.XPATH, './/h5')).text

    @allure.step('获取课程数量')
    def get_course_count(self):
        return len(self.find_element(EC.presence_of_all_elements_located, self.COURSES))

