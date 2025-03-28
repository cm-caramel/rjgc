import time
from common.utils import *

login_account = {
    "school": "东莞理工学院",
    "user": "10041",
    "pwd": "123"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('首页上方菜单-修改密码弹窗')
@pytest.mark.parametrize("home_page", [
        pytest.param(login_account)
    ], indirect=True)
class TestChangePwd:
    @staticmethod
    @allure.step('数据库验证密码修改情况')
    def review_pwd(db_conn, pwd):
        time.sleep(1)  # sql写入有延迟，要过一会再查
        with db_conn.cursor() as cursor:
            cursor.execute(f"select * "
                           f"from v_user "
                           f"where SCHOOL_NAME = '{login_account['school']}' and USER_ACCOUNT = '{login_account['user']}'")
            res = cursor.fetchone()
        assert res['USER_PASSWORD'] == pwd

    @pytest.mark.change_pwd
    @pytest.mark.parallel
    @pytest.mark.parametrize("datas", read_data_yaml('data/change_pwd.yaml'))
    def test_change_pwd(self, change_pwd_page, db_conn, datas):
        try:
            allure.dynamic.title(datas['title'])
            allure.dynamic.description('前置条件：\n1. 登录进入首页\n2. 右上角菜单，点击修改密码')
            change_pwd_page.input_old_pwd(datas['old'])
            change_pwd_page.input_new_pwd(datas['new'])
            change_pwd_page.input_confirm_pwd(datas['confirm'])
            change_pwd_page.click_confirm_btn()
            if datas['success']:
                self.review_pwd(db_conn, datas['new'])
            else:
                with allure.step('不修改密码，提示失败原因'):
                    assert change_pwd_page.get_el_alert_text() == datas['msg']
                    self.review_pwd(db_conn, login_account['pwd'])
        except Exception as e:
            screenshot(change_pwd_page.driver)
            raise e
        finally:
            change_pwd_page.close_if_open()
            with db_conn.cursor() as cursor:
                cursor.execute(f"UPDATE t_user "
                               f"SET USER_PASSWORD = '{login_account['pwd']}' "
                               f"WHERE USER_ACCOUNT = '{login_account['user']}'")
                db_conn.commit()

    @pytest.mark.change_pwd
    @pytest.mark.parallel
    @allure.title('点击返回-取消修改')
    def test_cancel(self, change_pwd_page, db_conn):
        try:
            allure.dynamic.description('前置条件：\n1. 登录进入首页\n2. 右上角菜单，点击修改密码')
            change_pwd_page.input_old_pwd('123')
            change_pwd_page.input_new_pwd('123456')
            change_pwd_page.input_confirm_pwd('123456')
            change_pwd_page.click_cancel_btn()
            self.review_pwd(db_conn, login_account['pwd'])
        except Exception as e:
            screenshot(change_pwd_page.driver)
            raise e

    @pytest.mark.change_pwd
    @pytest.mark.parallel
    @allure.title('点击外部空白-取消修改')
    def test_outside(self, change_pwd_page, db_conn):
        try:
            allure.dynamic.description('前置条件：\n1. 登录进入首页\n2. 右上角菜单，点击修改密码')
            change_pwd_page.input_old_pwd('123')
            change_pwd_page.input_new_pwd('123456')
            change_pwd_page.input_confirm_pwd('123456')
            change_pwd_page.click_outside_close()
            self.review_pwd(db_conn, login_account['pwd'])
        except Exception as e:
            screenshot(change_pwd_page.driver)
            raise e
