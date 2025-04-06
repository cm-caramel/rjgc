import time
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
class TestClass:
    @pytest.mark.course
    @pytest.mark.parallel
    @allure.story('检查行政班')
    def test_class_check(self, request, course_page, db_conn):
        try:
            param = request.getfixturevalue('home_page').param
            role = param.get('role')
            allure.dynamic.title(role)
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击课程管理')
            course_page.verify_page()
            with allure.step('选最后一门课程，添加班级'):
                detail_page = course_page.click_course_by_index(-1)
                add_class_page = detail_page.click_class_add_btn()
                add_class_page.click_class_select()
            with allure.step('检查行政班列表'):
                with db_conn.cursor() as cursor:
                    cursor.execute(f"SELECT DISTINCT USER_CLASS "
                                   f"FROM v_user "
                                   f"WHERE SCHOOL_NAME = '{param.get('school')}' AND USER_CLASS IS NOT NULL;")
                    res = cursor.fetchall()
                arr = []
                for item in res:
                    arr.append(item['USER_CLASS'])
                assert add_class_page.get_all_classes() == arr
        except Exception as e:
            screenshot(course_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("CALL reset_class();")
                db_conn.commit()


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('课程管理')
@pytest.mark.parametrize("home_page", [
    pytest.param(admin_account),
    pytest.param(teacher_account)
], indirect=True)
class TestClass:
    @pytest.mark.course
    @pytest.mark.serial
    @allure.story('班级添加')
    @pytest.mark.parametrize("datas", read_data_yaml('data/teach_class.yaml'))
    def test_class_add(self, request, course_page, db_conn, datas):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'{datas["title"]}-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击课程管理')
            course_page.verify_page()
            with allure.step('选第一门课程，添加班级'):
                detail_page = course_page.click_course_by_index(0)
                add_class_page = detail_page.click_class_add_btn()
                if datas.get('teach_class') > 0:
                    add_class_page.click_class_select()
                    for i in range(datas.get('teach_class')):
                        add_class_page.select_class_by_index(i)
                    add_class_page.click_class_select()
                add_class_page.input_class_name(datas.get('name'))
                if datas.get('cancel'):
                    add_class_page.click_return_btn()
                else:
                    add_class_page.click_confirm_btn()
                    time.sleep(1)
            with allure.step('校验添加结果'):
                if not datas.get('success'):
                    assert detail_page.get_class_name_by_index(-1) != datas.get('name')
                else:
                    assert detail_page.get_class_name_by_index(-1) == datas.get('name')
        except Exception as e:
            screenshot(course_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("CALL reset_class();")
                db_conn.commit()

    @pytest.mark.course
    @pytest.mark.serial
    @allure.story('班级删除')
    @pytest.mark.parametrize("datas", ['确认', '取消'])
    def test_class_delete(self, request, course_page, db_conn, datas):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'{role}-删除班级{datas}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击课程管理')
            course_page.verify_page()
            with allure.step('选第一门课程，添加一个班级'):
                course = course_page.get_course_name_by_index(0)
                class_name = f'删除课程{datas}'
                detail_page = course_page.click_course_by_index(0)
                add_class_page = detail_page.click_class_add_btn()
                add_class_page.input_class_name(class_name)
                add_class_page.click_confirm_btn()
                time.sleep(1)
            with allure.step('删除该班级'):
                assert detail_page.get_class_name_by_index(-1) == class_name
                del_page = detail_page.click_class_delete_by_index(-1)
                assert del_page.get_class_course_name() == course
                assert del_page.get_class_name() == class_name
                if datas == '确认':
                    del_page.click_delete_btn()
                    time.sleep(1)
                elif datas == '取消':
                    del_page.click_return_btn()
            with allure.step('校验删除结果'):
                if datas == '确认':
                    assert detail_page.get_class_name_by_index(-1) != class_name
                elif datas == '取消':
                    assert detail_page.get_class_name_by_index(-1) == class_name
        except Exception as e:
            screenshot(course_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("CALL reset_class();")
                db_conn.commit()

    @pytest.mark.course
    @pytest.mark.serial
    @allure.story('班级人员编辑')
    def test_student_add(self, request, course_page, db_conn):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'{role}-添加学生')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击课程管理')
            course_page.verify_page()
            with allure.step('选最后一门课程，添加一个班级'):
                detail_page = course_page.click_course_by_index(-1)
                add_class_page = detail_page.click_class_add_btn()
                add_class_page.input_class_name('班级人员编辑test')
                add_class_page.click_confirm_btn()
                time.sleep(1)
            with allure.step('编辑班级人员'):
                class_detail = detail_page.click_class_detail_by_index(-1)
                import_page = class_detail.click_import_btn()
            with allure.step('添加第一个学生'):
                name = import_page.get_name_by_index(0)
                account = import_page.get_account_by_index(0)
                _class = import_page.get_class_by_index(0)
                assert import_page.is_add_btn_visible_by_index(0)
                import_page.click_add_btn_by_index(0)
                assert import_page.get_el_alert_text() == '学生添加成功！'
                assert not import_page.is_add_btn_visible_by_index(0)
                import_page.click_return_btn()
            with allure.step('检查添加结果'):
                assert class_detail.get_name_by_index(-1) == name
                assert class_detail.get_account_by_index(-1) == account
                assert class_detail.get_class_by_index(-1) == _class
        except Exception as e:
            screenshot(course_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("CALL reset_class();")
                db_conn.commit()

    @pytest.mark.course
    @pytest.mark.serial
    @allure.story('班级人员编辑')
    @pytest.mark.parametrize("datas", ['确认', '取消'])
    def test_student_delete(self, request, course_page, db_conn, datas):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'{role}-删除学生{datas}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击课程管理')
            course_page.verify_page()
            with allure.step('选最后一门课程，添加一个班级'):
                detail_page = course_page.click_course_by_index(-1)
                add_class_page = detail_page.click_class_add_btn()
                add_class_page.click_class_select()
                add_class_page.select_class_by_index(0)
                add_class_page.click_class_select()
                add_class_page.input_class_name('班级人员编辑test')
                add_class_page.click_confirm_btn()
                time.sleep(1)
            with allure.step('删除第一个学生'):
                class_detail = detail_page.click_class_detail_by_index(-1)
                name = class_detail.get_name_by_index(0)
                del_page = class_detail.click_delete_btn_by_index(0)
                if datas == '确认':
                    del_page.click_delete_btn()
                    assert del_page.get_el_alert_text() == '学生删除成功！'
                elif datas == '取消':
                    del_page.click_return_btn()
            with allure.step('校验删除结果'):
                if datas == '取消':
                    assert class_detail.get_name_by_index(0) == name
                    return
                assert class_detail.get_name_by_index(0) != name
                import_page = class_detail.click_import_btn()
                assert import_page.is_add_btn_visible_by_index(0)
                import_page.click_return_btn()
        except Exception as e:
            screenshot(course_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("CALL reset_class();")
                db_conn.commit()




