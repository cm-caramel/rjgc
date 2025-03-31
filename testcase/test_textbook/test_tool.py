import time

import allure

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
@allure.feature('工具管理')
@allure.story('查看工具')
@pytest.mark.parametrize("home_page", [
    pytest.param(super_account),
    pytest.param(admin_account),
    pytest.param(teacher_account),
    pytest.param(student_account)
], indirect=True)
class TestToolDetail:
    @pytest.mark.tool
    @pytest.mark.parallel
    def test_read_tool(self, request, tool_page, db_conn):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'查看工具-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-工具列表')
            assert tool_page.verify_page()
            with allure.step('点击第一个工具，进入详情页'):
                tools = tool_page.get_all_tool()
                detail_page = tool_page.click_tool_by_index(0)
                assert detail_page.get_tool_title() == tools[0]
            with allure.step('点击工具链接'):
                detail_page.click_tool_link()
                old = detail_page.driver.current_window_handle
                new = [window for window in detail_page.driver.window_handles if window != old][0]
                detail_page.driver.switch_to.window(new)
                detail_page.driver.close()
                detail_page.driver.switch_to.window(old)
            with allure.step('切换工具'):
                for i in range(1, len(detail_page.title_lists)):
                    detail_page.click_catalog_by_index(i)
                    assert detail_page.get_tool_title() == detail_page.title_lists[i]
            with allure.step('点击返回按钮'):
                detail_page.click_return_btn()
                assert tool_page.verify_page()
        except Exception as e:
            screenshot(tool_page.driver)
            raise e


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('工具管理')
@allure.story('工具评论')
class TestDiscuss:
    @pytest.mark.tool
    @pytest.mark.parallel
    @allure.title('查看评论')
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account)
    ], indirect=True)
    def test_read_discuss(self, tool_page_function, db_conn):
        try:
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            detail_page = tool_page_function.click_tool_by_index(0)
            with allure.step('点击右侧目录切换工具'):
                detail_page.click_catalog_by_index(1)
            with allure.step('检查切换后的评论信息'):
                assert detail_page.get_all_discuss_info() == []
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("call discuss();")
                db_conn.commit()

    @pytest.mark.tool
    @pytest.mark.parallel
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account),
        pytest.param(student_account)
    ], indirect=True)
    def test_discuss_add(self, request, tool_page_function, db_conn):
        try:
            param = request.getfixturevalue('home_page_function').param
            role = param.get('role')
            allure.dynamic.title(f'新建评论-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            detail_page = tool_page_function.click_tool_by_index(0)
            with db_conn.cursor() as cursor:
                cursor.execute(f"select * from v_user "
                               f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                res = cursor.fetchone()
            user_name = res.get('USER_NAME')
            content = f'{role}新评论'
            with allure.step('发表评论，取消'):
                detail_page.click_discuss_add_btn()
                detail_page.input_discuss_content(content)
                detail_page.click_discuss_cancel_btn()
                assert not detail_page.has_this_discuss(user_name, content)
            with allure.step('发表评论，确定'):
                detail_page.click_discuss_add_btn()
                detail_page.input_discuss_content(content)
                detail_page.click_discuss_publish_btn()
                assert detail_page.has_this_discuss(user_name, content)
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("call discuss();")
                db_conn.commit()

    @pytest.mark.tool
    @pytest.mark.parallel
    @allure.title('评论排序')
    @pytest.mark.tool
    @pytest.mark.parallel
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account)
    ], indirect=True)
    def test_discuss_sort(self, tool_page_function, db_conn):
        try:
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            detail_page = tool_page_function.click_tool_by_index(0)
            with allure.step('获取排序前的第一条评论'):
                first_discuss = detail_page.get_all_discuss_info()[0]
                first_user = first_discuss['user']
                first_content = first_discuss['content']
            with allure.step('点击评论排序按钮'):
                detail_page.click_discuss_sort_btn()
            with allure.step('获取排序后的第一条评论'):
                res = detail_page.get_all_discuss_info()[0]
                assert res['content'] != first_content and res['user'] != first_user
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("call discuss();")
                db_conn.commit()

    @pytest.mark.tool
    @pytest.mark.serial
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account),
        pytest.param(student_account)
    ], indirect=True)
    def test_discuss_like(self, request, tool_page_function, db_conn):
        try:
            param = request.getfixturevalue('home_page_function').param
            role = param.get('role')
            allure.dynamic.title(f'点赞评论-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            detail_page = tool_page_function.click_tool_by_index(0)
            with allure.step('获取第一条评论信息'):
                first_discuss = detail_page.get_all_discuss_info()[0]
                first_content = first_discuss['content']
            with allure.step('点赞第一条评论'):
                detail_page.click_discuss_like_btn(0)
                assert detail_page.get_all_discuss_info()[0].get('like_cnt') == '1'
            with allure.step('数据库验证'):
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from t_tool_comment where TOOL_COMMENT_CONTENT = '{first_content}'")
                    res = cursor.fetchone()
                    db_conn.commit()
                assert res.get('TOOL_COMMENT_GOOD') == 1
            with allure.step('取消点赞'):
                detail_page.click_discuss_like_btn(0)
                assert detail_page.get_all_discuss_info()[0].get('like_cnt') == '0'
            with allure.step('数据库验证'):
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from t_tool_comment where TOOL_COMMENT_CONTENT = '{first_content}'")
                    res = cursor.fetchone()
                    db_conn.commit()
                assert res.get('TOOL_COMMENT_GOOD') == 0
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("call discuss();")
                db_conn.commit()

    @pytest.mark.tool
    @pytest.mark.serial
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account),
        pytest.param(student_account)
    ], indirect=True)
    def test_discuss_delete(self, request, tool_page_function, db_conn):
        try:
            param = request.getfixturevalue('home_page_function').param
            role = param.get('role')
            allure.dynamic.title(f'删除评论-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            detail_page = tool_page_function.click_tool_by_index(0)
            with db_conn.cursor() as cursor:
                cursor.execute(f"select * from v_user "
                               f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                res = cursor.fetchone()
            user_name = res.get('USER_NAME')
            with allure.step('检查删除按钮显示'):
                infos = detail_page.get_all_discuss_info()
                cnt = len(infos)
                print(infos)
                print(f'======== {cnt}')
                if role == '超管' or role == '学管':
                    for info in infos:
                        assert info.get('has_del_btn')
                else:
                    for info in infos:
                        if info.get('user') == user_name:
                            assert info.get('has_del_btn')
                        else:
                            assert not info.get('has_del_btn')
            if infos[0].get('has_del_btn'):
                with allure.step('删除第一条评论'):
                    detail_page.click_discuss_del_btn(0)
                    assert detail_page.get_el_alert_text() == '评论删除成功'
                    assert len(detail_page.get_all_discuss_info()) == cnt - 1
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute("call discuss();")
                db_conn.commit()


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('工具管理')
@allure.story('新增分类')
class TestToolAdd:
    @pytest.mark.tool
    @pytest.mark.serial
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
    def test_tool_add(self, request, tool_page_function, db_conn):
        try:
            param = request.getfixturevalue('home_page_function').param
            role = param.get('role')
            allure.dynamic.title(f'新增分类-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            with allure.step('新增分类'):
                edit_mode = tool_page_function.click_edit_mode()
                add_page = edit_mode.click_add_kind()
                add_page.input_kind_name('新增分类test')
            with allure.step('点击确认'):
                add_page.click_confirm_btn()
                try:
                    assert tool_page_function.get_el_alert_text() == '新增分类已成功发送请求，请耐心等待审核！'
                except Exception as e:
                    screenshot(tool_page_function.driver)
            with allure.step('登录超管账号，检查请求记录'):
                bar = tool_page_function.top_side_bar
                login_page = bar.click_menu_logout()
                login_page.login(review_account['school'], review_account['user'], review_account['pwd'])
                review_page = bar.switch_to_resource_review()
                review_page.switch_to_tool_review()
            with allure.step('检查最后一条请求的信息'):
                review_page.switch_to_last_page()
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                    res = cursor.fetchone()
                user_name = res.get('USER_NAME')
                assert review_page.get_last_record_kind() == '添加'
                assert review_page.get_last_record_tool_title() == '新增分类test'
                assert review_page.get_last_record_source() == user_name
                assert review_page.get_last_record_status() == '未审核'
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e

    @pytest.mark.tool
    @pytest.mark.parallel
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account)
    ], indirect=True)
    def test_tool_add_cancel(self, tool_page_function):
        try:
            allure.dynamic.title(f'取消新增分类')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            with allure.step('新增分类'):
                edit_mode = tool_page_function.click_edit_mode()
                add_page = edit_mode.click_add_kind()
                add_page.input_kind_name('取消新增分类test')
            with allure.step('点击返回'):
                add_page.click_return_btn()
            with allure.step('检查请求记录'):
                review_page = tool_page_function.top_side_bar.switch_to_resource_review()
                review_page.switch_to_tool_review()
                assert review_page.get_last_record_tool_title() != '取消新增分类test'
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e

    @pytest.mark.tool
    @pytest.mark.serial
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account)
    ], indirect=True)
    def test_tool_add_empty(self, tool_page_function):
        try:
            allure.dynamic.title(f'新增空分类')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            with allure.step('新增分类，输入为空'):
                edit_mode = tool_page_function.click_edit_mode()
                add_page = edit_mode.click_add_kind()
                add_page.input_kind_name('')
            with allure.step('点击确认'):
                add_page.click_confirm_btn()
                try:
                    assert tool_page_function.get_el_alert_text() == '新增分类已成功发送请求，请耐心等待审核！'
                except Exception as e:
                    screenshot(tool_page_function.driver)
            with allure.step('检查请求记录'):
                review_page = tool_page_function.top_side_bar.switch_to_resource_review()
                review_page.switch_to_tool_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_tool_title() != ''
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('工具管理')
@allure.story('删除分类')
class TestToolDelete:
    @pytest.mark.tool
    @pytest.mark.serial
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
    def test_tool_delete(self, request, tool_page_function, db_conn):
        try:
            param = request.getfixturevalue('home_page_function').param
            role = param.get('role')
            allure.dynamic.title(f'删除分类-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            with allure.step('删除最后一个分类'):
                tools = tool_page_function.get_all_tool()
                edit_mode = tool_page_function.click_edit_mode()
                del_page = edit_mode.click_delete_btn_by_index(-1)
                label = del_page.get_tool_label()
                title = del_page.get_tool_title()
                assert title == tools[-1]
            with allure.step('点击返回'):
                del_page.click_return_btn()
            with allure.step('点击删除'):
                del_page = edit_mode.click_delete_btn_by_index(-1)
                del_page.click_delete_btn()
                try:
                    assert tool_page_function.get_el_alert_text() == '删除分类已成功发送请求，请耐心等待审核！'
                except Exception as e:
                    screenshot(tool_page_function.driver)
            with allure.step('检查是否已删除'):
                assert len(tool_page_function.get_all_tool()) == len(tools)
                assert tool_page_function.get_all_tool()[-1] == title
            with allure.step('登录超管账号，检查请求记录'):
                bar = tool_page_function.top_side_bar
                login_page = bar.click_menu_logout()
                login_page.login(review_account['school'], review_account['user'], review_account['pwd'])
                review_page = bar.switch_to_resource_review()
                review_page.switch_to_tool_review()
            with allure.step('检查最后一条请求的信息'):
                review_page.switch_to_last_page()
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                    res = cursor.fetchone()
                user_name = res.get('USER_NAME')
                assert review_page.get_last_record_kind() == '删除'
                assert review_page.get_last_record_tool_label() == label
                assert review_page.get_last_record_tool_title() == title
                assert review_page.get_last_record_source() == user_name
                assert review_page.get_last_record_status() == '未审核'
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('工具管理')
@allure.story('修改工具')
class TestToolEdit:
    @pytest.mark.tool
    @pytest.mark.serial
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
    def test_tool_edit(self, request, tool_page_function, db_conn):
        try:
            param = request.getfixturevalue('home_page_function').param
            role = param.get('role')
            allure.dynamic.title(f'修改工具-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-工具列表')
            assert tool_page_function.verify_page()
            with allure.step('修改最后一个分类'):
                last_title = tool_page_function.get_all_tool()[-1]
                edit_mode = tool_page_function.click_edit_mode()
                edit_page = edit_mode.click_edit_btn_by_index(-1)
            with allure.step('检查详情页信息'):
                assert edit_page.get_tool_kind() == last_title
                assert edit_page.get_opt_kind() == '修改'
            with allure.step('修改工具，点击返回'):
                edit_page.input_tool_kind('123')
                edit_page.click_return_btn()
            with allure.step('修改工具，点击确认'):
                tool_page_function.click_edit_mode().click_edit_btn_by_index(-1)
                assert edit_page.get_tool_kind() == last_title
                edit_page.input_tool_kind('修改工具kind')
                edit_page.input_tool_name('修改工具name')
                edit_page.input_tool_link('修改工具link')
                edit_page.click_confirm_btn()
                assert '已成功发送请求，请耐心等待审核' in tool_page_function.get_el_alert_text()
            with allure.step('登录超管账号，检查请求记录'):
                bar = tool_page_function.top_side_bar
                login_page = bar.click_menu_logout()
                login_page.login(review_account['school'], review_account['user'], review_account['pwd'])
                review_page = bar.switch_to_resource_review()
                review_page.switch_to_tool_review()
            with allure.step('检查最后一条请求的信息'):
                review_page.switch_to_last_page()
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                    res = cursor.fetchone()
                user_name = res.get('USER_NAME')
                assert review_page.get_last_record_tool_title() == '修改工具name'
                assert review_page.get_last_record_source() == user_name
                assert review_page.get_last_record_status() == '未审核'
        except Exception as e:
            screenshot(tool_page_function.driver)
            raise e

