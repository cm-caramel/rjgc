import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.utils import *
from page.base_page import BasePage


# 个人、结对、团队项目共用此页面
class ProjectListPage(BasePage):
    UPLOAD_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/section/footer/div/div'
                            '/div[2]/span/button')
    PAGE_TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/div/div[2]')
    RECORDS = (By.XPATH, '//tbody//div[normalize-space(text())]/../..')
    PAGE_SWITCH = (By.XPATH, '//*[@id="app"]//ul[@class="el-pager"]/li')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.home.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('验证当前在个人项目列表')
    def verify_personal_page(self):
        return self.waiter.until(EC.url_to_be(conf['base_url'] + 'project/soloproj'))

    @allure.step('验证当前在结对编程列表')
    def verify_pair_page(self):
        return self.waiter.until(EC.url_to_be(conf['base_url'] + 'project/twinproj'))

    @allure.step('验证当前在团队项目列表')
    def verify_team_page(self):
        return self.waiter.until(EC.url_to_be(conf['base_url'] + 'project/teamproj'))

    @allure.step("点击上传按钮")
    def click_upload_btn(self):
        self.find_element(EC.visibility_of_element_located, self.UPLOAD_BTN).click()
        from page.project_management.project_upload_page import ProjectUploadPage
        return ProjectUploadPage(self.driver)

    @allure.step("获取页面标题")
    def get_page_title(self):
        return self.find_element(EC.visibility_of_element_located, self.PAGE_TITLE).text

    @allure.step("获取项目名称")
    def get_project_name_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[2]/div')).text

    @allure.step("获取来自学校")
    def get_school_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.presence_of_element_located, (By.XPATH, './td[3]/div')).text

    @allure.step("获取难度")
    def get_difficulty_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[4]/div')).text

    @allure.step("获取使用次数")
    def get_use_times_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[5]/div')).text

    @allure.step("点击详情")
    def click_detail_btn_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        self.find_element_by_parent(pel, EC.visibility_of_element_located,
                                    (By.XPATH, './td[6]/div/div/div[1]/button')).click()
        from page.project_management.project_detail_page import ProjectDetailPage
        return ProjectDetailPage(self.driver)

    @allure.step("点击删除")
    def click_delete_btn_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        self.find_element_by_parent(pel, EC.visibility_of_element_located,
                                    (By.XPATH, './td[6]/div/div/div[2]/button')).click()
        from page.project_management.project_delete_page import ProjectDeletePage
        return ProjectDeletePage(self.driver)

    @allure.step('获取开发语言')
    def get_language_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[4]/div')).text

    @allure.step('获取涉及技术')
    def get_technology_by_index(self, index):
        pel = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)[index]
        return self.find_element_by_parent(pel, EC.visibility_of_element_located, (By.XPATH, './td[5]/div')).text

    @allure.step('切换到表格最后一页')
    def switch_to_last_page(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.PAGE_SWITCH)
        # arr[len(arr)-1].click()
        a = ActionChains(self.driver)
        a.move_to_element(arr[len(arr) - 1]).click().perform()
        time.sleep(0.1)


