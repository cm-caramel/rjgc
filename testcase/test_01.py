import allure
import pytest
from common.utils import *
from page.login_page import LoginPage
from page.home_page import HomePage
from page.personal_info_page import PersonalInfoPage
import time
import yaml


@pytest.mark.parametrize("home_page", [
        pytest.param({"school": "东莞理工学院", "user": "10041", "pwd": "123"})
    ], indirect=True)
@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('测试')
class Test01:
    # @pytest.mark.test
    # def test01(self):
    #     with open('data/personal_info.yaml', 'r', encoding='utf-8') as f:
    #         data = yaml.safe_load(f)
    #     print('\n========== res ==========\n')
    #     print(data[2].get('sex') == '')

    # @pytest.mark.test
    def test02(self, home_page):
        try:
            bar = home_page.top_side_bar
            bar.switch_to_user_management()
            time.sleep(3)
        except Exception as e:
            screenshot(home_page.driver)
            raise e

    # @pytest.mark.test
    def test03(self, change_pwd_page, db_conn):
        change_pwd_page.input_old_pwd('123')
        change_pwd_page.input_new_pwd('123456')
        change_pwd_page.input_confirm_pwd('123456')
        change_pwd_page.click_confirm_btn()
        print(change_pwd_page.close_if_open())



