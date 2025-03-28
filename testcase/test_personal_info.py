from page.top_side_bar import TopSideBar
from common.utils import *


login_account = {
    "school": "东莞理工学院",
    "user": "10040",
    "pwd": "123"
}


# 首页上方菜单-个人信息弹窗
@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('首页上方菜单-个人信息弹窗')
@pytest.mark.parametrize("home_page", [
        pytest.param(login_account)
    ], indirect=True)
class TestPersonalInfo:
    # 只检查性别、手机、邮箱的修改情况
    @staticmethod
    @allure.step('再次打开弹窗，校验数据修改情况')
    def review_edit(bar, db_conn, sex, tel, email):
        p = bar.click_menu_personal_info()
        assert p.get_user_sex() == sex
        assert p.get_user_tel() == tel
        assert p.get_user_email() == email
        if sql_check:
            with allure.step('数据库校验'):
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * "
                                   f"from v_user "
                                   f"where school_name = '{login_account['school']}' "
                                   f"AND user_account = '{login_account['user']}'")
                    res = cursor.fetchone()
                assert res['USER_SEX'] == sex
                assert res['USER_TEL'] == tel
                assert res['USER_EMAIL'] == email

    @pytest.mark.personal_info
    @pytest.mark.parallel
    @allure.title('校验个人信息')
    def test_review_info(self, personal_info_page, db_conn):
        try:
            allure.dynamic.description('前置条件：\n1. 登录进入首页\n2. 右上角菜单，点击个人信息')
            assert personal_info_page.get_user_account() == login_account['user']
            assert personal_info_page.get_school_name() == login_account['school']
            if sql_check:
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * "
                                   f"from v_user "
                                   f"where school_name = '{login_account['school']}' "
                                   f"AND user_account = '{login_account['user']}'")
                    res = cursor.fetchone()
                assert personal_info_page.get_user_name() == res['USER_NAME']
                assert personal_info_page.get_user_sex() == res['USER_SEX']
                assert personal_info_page.get_user_tel() == res['USER_TEL']
                assert personal_info_page.get_user_email() == res['USER_EMAIL']
                assert personal_info_page.get_role_name() == res['ROLE_NAME']
        except Exception as e:
            screenshot(personal_info_page.driver)
            raise e
        finally:
            personal_info_page.close_if_open()

    @pytest.mark.personal_info
    @pytest.mark.parallel
    @allure.title('取消修改')
    def test_cancel_edit(self, personal_info_page, db_conn):
        try:
            allure.dynamic.description('前置条件：\n1. 登录进入首页\n2. 右上角菜单，点击个人信息')
            with allure.step('获取原始数据'):
                sex = personal_info_page.get_user_sex()
                tel = personal_info_page.get_user_tel()
                email = personal_info_page.get_user_email()
            with allure.step('修改性别、电话、邮箱'):
                personal_info_page.input_user_sex('男')
                personal_info_page.input_user_tel('123')
                personal_info_page.input_user_email('123@qq.com')
            personal_info_page.click_outside_close()
            bar = TopSideBar(personal_info_page.driver)
            self.review_edit(bar, db_conn, sex, tel, email)
        except Exception as e:
            screenshot(personal_info_page.driver)
            raise e
        finally:
            personal_info_page.close_if_open()

    @pytest.mark.personal_info
    @pytest.mark.parallel
    @pytest.mark.parametrize("datas", read_data_yaml('data/personal_info.yaml'))
    def test_edit_info(self, personal_info_page, db_conn, datas):
        try:
            allure.dynamic.title(datas['title'])
            allure.dynamic.description('前置条件：\n1. 登录进入首页\n2. 右上角菜单，点击个人信息')
            with allure.step('获取原始数据'):
                sex = personal_info_page.get_user_sex()
                tel = personal_info_page.get_user_tel()
                email = personal_info_page.get_user_email()
            with allure.step('修改数据'):
                if datas.get('sex') is not None:
                    sex = datas.get('sex')
                    personal_info_page.input_user_sex(sex)
                if datas.get('tel') is not None:
                    tel = datas.get('tel')
                    personal_info_page.input_user_tel(tel)
                if datas.get('email') is not None:
                    email = datas.get('email')
                    personal_info_page.input_user_email(email)
                personal_info_page.click_save_btn()
                bar = TopSideBar(personal_info_page.driver)
            if datas.get('success'):
                with allure.step('修改数据，提示修改成功'):
                    assert personal_info_page.get_el_alert_text() == '个人信息修改成功！'
            else:
                with allure.step(f'不修改数据，提示"{datas.get("error")}"'):
                    assert personal_info_page.get_el_alert_text() == datas.get('error')
            self.review_edit(bar, db_conn, sex, tel, email)
        except Exception as e:
            screenshot(personal_info_page.driver)
            raise e
        finally:
            personal_info_page.close_if_open()
