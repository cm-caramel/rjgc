from common.utils import *

teacher_account = {
    "school": "东莞理工学院",
    "user": "10030",
    "pwd": "123",
    "role": "教师"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('用户管理')
@allure.story('教师')
@pytest.mark.parametrize("home_page", [
        pytest.param(teacher_account)
    ], indirect=True)
class TestUserManagementAdmin:
    @staticmethod
    def add_user(db_conn, name, account, school, role, classes):
        with db_conn.cursor() as cursor:
            cursor.execute(f"call add_user('{name}', '{school}', '{account}', '{role}', '{classes}')")
            cursor.execute(f"select * from v_user "
                           f"where USER_ACCOUNT = '{account}' and USER_NAME = '{name}' "
                           f"and SCHOOL_NAME = '{school}' and ROLE_NAME = '{role}'")
            res = cursor.fetchone()
            db_conn.commit()
        new_id = res.get('USER_ID')
        return new_id

    @pytest.mark.user_management
    @pytest.mark.parallel
    @allure.title('查看详情')
    def test_detail_page(self, user_page, db_conn):
        try:
            allure.dynamic.description(f'前置条件：\n1. 教师登录后点击教材管理-学生管理')
            with allure.step('获取表格第一条记录信息'):
                name = user_page.get_name_by_index(0)
                account = user_page.get_account_by_index(0)
            with allure.step('点击详情'):
                detail_page = user_page.click_detail_btn_by_index(0)
            with allure.step('查看详情信息'):
                assert detail_page.get_user_name() == name
                assert detail_page.get_user_account() == account
                assert detail_page.get_school_name() == teacher_account.get('school')
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{teacher_account.get('school')}' AND USER_ACCOUNT = '{account}'")
                    res = cursor.fetchone()
                sex = res.get('USER_SEX') if res.get('USER_SEX') else ''
                tel = res.get('USER_TEL') if res.get('USER_TEL') else ''
                email = res.get('USER_EMAIL') if res.get('USER_EMAIL') else ''
                assert detail_page.get_user_sex() == sex
                assert detail_page.get_user_tel() == tel
                assert detail_page.get_user_email() == email
        except Exception as e:
            screenshot(user_page.driver)
            raise e
        finally:
            detail_page.close_if_open()

    @pytest.mark.user_management
    @pytest.mark.serial
    @pytest.mark.parametrize("datas", ['确认', '返回'])
    def test_update_detail(self, user_page, db_conn, datas):
        try:
            allure.dynamic.description(f'前置条件：\n1. 教师登录后点击教材管理-学生管理')
            allure.dynamic.title(f'查看详情-修改{datas}')
            with allure.step('数据库新建用户'):
                name = 'detail'
                account = 'update'
                school = '东莞理工学院'
                role = '学生'
                classes = '软件4班'
                new_id = self.add_user(db_conn, name, account, school, role, classes)
            with allure.step('点击详情'):
                user_page.driver.refresh()
                user_page.top_side_bar.switch_to_student_management()
                user_page.switch_to_last_page()
                assert user_page.get_name_by_index(-1) == name
                detail_page = user_page.click_detail_btn_by_index(-1)
            with allure.step('修改'):
                update_name = f'{name}1'
                update_account = f'{account}1'
                update_tel = '1234'
                update_email = '1234@example.com'
                detail_page.input_user_name(update_name)
                detail_page.input_user_account(update_account)
                detail_page.input_user_sex_male()
                detail_page.input_user_tel(update_tel)
                detail_page.input_user_email(update_email)
            if datas == '确认':
                detail_page.click_confirm_btn()
                assert detail_page.get_el_alert_text() == '用户信息修改成功'
            elif datas == '返回':
                detail_page.click_return_btn()
            with allure.step('查看修改结果'):
                user_page.driver.refresh()
                user_page.top_side_bar.switch_to_student_management()
                user_page.switch_to_last_page()
                if datas == '确认':
                    assert user_page.get_name_by_index(-1) == update_name
                    assert user_page.get_account_by_index(-1) == update_account
                    user_page.click_detail_btn_by_index(-1)
                    assert detail_page.get_user_sex() == '男'
                    assert detail_page.get_user_tel() == update_tel
                    assert detail_page.get_user_email() == update_email
                elif datas == '返回':
                    assert user_page.get_name_by_index(-1) == name
                    assert user_page.get_account_by_index(-1) == account
                    user_page.click_detail_btn_by_index(-1)
                    assert detail_page.get_user_sex() == ''
                    assert detail_page.get_user_tel() == ''
                    assert detail_page.get_user_email() == ''
        except Exception as e:
            screenshot(user_page.driver)
            raise e
        finally:
            detail_page.close_if_open()
            with db_conn.cursor() as cursor:
                cursor.execute(f"delete from t_user where USER_ID = {new_id}")
                db_conn.commit()

    @pytest.mark.user_management
    @pytest.mark.serial
    @allure.title('查看详情-重置密码')
    def test_reset_pwd(self, user_page, db_conn):
        try:
            allure.dynamic.description(f'前置条件：\n1. 教师登录后点击教材管理-学生管理')
            with allure.step('数据库新建用户'):
                name = 'detail'
                account = 'update'
                school = '东莞理工学院'
                role = '学生'
                classes = '软件4班'
                new_id = self.add_user(db_conn, name, account, school, role, classes)
            with allure.step('点击详情'):
                user_page.driver.refresh()
                user_page.top_side_bar.switch_to_student_management()
                user_page.switch_to_last_page()
                assert user_page.get_name_by_index(-1) == name
                detail_page = user_page.click_detail_btn_by_index(-1)
            detail_page.click_reset_pwd_btn()
            assert detail_page.get_el_alert_text() == '该用户的密码已经被重置'
            with allure.step('数据库查看修改结果'):
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user where USER_ID = {new_id}")
                    res = cursor.fetchone()
                    db_conn.commit()
                assert res.get('USER_PASSWORD') == '123456'
        except Exception as e:
            screenshot(user_page.driver)
            raise e
        finally:
            detail_page.close_if_open()
            with db_conn.cursor() as cursor:
                cursor.execute(f"delete from t_user where USER_ID = {new_id}")
                db_conn.commit()

    @pytest.mark.user_management
    @pytest.mark.serial
    @allure.title('查看详情-删除用户')
    @pytest.mark.parametrize("datas", ['删除', '返回'])
    def test_delete_user(self, user_page, db_conn, datas):
        try:
            allure.dynamic.description(f'前置条件：\n1. 教师登录后点击教材管理-学生管理')
            with allure.step('数据库新建用户'):
                name = 'detail'
                account = 'update'
                school = '东莞理工学院'
                role = '学生'
                classes = '软件4班'
                new_id = self.add_user(db_conn, name, account, school, role, classes)
            with allure.step('点击删除'):
                user_page.driver.refresh()
                user_page.top_side_bar.switch_to_student_management()
                user_page.switch_to_last_page()
                assert user_page.get_name_by_index(-1) == name
                del_page = user_page.click_delete_btn_by_index(-1)
            if datas == '删除':
                del_page.click_delete_btn()
                assert del_page.get_el_alert_text() == '用户删除成功'
            elif datas == '返回':
                del_page.click_return_btn()
            with allure.step('数据库查看修改结果'):
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user where USER_ID = {new_id}")
                    res = cursor.fetchone()
                    db_conn.commit()
                if datas == '删除':
                    assert res is None
                elif datas == '返回':
                    assert res is not None
        except Exception as e:
            screenshot(user_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute(f"delete from t_user where USER_ID = {new_id}")
                db_conn.commit()
