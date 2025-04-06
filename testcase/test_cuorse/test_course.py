from common.utils import *

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


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('课程管理')
@pytest.mark.parametrize("home_page", [
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
class TestCourse:
    @pytest.mark.course
    @pytest.mark.serial
    @allure.story('课程添加')
    @pytest.mark.parametrize("datas", read_data_yaml('data/course.yaml'))
    def test_course_add(self, request, course_page, db_conn, datas):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'{datas["title"]}-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击课程管理')
            assert course_page.verify_page()
            add_page = course_page.click_add_course_btn()
            with allure.step('输入信息'):
                add_page.input_course_name(datas.get('name'))
                add_page.input_course_time(datas.get('time'))
                add_page.input_course_info(datas.get('info'))
            if datas.get('cancel'):
                add_page.click_exit_edit_btn()
            else:
                add_page.click_confirm_btn()
                assert course_page.get_el_alert_text() == '课程新建成功！'
            with allure.step('校验添加结果'):
                if not datas.get('success'):
                    name = datas.get('name') if datas.get('name') else ''
                    assert course_page.get_course_name_by_index(-1) != name
                    return
                assert course_page.get_course_name_by_index(-1) == datas.get('name')
                assert course_page.get_course_time_by_index(-1) == datas.get('time')
                detail_page = course_page.click_course_by_index(-1)
                detail_page.click_course_detail_tab()
                assert detail_page.get_course_name() == datas.get('name')
                assert detail_page.get_course_time() == datas.get('time')
                if datas.get('info'):
                    assert detail_page.get_course_info() == datas.get('info')
            detail_page.click_return_btn()
            assert course_page.verify_page()
        except Exception as e:
            screenshot(course_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("CALL reset_course();")
                db_conn.commit()

    @pytest.mark.course
    @pytest.mark.serial
    @allure.story('课程删除')
    @pytest.mark.parametrize("datas", ['确认', '取消'])
    def test_course_delete(self, request, course_page, db_conn, datas):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'{role}-删除课程{datas}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击课程管理')
            assert course_page.verify_page()
            with allure.step('添加一门课程'):
                name = f'删除课程{datas}'
                t = '删除课程的时间'
                add_page = course_page.click_add_course_btn()
                add_page.input_course_name(name)
                add_page.input_course_time(t)
                add_page.click_confirm_btn()
                assert course_page.get_course_name_by_index(-1) == name
            with allure.step('删除刚添加的课程'):
                detail_page = course_page.click_course_by_index(-1)
                del_page = detail_page.click_delete_btn()
                assert del_page.get_course_name() == name
                assert del_page.get_course_time() == t
                if datas == '确认':
                    del_page.click_delete_btn()
                    assert course_page.get_el_alert_text() == '课程删除成功！'
                elif datas == '取消':
                    del_page.click_return_btn()
                    detail_page.click_return_btn()
                assert course_page.verify_page()
            with allure.step('校验删除结果'):
                if datas == '确认':
                    assert course_page.get_course_name_by_index(-1) != name
                elif datas == '取消':
                    assert course_page.get_course_name_by_index(-1) == name
        except Exception as e:
            screenshot(course_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("CALL reset_course();")
                db_conn.commit()

    @pytest.mark.course
    @pytest.mark.serial
    @allure.story('课程修改')
    @pytest.mark.parametrize("datas", ['确认', '取消'])
    def test_course_edit(self, request, course_page, db_conn, datas):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'{role}-修改课程信息{datas}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击课程管理')
            assert course_page.verify_page()
            with allure.step('添加一门课程'):
                name = f'修改课程{datas}'
                t = '修改课程的时间'
                add_page = course_page.click_add_course_btn()
                add_page.input_course_name(name)
                add_page.input_course_time(t)
                add_page.click_confirm_btn()
                assert course_page.get_course_name_by_index(-1) == name
            with allure.step('修改刚添加的课程'):
                detail_page = course_page.click_course_by_index(-1)
                detail_page.click_course_detail_tab()
                name2 = '修改后的课程名称'
                t2 = '修改后的课程时间'
                detail_page.input_course_name(name2)
                detail_page.input_course_time(t2)
                if datas == '确认':
                    detail_page.click_course_confirm_btn()
                    assert detail_page.get_el_alert_text() == '修改成功！'
            with allure.step('校验修改结果'):
                detail_page.click_return_btn()
                assert course_page.verify_page()
                if datas == '确认':
                    assert course_page.get_course_name_by_index(-1) == name2
                    assert course_page.get_course_time_by_index(-1) == t2
                elif datas == '取消':
                    assert course_page.get_course_name_by_index(-1) == name
                    assert course_page.get_course_time_by_index(-1) == t
        except Exception as e:
            screenshot(course_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("CALL reset_course();")
                db_conn.commit()

