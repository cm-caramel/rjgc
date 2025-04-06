import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 班级详情页。点击班级右侧的详情按钮
class ClassDetailPage(BasePage):
    RETURN_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/header/div/div[3]/button')
    IMPORT_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/div['
                            '2]/div/section/footer/div/div/div[2]/button')
    TABLE_RECORDS = (By.XPATH, '//tbody//div[normalize-space(text())]/../..')
    TABLE_PAGE_SWITCH = (By.XPATH, '//*[@id="app"]//ul[@class="el-pager"]/li')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('点击导入用户')
    def click_import_btn(self):
        self.find_element(EC.visibility_of_element_located, self.IMPORT_BTN).click()
        from page.course_management.import_student_page import ImportStudentPage
        return ImportStudentPage(self.driver)

    @allure.step('点击返回按钮')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()

    @allure.step('获取姓名')
    def get_name_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.TABLE_RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[1]/div')).text

    @allure.step('获取学号')
    def get_account_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.TABLE_RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[2]/div')).text

    @allure.step('获取行政班')
    def get_class_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.TABLE_RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[3]/div')).text

    @allure.step('点击删除')
    def click_delete_btn_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.TABLE_RECORDS)[index]
        self.find_element_by_parent(pel, EC.visibility_of_element_located,
                                    (By.XPATH, './td[4]/div/div/div/button')).click()
        from page.course_management.delete_page import DeletePage
        return DeletePage(self.driver)

    @allure.step('切换到表格最后一页')
    def switch_to_last_page(self):
        time.sleep(0.1)
        arr = self.find_element(EC.visibility_of_all_elements_located, self.TABLE_PAGE_SWITCH)
        a = ActionChains(self.driver)
        a.move_to_element(arr[len(arr) - 1]).click().perform()
        time.sleep(0.1)
