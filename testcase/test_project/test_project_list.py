import time
from common.utils import *

super_account = {
    "school": "东莞理工学院",
    "user": "10010",
    "pwd": "123",
    "role": "超管"
}

admin_account = {
    "school": "东莞理工学院",
    "user": "10020",
    "pwd": "123",
    "role": "学管"
}

teacher_account = {
    "school": "东莞理工学院",
    "user": "10030",
    "pwd": "123",
    "role": "教师"
}

student_account = {
    "school": "东莞理工学院",
    "user": "10042",
    "pwd": "123",
    "role": "学生"
}

review_account = {
    "school": "东莞理工学院",
    "user": "10011",
    "pwd": "123"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('项目管理')
@allure.story('查看项目')
@pytest.mark.parametrize("home_page", [
    pytest.param(super_account),
    pytest.param(admin_account),
    pytest.param(teacher_account),
    pytest.param(student_account)
], indirect=True)
class TestProjectList:
    @pytest.mark.project
    @pytest.mark.parallel
    @pytest.mark.parametrize("datas", ['个人项目', '结对编程', '团队项目'])
    def test_project_detail(self, home_page, datas, db_conn):
        try:
            role = home_page.param.get('role')
            allure.dynamic.title(f'{datas}-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击项目管理-{datas}')
            if datas == '个人项目':
                project_page = home_page.top_side_bar.switch_to_personal_project()
                project_page.verify_personal_page()
            elif datas == '结对编程':
                project_page = home_page.top_side_bar.switch_to_pair_programming()
                project_page.verify_pair_page()
            else:
                project_page = home_page.top_side_bar.switch_to_team_project()
                project_page.verify_team_page()
            with allure.step('获取第一个项目的信息'):
                name = project_page.get_project_name_by_index(0)
                with db_conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM t_project WHERE PROJECT_TITLE='{name}';")
                    res = cursor.fetchone()
                    db_conn.commit()
                u_id = res.get('USER_ID')
                with db_conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM v_user WHERE USER_ID='{u_id}';")
                    u = cursor.fetchone()
                    db_conn.commit()
                school = u.get('SCHOOL_NAME')
                teacher = u.get('USER_NAME')
            with allure.step('检查项目信息'):
                assert project_page.get_school_by_index(0) == school
                if datas == '个人项目' or datas == '结对编程':
                    assert project_page.get_difficulty_by_index(0) == res['PROJECT_DIFFICULTY']
                    assert project_page.get_use_times_by_index(0) == str(res['PROJECT_DOWNLOAD_TIMES'])
                else:
                    assert project_page.get_language_by_index(0) == res['PROJECT_LANGUAGE']
                    assert project_page.get_technology_by_index(0) == res['PROJECT_SKILLS']
            with allure.step('点击详情，检查项目信息'):
                detail_page = project_page.click_detail_btn_by_index(0)
                assert detail_page.get_project_name() == name
                assert detail_page.get_project_kind() == datas[:2]
                assert detail_page.get_teacher() == teacher
                assert detail_page.get_project_intro() == res['PROJECT_INTRO']
                assert detail_page.get_source_code_link() == res['PROJECT_LOCATION']
            detail_page.click_return_btn()
        except Exception as e:
            screenshot(home_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute('CALL reset_project();')
                db_conn.commit()


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('项目管理')
@allure.story('上传项目详情页')
@pytest.mark.parametrize("home_page", [
        pytest.param(super_account)
    ], indirect=True)
class TestProjectUploadPage:
    @pytest.mark.project
    @pytest.mark.parallel
    @pytest.mark.parametrize("datas", ['个人项目', '结对编程', '团队项目'])
    def test_upload_project_kind(self, home_page, datas):
        try:
            allure.dynamic.title(f'{datas}-项目类型')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-{datas}')
            if datas == '个人项目':
                project_page = home_page.top_side_bar.switch_to_personal_project()
                project_page.verify_personal_page()
            elif datas == '结对编程':
                project_page = home_page.top_side_bar.switch_to_pair_programming()
                project_page.verify_pair_page()
            else:
                project_page = home_page.top_side_bar.switch_to_team_project()
                project_page.verify_team_page()
            with allure.step('点击上传，查看项目类型'):
                upload_page = project_page.click_upload_btn()
                assert upload_page.get_project_kind() == datas[:2]
        except Exception as e:
            screenshot(home_page.driver)
            raise e

    @pytest.mark.project
    @pytest.mark.parallel
    @pytest.mark.parametrize("datas", ['个人项目', '结对编程', '团队项目'])
    def test_upload_confirm(self, home_page, datas):
        try:
            allure.dynamic.title(f'{datas}-确认上传')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-{datas}')
            if datas == '个人项目':
                project_page = home_page.top_side_bar.switch_to_personal_project()
                project_page.verify_personal_page()
            elif datas == '结对编程':
                project_page = home_page.top_side_bar.switch_to_pair_programming()
                project_page.verify_pair_page()
            else:
                project_page = home_page.top_side_bar.switch_to_team_project()
                project_page.verify_team_page()
            upload_page = project_page.click_upload_btn()
            with allure.step('输入信息，点击确认'):
                upload_page.input_project_name('测试点击确认')
                upload_page.click_confirm_btn()
            with allure.step('返回项目列表'):
                if datas == '个人项目':
                    project_page.verify_personal_page()
                elif datas == '结对编程':
                    project_page.verify_pair_page()
                else:
                    project_page.verify_team_page()
        except Exception as e:
            screenshot(home_page.driver)
            raise e

    @pytest.mark.project
    @pytest.mark.parallel
    @pytest.mark.parametrize("datas", ['个人项目', '结对编程', '团队项目'])
    def test_upload_alert_msg(self, home_page, datas):
        try:
            allure.dynamic.title(f'{datas}-确认上传提示')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-{datas}')
            if datas == '个人项目':
                project_page = home_page.top_side_bar.switch_to_personal_project()
                project_page.verify_personal_page()
            elif datas == '结对编程':
                project_page = home_page.top_side_bar.switch_to_pair_programming()
                project_page.verify_pair_page()
            else:
                project_page = home_page.top_side_bar.switch_to_team_project()
                project_page.verify_team_page()
            upload_page = project_page.click_upload_btn()
            with allure.step('输入信息，点击确认'):
                upload_page.input_project_name('测试点击确认')
                upload_page.click_confirm_btn()
            with allure.step('检查提示'):
                assert upload_page.get_el_alert_text() == '上传项目已成功发送请求，请耐心等待审核！'
        except Exception as e:
            screenshot(home_page.driver)
            raise e


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('项目管理')
@allure.story('删除项目弹窗')
@pytest.mark.parametrize("home_page", [
        pytest.param(super_account)
    ], indirect=True)
class TestProjectDeletePage:
    @pytest.mark.project
    @pytest.mark.parallel
    @pytest.mark.parametrize("datas", ['个人项目', '结对编程', '团队项目'])
    def test_delete_page(self, home_page, db_conn, datas):
        try:
            allure.dynamic.title(datas)
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-{datas}')
            if datas == '个人项目':
                project_page = home_page.top_side_bar.switch_to_personal_project()
                project_page.verify_personal_page()
            elif datas == '结对编程':
                project_page = home_page.top_side_bar.switch_to_pair_programming()
                project_page.verify_pair_page()
            else:
                project_page = home_page.top_side_bar.switch_to_team_project()
                project_page.verify_team_page()
            with allure.step('获取第一个项目信息'):
                title = project_page.get_project_name_by_index(0)
                with db_conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM t_project WHERE PROJECT_TITLE='{title}';")
                    res = cursor.fetchone()
                    db_conn.commit()
                u_id = res.get('USER_ID')
                with db_conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM v_user WHERE USER_ID='{u_id}';")
                    u = cursor.fetchone()
                    db_conn.commit()
                teacher = u.get('USER_NAME')
            with allure.step('删除第一个项目，查看信息'):
                del_page = project_page.click_delete_btn_by_index(0)
                assert del_page.get_project_name() == title
                assert del_page.get_upload_teacher() == teacher
                assert del_page.get_project_difficulty() == res.get('PROJECT_DIFFICULTY')
        except Exception as e:
            screenshot(home_page.driver)
            raise e
        finally:
            del_page.close_if_open()


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('项目管理')
class TestProjectEdit:
    @pytest.mark.project
    @pytest.mark.serial
    @allure.story('上传项目')
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
    @pytest.mark.parametrize("title", ['上传test', ''])
    @pytest.mark.parametrize("module", ['个人项目', '结对编程', '团队项目'])
    def test_project_upload(self, home_page_function, db_conn, module, title):
        try:
            param = home_page_function.param
            role = param.get('role')
            allure.dynamic.title(f'{module}-{role}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-{module}')
            if module == '个人项目':
                project_page = home_page_function.top_side_bar.switch_to_personal_project()
                project_page.verify_personal_page()
            elif module == '结对编程':
                project_page = home_page_function.top_side_bar.switch_to_pair_programming()
                project_page.verify_pair_page()
            else:
                project_page = home_page_function.top_side_bar.switch_to_team_project()
                project_page.verify_team_page()
            upload_page = project_page.click_upload_btn()
            with allure.step('输入信息，点击确认'):
                if title:
                    upload_page.input_project_name(module + title)
                if module == '个人项目':
                    upload_page.click_easy_btn()
                elif module == '结对编程':
                    upload_page.click_mid_btn()
                else:
                    upload_page.click_difficult_btn()
                upload_page.input_project_intro('test xxx')
                upload_page.click_confirm_btn()
            with allure.step('登录超管账号，检查请求记录'):
                bar = home_page_function.top_side_bar
                login_page = bar.click_menu_logout()
                login_page.login(review_account['school'], review_account['user'], review_account['pwd'])
                review_page = bar.switch_to_project_review()
                review_page.switch_to_last_page()
            if title == '':
                with allure.step('验证项目名为空没有请求记录'):
                    assert review_page.get_project_name_by_index(-1) != ''
                return
            with allure.step('检查最后一条请求的信息'):
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                    res = cursor.fetchone()
                user_name = res.get('USER_NAME')
                assert review_page.get_request_kind_by_index(-1) == '添加'
                assert review_page.get_project_kind_by_index(-1) == module[:2]
                assert review_page.get_project_name_by_index(-1) == module + title
                assert review_page.get_publisher_by_index(-1) == user_name
                assert review_page.get_status_by_index(-1) == '未审核'
                review_detail = review_page.click_detail_btn_by_index(-1)
                assert review_detail.get_project_intro() == 'test xxx'
        except Exception as e:
            screenshot(home_page_function.driver)
            raise e

    @pytest.mark.project
    @pytest.mark.serial
    @allure.story('上传项目')
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account)
    ], indirect=True)
    @pytest.mark.parametrize("module", ['个人项目', '结对编程', '团队项目'])
    def test_project_cancel_upload(self, home_page_function, module):
        try:
            allure.dynamic.title(f'{module}-取消上传')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-{module}')
            if module == '个人项目':
                project_page = home_page_function.top_side_bar.switch_to_personal_project()
                project_page.verify_personal_page()
            elif module == '结对编程':
                project_page = home_page_function.top_side_bar.switch_to_pair_programming()
                project_page.verify_pair_page()
            else:
                project_page = home_page_function.top_side_bar.switch_to_team_project()
                project_page.verify_team_page()
            upload_page = project_page.click_upload_btn()
            with allure.step('输入信息，点击返回'):
                upload_page.input_project_name(f'{module}取消上传')
                upload_page.click_easy_btn()
                upload_page.click_return_btn()
            with allure.step('检查请求记录'):
                review_page = home_page_function.top_side_bar.switch_to_project_review()
                review_page.switch_to_last_page()
                assert review_page.get_project_name_by_index(-1) != f'{module}取消上传'
        except Exception as e:
            screenshot(home_page_function.driver)
            raise e

    @pytest.mark.project
    @pytest.mark.serial
    @allure.story('删除项目')
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
    @pytest.mark.parametrize("module", ['个人项目', '结对编程', '团队项目'])
    def test_project_delete(self, home_page_function, db_conn, module):
        try:
            param = home_page_function.param
            role = param.get('role')
            allure.dynamic.title(f'{module}-{role}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-{module}')
            with allure.step('数据库添加一条记录'):
                title = f'{module}删除test'
                dif = '简单'
                kind = module[:2]
                with db_conn.cursor() as cursor:
                    cursor.execute(f"CALL add_project('{param['user']}', '{title}', '{dif}', '{kind}');")
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}';")
                    res = cursor.fetchone()
                    db_conn.commit()
                user_name = res.get('USER_NAME')
            with allure.step('删除刚添加的记录'):
                if module == '个人项目':
                    project_page = home_page_function.top_side_bar.switch_to_personal_project()
                    project_page.verify_personal_page()
                elif module == '结对编程':
                    project_page = home_page_function.top_side_bar.switch_to_pair_programming()
                    project_page.verify_pair_page()
                else:
                    project_page = home_page_function.top_side_bar.switch_to_team_project()
                    project_page.verify_team_page()
                del_page = project_page.click_delete_btn_by_index(-1)
                del_page.click_delete_btn()
                assert del_page.get_el_alert_text() == '删除请求已成功发送，请耐心等待审核！'
            with allure.step('登录超管账号，检查请求记录'):
                bar = home_page_function.top_side_bar
                login_page = bar.click_menu_logout()
                login_page.login(review_account['school'], review_account['user'], review_account['pwd'])
                review_page = bar.switch_to_project_review()
                review_page.switch_to_last_page()
            with allure.step('检查最后一条请求的信息'):
                assert review_page.get_request_kind_by_index(-1) == '删除'
                assert review_page.get_project_kind_by_index(-1) == kind
                assert review_page.get_project_name_by_index(-1) == title
                assert review_page.get_publisher_by_index(-1) == user_name
                assert review_page.get_status_by_index(-1) == '未审核'
        except Exception as e:
            screenshot(home_page_function.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute('CALL reset_project();')
                db_conn.commit()

    @pytest.mark.project
    @pytest.mark.serial
    @allure.story('删除项目')
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account)
    ], indirect=True)
    @pytest.mark.parametrize("module", ['个人项目', '结对编程', '团队项目'])
    def test_project_cancel_delete(self, home_page_function, module):
        try:
            allure.dynamic.title(f'{module}-取消删除')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-{module}')
            if module == '个人项目':
                project_page = home_page_function.top_side_bar.switch_to_personal_project()
                project_page.verify_personal_page()
            elif module == '结对编程':
                project_page = home_page_function.top_side_bar.switch_to_pair_programming()
                project_page.verify_pair_page()
            else:
                project_page = home_page_function.top_side_bar.switch_to_team_project()
                project_page.verify_team_page()
            with allure.step('删除第一个项目，点击返回'):
                title = project_page.get_project_name_by_index(0)
                project_page.click_delete_btn_by_index(0).click_return_btn()
            with allure.step('检查请求记录'):
                review_page = home_page_function.top_side_bar.switch_to_project_review()
                review_page.switch_to_last_page()
                assert review_page.get_project_name_by_index(-1) != title or review_page.get_request_kind_by_index(-1) != '删除'
        except Exception as e:
            screenshot(home_page_function.driver)
            raise e

