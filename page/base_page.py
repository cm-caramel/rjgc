import allure
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from common.exceptions import TechnicalException
from common.utils import conf


class BasePage:
    ALERT = (By.XPATH, '//*[@role="alert"]/p')

    def __init__(self, driver):
        self.driver = driver
        self.waiter = WebDriverWait(self.driver, conf['wait_time'])

    def find_element(self, condition, locator):
        try:
            return self.waiter.until(condition(locator))
        except Exception as e:
            raise TechnicalException(f'\n\n元素定位失败，定位器：{locator}\n{str(e)}') from e

    # 点击element所在的地方，x/y是offset。因为有些元素是不可点击的，所以直接用ActionChains来操作
    def click_element_position(self, condition, locator, x=0, y=0):
        a = ActionChains(self.driver)
        a.move_to_element(self.find_element(condition, locator))
        a.move_by_offset(x, y)
        a.click()
        a.perform()

    # el_alert指的是顶部弹出的element ui组件提示，下面的alert则是浏览器的自带提示
    @allure.step("获取弹出的提示文本")
    def get_el_alert_text(self):
        time.sleep(0.5)  # 多个alert同时出现时，加一个延时让最新出现的alert加载完毕，否则会获取到旧的
        t = self.find_element(EC.presence_of_all_elements_located, self.ALERT)
        return t.pop().text

    def switch_to_alert(self):
        try:
            return self.waiter.until(EC.alert_is_present())
        except Exception as e:
            raise TechnicalException(f'\n\n无法定位到alert\n{str(e)}') from e

    @allure.step("获取alert文本")
    def get_alert_text(self):
        return self.switch_to_alert().text

    @allure.step("点击确定关闭alert")
    def click_alert_ok(self):
        alert = self.switch_to_alert()
        try:
            alert.accept()
            return True
        except Exception as e:
            return False
