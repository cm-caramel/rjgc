import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.utils import conf
from page.base_page import BasePage


# 首页（不区分角色）
class HomePage(BasePage):
    MSG_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[1]/button')
    TASK_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[2]/button')
    STUDENT_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[3]/button')
    TEACHER_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[4]/button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        from page.home.top_side_bar import TopSideBar
        self.top_side_bar = TopSideBar(driver)

    @allure.step('验证当前页面为首页')
    def verify_page(self):
        return self.waiter.until(EC.url_to_be(conf['base_url'] + 'home'))

    @allure.step('验证没有发生页面跳转')
    def maintain_page(self):
        try:
            return not WebDriverWait(self.driver, conf['wait_time'] / 4).until(
                EC.url_changes(conf['base_url'] + 'home')
            )
        except TimeoutException as e:
            return True
        except Exception as e:
            raise e

    @allure.step('点击消息')
    def click_msg_btn(self):
        self.find_element(EC.presence_of_element_located, self.MSG_BTN).click()

    @allure.step('点击待办事项')
    def click_task_btn(self):
        self.find_element(EC.presence_of_element_located, self.TASK_BTN).click()

    @allure.step('点击导入学生用户')
    def click_student_btn(self):
        self.find_element(EC.presence_of_element_located, self.STUDENT_BTN).click()

    @allure.step('点击导入教师用户')
    def click_teacher_btn(self):
        self.find_element(EC.presence_of_element_located, self.TEACHER_BTN).click()

    def has_page_change(self):
        try:
            return WebDriverWait(self.driver, conf['wait_time'] / 4).until(
                EC.url_changes(conf['base_url'] + 'home')
            )
        except TimeoutException as e:
            return False
        except Exception as e:
            raise e
