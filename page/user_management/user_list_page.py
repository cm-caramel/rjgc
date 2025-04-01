import time
import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


class UserListPage(BasePage):
    IMPORT_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/div/section/footer/div'
                            '/div/div[2]/button')
    PAGE_TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/section/main/div/div/div/div[2]')
    HEAD_SCHOOL_BTN = (By.XPATH, '//table[@class="el-table__header"]//th[3]/div/div')
    HEAD_USER_KIND_BTN = (By.XPATH, '//table[@class="el-table__header"]//th[4]/div/div')
    POPUP_MENU = (By.XPATH, '//body/div[2]//div[@data-popper-placement="bottom" and @aria-hidden="false"]')
    POPUP_MENU_ITEM = '//body/div[2]//div[@data-popper-placement="bottom"]//li[text()="{}"]'
    PAGE_SWITCH = (By.XPATH, '//*[@id="app"]//ul[@class="el-pager"]/li')
    RECORDS = (By.XPATH, '//tbody//div[normalize-space(text())]/../..')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step("点击导入用户")
    def click_import_btn(self):
        self.find_element(EC.visibility_of_element_located, self.IMPORT_BTN).click()
        from page.user_management.user_import_page import UserImportPage
        return UserImportPage(self.driver)

    @allure.step('点击详情')
    def click_detail_btn_by_index(self, index):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        self.find_element_by_parent(arr[index], EC.visibility_of_element_located,
                                    (By.XPATH, './td[5]/div/div/div[1]/button')).click()
        from page.user_management.user_detail_page import UserDetailPage
        return UserDetailPage(self.driver)

    @allure.step('点击删除')
    def click_delete_btn_by_index(self, index):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        self.find_element_by_parent(arr[index], EC.visibility_of_element_located,
                                    (By.XPATH, './td[5]/div/div/div[2]/button')).click()
        from page.user_management.user_delete_page import UserDeletePage
        return UserDeletePage(self.driver)

    @allure.step('获取姓名')
    def get_name_by_index(self, index):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        return self.find_element_by_parent(arr[index], EC.presence_of_element_located, (By.XPATH, './td[1]/div')).text

    @allure.step('获取工号')
    def get_account_by_index(self, index):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        return self.find_element_by_parent(arr[index], EC.presence_of_element_located, (By.XPATH, './td[2]/div')).text

    @allure.step('获取学校')
    def get_school_by_index(self, index):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        return self.find_element_by_parent(arr[index], EC.presence_of_element_located, (By.XPATH, './td[3]/div')).text

    @allure.step('获取用户类型')
    def get_user_kind_by_index(self, index):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        return self.find_element_by_parent(arr[index], EC.presence_of_element_located, (By.XPATH, './td[4]/div')).text

    @allure.step('获取班级')
    def get_class_by_index(self, index):
        return self.get_school_by_index(index)

    @allure.step('获取页面标题')
    def get_page_title(self):
        return self.find_element(EC.visibility_of_element_located, self.PAGE_TITLE).text

    @allure.step('表格筛选学校')
    def filter_school(self, school='全部学校'):
        self.find_element(EC.visibility_of_element_located, self.HEAD_SCHOOL_BTN).click()
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.POPUP_MENU_ITEM.format(school))).click()

    @allure.step('表格筛选用户类型')
    def filter_user_kind(self, kind='全部'):
        self.find_element(EC.visibility_of_element_located, self.HEAD_USER_KIND_BTN).click()
        self.find_element(EC.visibility_of_element_located,
                          (By.XPATH, self.POPUP_MENU_ITEM.format(kind))).click()

    @allure.step('获取菜单内所有学校')
    def get_all_school_in_menu(self):
        self.find_element(EC.visibility_of_element_located, self.HEAD_SCHOOL_BTN).click()
        pel = self.find_element(EC.visibility_of_element_located, self.POPUP_MENU)
        arr = self.find_element_by_parent(pel, EC.presence_of_all_elements_located, (By.XPATH, './/li'))
        self.find_element(EC.visibility_of_element_located, self.HEAD_SCHOOL_BTN).click()
        arr = [i.text for i in arr]
        return arr[1:]

    @allure.step('获取当前页所有学校')
    def get_all_school_in_page(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        schools = set()
        for pel in arr:
            t = self.find_element_by_parent(pel, EC.presence_of_element_located, (By.XPATH, './td[3]/div')).text
            schools.add(t)
        # return len(arr)
        return schools

    @allure.step('获取当前页所有用户类型')
    def get_all_user_kind_in_page(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.RECORDS)
        users = set()
        for pel in arr:
            t = self.find_element_by_parent(pel, EC.presence_of_element_located, (By.XPATH, './td[4]/div')).text
            users.add(t)
        return users

    @allure.step('切换到表格最后一页')
    def switch_to_last_page(self):
        arr = self.find_element(EC.visibility_of_all_elements_located, self.PAGE_SWITCH)
        # arr[len(arr)-1].click()
        a = ActionChains(self.driver)
        a.move_to_element(arr[len(arr) - 1]).click().perform()
        time.sleep(0.1)
