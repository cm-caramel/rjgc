from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.base_page import BasePage
from common.utils import *


# 资源审核详情页。教材和工具审核共用
class ReviewDetailPage(BasePage):
    TITLE = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[1]/div[2]/span[2]')
    USER = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[1]/div[3]/span[2]')
    KIND = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[1]/div[5]/span[2]')
    CONFIRM_BTN_P = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[3]/div[2]')
    REJECT_BTN_P = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[3]/div[3]')
    CONFIRM_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[3]/div[2]/span/button')
    REJECT_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[3]/div[3]/span/button')
    RETURN_BTN = (By.XPATH, '//*[@id="app"]/div/section/section/div/main/div/div[3]/div[4]/button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step('获取节名称')
    def get_title(self):
        return self.find_element(EC.presence_of_element_located, self.TITLE).text

    @allure.step('获取用户')
    def get_user(self):
        return self.find_element(EC.visibility_of_element_located, self.USER).text

    @allure.step('获取类型')
    def get_kind(self):
        return self.find_element(EC.visibility_of_element_located, self.KIND).text

    @allure.step('获取确认按钮的显示状态')
    def is_confirm_btn_visible(self):
        p = self.find_element(EC.presence_of_element_located, self.CONFIRM_BTN_P)
        return p.get_attribute("innerHTML").strip() != ''

    @allure.step('获取否决按钮的显示状态')
    def is_reject_btn_visible(self):
        p = self.find_element(EC.presence_of_element_located, self.REJECT_BTN_P)
        return p.get_attribute("innerHTML").strip() != ''

    @allure.step('点击确认按钮')
    def click_confirm_btn(self):
        self.find_element(EC.visibility_of_element_located, self.CONFIRM_BTN).click()
        from page.textbook_management.resource_review.textbook_tool_review_page import TextbookToolReviewPage
        return TextbookToolReviewPage(self.driver)

    @allure.step('点击否决按钮')
    def click_reject_btn(self):
        self.find_element(EC.visibility_of_element_located, self.REJECT_BTN).click()
        from page.textbook_management.resource_review.textbook_tool_review_page import TextbookToolReviewPage
        return TextbookToolReviewPage(self.driver)

    @allure.step('点击返回按钮')
    def click_return_btn(self):
        self.find_element(EC.visibility_of_element_located, self.RETURN_BTN).click()
        from page.textbook_management.resource_review.textbook_tool_review_page import TextbookToolReviewPage
        return TextbookToolReviewPage(self.driver)

