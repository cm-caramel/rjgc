import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage


# 顶部和侧边的功能栏（首页中所有页面都共用这个）
class TopSideBar(BasePage):
    TOP_SEARCH = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[2]/div/div/input')
    SEARCH_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[2]/div/div/span')
    MENU_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span')
    MENU_BTN_TEXT = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/div/span')
    MENU_LIST = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/ul')
    PERSONAL_INFO = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/ul/li[1]')
    CHANGE_PWD = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/ul/li[2]')
    LOGOUT = (By.XPATH, '//*[@id="app"]/div/section/section/div/header/div/div[3]/div/span/ul/li/ul/li[3]')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('顶部搜索框输入')
    def input_search(self, text):
        el = self.find_element(EC.visibility_of_element_located, self.TOP_SEARCH)
        el.clear()
        el.send_keys(text)

    @allure.step('点击搜索框左侧放大镜按钮')
    def click_search(self):
        self.find_element(EC.visibility_of_element_located, self.SEARCH_BTN).click()

    @allure.step('顶部搜索框输入并回车搜索')
    def input_search_and_enter(self, text):
        el = self.find_element(EC.visibility_of_element_located, self.TOP_SEARCH)
        el.clear()
        el.send_keys(text + Keys.ENTER)

    @allure.step('获取顶部菜单栏处的文本')
    def get_menu_btn_text(self):
        return self.find_element(EC.visibility_of_element_located, self.MENU_BTN_TEXT).text

    @allure.step('点击个人信息')
    def click_menu_personal_info(self):
        el = self.find_element(EC.presence_of_element_located, self.MENU_LIST)
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.MENU_BTN).click()
        self.find_element(EC.visibility_of_element_located, self.PERSONAL_INFO).click()
        from page.home.personal_info_page import PersonalInfoPage
        return PersonalInfoPage(self.driver)

    @allure.step('点击修改密码')
    def click_menu_change_pwd(self):
        el = self.find_element(EC.presence_of_element_located, self.MENU_LIST)
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.MENU_BTN).click()
        self.find_element(EC.visibility_of_element_located, self.CHANGE_PWD).click()
        from page.home.change_pwd_page import ChangePwdPage
        return ChangePwdPage(self.driver)

    @allure.step('点击安全退出')
    def click_menu_logout(self):
        el = self.find_element(EC.presence_of_element_located, self.MENU_LIST)
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.MENU_BTN).click()
        self.find_element(EC.visibility_of_element_located, self.LOGOUT).click()
        from page.login.login_page import LoginPage
        return LoginPage(self.driver)

    @staticmethod
    def get_left_ul_xpath(item_name):
        return By.XPATH, f'//*[@id="app"]/div/section/aside/div/div/div/div//*[text()="{item_name}"]/../../ul'

    @staticmethod
    def get_left_item_xpath(item_name):
        return By.XPATH, f'//*[@id="app"]/div/section/aside/div/div/div/div//*[text()="{item_name}"]'

    @allure.step('通过左侧栏切换到首页')
    def switch_to_home(self):
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('首页')).click()
        from page.home.home_page import HomePage
        return HomePage(self.driver)

    @allure.step('通过左侧栏切换到教材章节')
    def switch_to_textbook_chapter(self):
        el = self.find_element(EC.presence_of_element_located, self.get_left_ul_xpath('教材管理'))
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('教材管理')).click()
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('教材章节')).click()
        from page.textbook_management.textbook.textbook_page import TextbookPage
        return TextbookPage(self.driver)

    @allure.step('通过左侧栏切换到工具列表')
    def switch_to_tool_list(self):
        el = self.find_element(EC.presence_of_element_located, self.get_left_ul_xpath('教材管理'))
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('教材管理')).click()
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('工具列表')).click()
        from page.textbook_management.tool.tool_page import ToolPage
        return ToolPage(self.driver)

    @allure.step('通过左侧栏切换到教材章节（学生）')
    def switch_to_textbook_chapter_stu(self):
        el = self.find_element(EC.presence_of_element_located, self.get_left_ul_xpath('教材资源'))
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('教材资源')).click()
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('教材章节')).click()
        from page.textbook_management.textbook.textbook_page import TextbookPage
        return TextbookPage(self.driver)

    @allure.step('通过左侧栏切换到工具列表（学生）')
    def switch_to_tool_list_stu(self):
        el = self.find_element(EC.presence_of_element_located, self.get_left_ul_xpath('教材资源'))
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('教材资源')).click()
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('工具列表')).click()
        from page.textbook_management.tool.tool_page import ToolPage
        return ToolPage(self.driver)

    @allure.step('通过左侧栏切换到资源审核')
    def switch_to_resource_review(self):
        el = self.find_element(EC.presence_of_element_located, self.get_left_ul_xpath('教材管理'))
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('教材管理')).click()
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('资源审核')).click()
        from page.textbook_management.resource_review.textbook_tool_review_page import TextbookToolReviewPage
        return TextbookToolReviewPage(self.driver)

    @allure.step('通过左侧栏切换到个人项目')
    def switch_to_personal_project(self):
        el = self.find_element(EC.presence_of_element_located, self.get_left_ul_xpath('项目管理'))
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('项目管理')).click()
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('个人项目')).click()
        from page.project_management.project_list_page import ProjectListPage
        return ProjectListPage(self.driver)

    @allure.step('通过左侧栏切换到结对编程')
    def switch_to_pair_programming(self):
        el = self.find_element(EC.presence_of_element_located, self.get_left_ul_xpath('项目管理'))
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('项目管理')).click()
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('结对编程')).click()
        from page.project_management.project_list_page import ProjectListPage
        return ProjectListPage(self.driver)

    @allure.step('通过左侧栏切换到团队项目')
    def switch_to_team_project(self):
        el = self.find_element(EC.presence_of_element_located, self.get_left_ul_xpath('项目管理'))
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('项目管理')).click()
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('团队项目')).click()
        from page.project_management.project_list_page import ProjectListPage
        return ProjectListPage(self.driver)

    @allure.step('通过左侧栏切换到项目审核')
    def switch_to_project_review(self):
        el = self.find_element(EC.presence_of_element_located, self.get_left_ul_xpath('项目管理'))
        if not el.is_displayed():
            self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('项目管理')).click()
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('项目审核')).click()
        from page.project_management.project_review_page import ProjectReviewPage
        return ProjectReviewPage(self.driver)

    @allure.step('通过左侧栏切换到课程管理')
    def switch_to_course_management(self):
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('课程管理')).click()
        from page.course_management.course_list_page import CourseListPage
        return CourseListPage(self.driver)

    @allure.step('通过左侧栏切换到用户管理')
    def switch_to_user_management(self):
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('用户管理')).click()
        from page.user_management.user_list_page import UserListPage
        return UserListPage(self.driver)

    @allure.step('通过左侧栏切换到学生管理')
    def switch_to_student_management(self):
        self.find_element(EC.visibility_of_element_located, self.get_left_item_xpath('学生管理')).click()
        from page.user_management.user_list_page import UserListPage
        return UserListPage(self.driver)
