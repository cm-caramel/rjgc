from page.login_page import LoginPage
from common.utils import *


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('登录')
class TestLogin:
    @pytest.mark.login
    @pytest.mark.parallel
    @pytest.mark.parametrize("datas", read_data_yaml('data/login.yaml'))
    def test_login(self, login_page_d, db_conn, datas):
        try:
            allure.dynamic.title(datas['title'])
            allure.dynamic.description('前置条件：\n1. 打开应用，默认进入登录页')
            login_page = LoginPage(login_page_d)
            school = datas['school']
            user = datas['user']
            pwd = datas['pwd']
            home_page = login_page.login(school, user, pwd)
            if datas['success']:
                with allure.step('提示“登录成功”'):
                    assert login_page.get_el_alert_text() == '登录成功！'
                with allure.step('跳转至首页'):
                    assert home_page.verify_page()
            else:
                with allure.step('提示“用户名或密码错误”'):
                    assert login_page.get_el_alert_text() == '用户名或密码错误！'
                with allure.step('停留在登录页'):
                    assert login_page.maintain_page()
            if sql_check:
                with allure.step('数据库验证'):
                    with db_conn.cursor() as cursor:
                        cursor.execute(f"select * "
                                       f"from v_user "
                                       f"where school_name = '{school}' "
                                       f"AND user_account = '{user}' "
                                       f"AND user_password = '{pwd}'")
                        res = cursor.fetchone()
                    if datas['success']:
                        assert res is not None
                        assert res['USER_NAME'] == home_page.top_side_bar.get_menu_btn_text()
                    else:
                        assert res is None
        except Exception as e:
            screenshot(login_page_d)
            raise e

    @allure.title('跳过登录')
    @pytest.mark.login
    @pytest.mark.parallel
    def test_skip_login(self, login_page_d):
        try:
            allure.dynamic.description('前置条件：\n1. 打开应用，默认进入登录页')
            login_page = LoginPage(login_page_d)
            with allure.step('点击“直接通过url访问首页”'):
                login_page_d.get(conf['base_url'] + 'home')
            with allure.step('alert提示无权限'):
                assert login_page.get_alert_text() == '无权限'
                assert login_page.click_alert_ok()
            with allure.step('停留在登录页'):
                assert login_page.maintain_page()
        except Exception as e:
            screenshot(login_page_d)
            raise e

    @allure.title('登录后退出重登成功')
    @pytest.mark.login
    @pytest.mark.parallel
    def test_logout_login_success(self, login_page_d):
        try:
            allure.dynamic.description('前置条件：\n1. 打开应用，默认进入登录页')
            login_page = LoginPage(login_page_d)
            home_page = login_page.login('东莞理工学院', '10010', '123')
            with allure.step('提示“登录成功”'):
                assert login_page.get_el_alert_text() == '登录成功！'
            with allure.step('跳转至首页'):
                assert home_page.verify_page()
            bar = home_page.top_side_bar
            login_page_2 = bar.click_menu_logout()
            with allure.step('跳转至登录页'):
                assert login_page.verify_page()
            login_page_2.login('东莞理工学院', '10020', '123')
            with allure.step('提示“登录成功”'):
                assert login_page.get_el_alert_text() == '登录成功！'
            with allure.step('跳转至首页'):
                assert home_page.verify_page()
        except Exception as e:
            screenshot(login_page_d)
            raise e

    @allure.title('登录后退出重登失败')
    @pytest.mark.login
    @pytest.mark.parallel
    def test_logout_login_fail(self, login_page_d):
        try:
            allure.dynamic.description('前置条件：\n1. 打开应用，默认进入登录页')
            login_page = LoginPage(login_page_d)
            home_page = login_page.login('东莞理工学院', '10010', '123')
            with allure.step('提示“登录成功”'):
                assert login_page.get_el_alert_text() == '登录成功！'
            with allure.step('跳转至首页'):
                assert home_page.verify_page()
            bar = home_page.top_side_bar
            login_page_2 = bar.click_menu_logout()
            with allure.step('跳转至登录页'):
                assert login_page.verify_page()
            login_page_2.login('东莞理工学院', '10010', '12345')
            with allure.step('提示“用户名或密码错误”'):
                assert login_page.get_el_alert_text() == '用户名或密码错误！'
            with allure.step('停留在登录页'):
                assert login_page.maintain_page()
        except Exception as e:
            screenshot(login_page_d)
            raise e


