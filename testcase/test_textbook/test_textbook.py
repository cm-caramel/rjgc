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


# 本文件内的增删改用例，主要检查是否成功发送增删改的请求。至于能否增删改成功，在审核功能的用例中再验证。
@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('教材管理')
@allure.story('查看章节')
@pytest.mark.parametrize("home_page", [
    pytest.param(super_account),
    pytest.param(admin_account),
    pytest.param(teacher_account),
    pytest.param(student_account)
], indirect=True)
class TestTextbookDetail:
    @pytest.mark.textbook
    @pytest.mark.parallel
    def test_pre_next_btn(self, request, textbook_page):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'查看章节-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-教材章节')
            assert textbook_page.verify_page()
            books = textbook_page.get_all_textbook()
            first_books = books[0]
            label = first_books.split(' ', 1)[0]
            title = first_books.split(' ', 1)[1]
            with allure.step('点击第一个章节，进入详情页'):
                detail_page = textbook_page.click_textbook(label, title)
                assert detail_page.verify_page()
            with allure.step('检查标题'):
                assert detail_page.get_textbook_title() == first_books
            with allure.step('检查上一节、下一节按钮'):
                assert not detail_page.is_pre_btn_visible()
                assert detail_page.is_next_btn_visible()
            if len(detail_page.title_lists) > 1:
                with allure.step('点击下一节按钮'):
                    detail_page.click_next_btn()
                    assert detail_page.get_textbook_title() == books[1]
                if len(detail_page.title_lists) > 2:
                    assert detail_page.is_pre_btn_visible()
                    assert detail_page.is_next_btn_visible()
                else:
                    assert detail_page.is_pre_btn_visible()
                    assert not detail_page.is_next_btn_visible()
                with allure.step('点击上一节按钮'):
                    detail_page.click_pre_btn()
                    assert detail_page.get_textbook_title() == first_books
                    assert not detail_page.is_pre_btn_visible()
                    assert detail_page.is_next_btn_visible()
            if len(detail_page.title_lists) > 2:
                with allure.step('点击下一节按钮到最后一章'):
                    i = detail_page.get_current_index()
                    while i < len(detail_page.title_lists) - 1:
                        detail_page.click_next_btn()
                        i += 1
                    assert detail_page.is_pre_btn_visible()
                    assert not detail_page.is_next_btn_visible()
            with allure.step('点击返回按钮'):
                detail_page.click_return_btn()
                assert textbook_page.verify_page()
        except Exception as e:
            screenshot(textbook_page.driver)
            raise e

    @pytest.mark.textbook
    @pytest.mark.parallel
    def test_catalog(self, request, textbook_page):
        try:
            role = request.getfixturevalue('home_page').param.get('role')
            allure.dynamic.title(f'右侧目录-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-教材章节')
            books = textbook_page.get_all_textbook()
            first_books = books[0]
            label = first_books.split(' ', 1)[0]
            title = first_books.split(' ', 1)[1]
            with allure.step('点击第一个章节，进入详情页'):
                detail_page = textbook_page.click_textbook(label, title)
                assert detail_page.verify_page()
            if len(books) > 1:
                with allure.step('点击右侧目录中最后一个章节'):
                    detail_page.click_catalog_by_index(len(books) - 1)
                    assert detail_page.get_textbook_title() == books[-1]
                    assert detail_page.is_pre_btn_visible()
                    assert not detail_page.is_next_btn_visible()
            if len(books) > 2:
                with allure.step('点击右侧目录第二个章节'):
                    detail_page.click_catalog_by_index(1)
                    assert detail_page.get_textbook_title() == books[1]
                    assert detail_page.is_pre_btn_visible()
                    assert detail_page.is_next_btn_visible()
        except Exception as e:
            screenshot(textbook_page.driver)
            raise e


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('教材管理')
@allure.story('添加新书')
class TestAddTextbook:
    @pytest.mark.textbook
    @pytest.mark.serial
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
    @pytest.mark.parametrize("datas", read_data_yaml('data/textbook.yaml'))
    def test_add_textbook(self, request, textbook_page_function, db_conn, datas):
        try:
            param = request.getfixturevalue('home_page_function').param
            role = param.get('role')
            allure.dynamic.title(f'{role}-{datas["title"]}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-教材章节')
            book_cnt = len(textbook_page_function.get_all_textbook())
            title = f'添加新书{datas["textbook_title"]}' if datas['textbook_title'] else ''
            content = f'1. 新书内容{datas["textbook_content"]}' if datas['textbook_content'] else ''
            edit_mode = textbook_page_function.click_edit_mode()
            assert edit_mode.verify_page()
            with allure.step('点击添加新书'):
                edit_page = edit_mode.click_textbook_add()
                assert edit_page.get_kind() == '添加'
            with allure.step('填写信息，点击返回'):
                edit_page.input_textbook_title(title)
                edit_page.input_content(content)
                edit_page.click_return_btn()
                assert textbook_page_function.verify_page()
            with allure.step('填写信息，点击确认'):
                textbook_page_function.click_edit_mode()
                edit_page = edit_mode.click_textbook_add()
                edit_page.input_textbook_title(title)
                edit_page.input_content(content)
                edit_page.click_confirm_btn()
            if datas['success']:
                assert textbook_page_function.verify_page()
                assert textbook_page_function.get_el_alert_text() == '添加章节已成功发送请求，请耐心等待审核！'
            else:
                edit_page.click_return_btn()
            with allure.step('检查是否已添加'):
                assert len(textbook_page_function.get_all_textbook()) == book_cnt
            with allure.step('登录超管账号，检查请求记录'):
                bar = textbook_page_function.top_side_bar
                login_page = bar.click_menu_logout()
                login_page.login(review_account['school'], review_account['user'], review_account['pwd'])
                review_page = bar.switch_to_resource_review()
                review_page.switch_to_textbook_review()
            with allure.step('检查最后一条请求的信息'):
                review_page.switch_to_last_page()
                if not datas['success']:
                    assert review_page.get_last_record_textbook_title() != ''
                    return
                assert review_page.get_last_record_kind() == '添加'
                assert review_page.get_last_record_textbook_title() == title
                assert review_page.get_last_record_status() == '未审核'
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                    res = cursor.fetchone()
                assert review_page.get_last_record_source() == res.get('USER_NAME')
        except Exception as e:
            screenshot(textbook_page_function.driver)
            raise e


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('教材管理')
@allure.story('编辑章节')
class TestEditChapter:
    @pytest.mark.textbook
    @pytest.mark.serial
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
    @pytest.mark.parametrize("datas", read_data_yaml('data/textbook.yaml'))
    def test_edit_chapter(self, request, textbook_page_function, db_conn, datas):
        try:
            param = request.getfixturevalue('home_page_function').param
            role = param.get('role')
            allure.dynamic.title(f'{role}-{datas["title"]}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-教材章节')
            books = textbook_page_function.get_all_textbook()
            book = books[0]
            label = book.split(' ', 1)[0]
            title = book.split(' ', 1)[1]
            datas_title = f'修改章节{datas["textbook_title"]}' if datas['textbook_title'] else ''
            datas_content = f'修改内容{datas["textbook_content"]}' if datas['textbook_content'] else ''
            edit_mode = textbook_page_function.click_edit_mode()
            assert edit_mode.verify_page()
            with allure.step('点击章节右侧的编辑按钮'):
                edit_page = edit_mode.click_edit_btn(label, title)
                assert edit_page.get_kind() == '修改'
                assert edit_page.get_textbook_title() == title
            with allure.step('修改信息，点击返回'):
                edit_page.input_textbook_title(datas_title)
                edit_page.click_return_btn()
                assert textbook_page_function.verify_page()
            with allure.step('修改信息，点击确认'):
                textbook_page_function.click_edit_mode()
                edit_page = edit_mode.click_edit_btn(label, title)
                edit_page.input_textbook_title(datas_title)
                edit_page.input_content(datas_content)
                edit_page.click_confirm_btn()
            if datas['success']:
                assert textbook_page_function.verify_page()
                assert textbook_page_function.get_el_alert_text() == '修改章节已成功发送请求，请耐心等待审核！'
            with allure.step('登录超管账号，检查请求记录'):
                bar = textbook_page_function.top_side_bar
                login_page = bar.click_menu_logout()
                login_page.login(review_account['school'], review_account['user'], review_account['pwd'])
                review_page = bar.switch_to_resource_review()
                review_page.switch_to_textbook_review()
            with allure.step('检查最后一条请求的信息'):
                review_page.switch_to_last_page()
                if not datas['success']:
                    assert review_page.get_last_record_textbook_title() != ''
                    return
                assert review_page.get_last_record_kind() == '修改'
                assert review_page.get_last_record_textbook_label() == label
                assert review_page.get_last_record_textbook_title() == title
                assert review_page.get_last_record_status() == '未审核'
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                    res = cursor.fetchone()
                assert review_page.get_last_record_source() == res.get('USER_NAME')
        except Exception as e:
            screenshot(textbook_page_function.driver)
            raise e


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('教材管理')
@allure.story('添加章节')
class TestAddChapter:
    @pytest.mark.textbook
    @pytest.mark.serial
    @pytest.mark.parametrize("home_page_function", [
        pytest.param(super_account),
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
    @pytest.mark.parametrize("datas", read_data_yaml('data/textbook.yaml'))
    def test_add_chapter(self, request, textbook_page_function, db_conn, datas):
        try:
            param = request.getfixturevalue('home_page_function').param
            role = param.get('role')
            allure.dynamic.title(f'{role}-{datas["title"]}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-教材章节')
            books = textbook_page_function.get_all_textbook()
            first_book = books[0]
            first_label = first_book.split(' ', 1)[0]
            first_title = first_book.split(' ', 1)[1]
            datas_title = f'添加章节{datas["textbook_title"]}' if datas['textbook_title'] else ''
            datas_content = f'章节内容{datas["textbook_content"]}' if datas['textbook_content'] else ''
            edit_mode = textbook_page_function.click_edit_mode()
            assert edit_mode.verify_page()
            with allure.step('点击章节右侧的添加按钮'):
                edit_page = edit_mode.click_add_btn(first_label, first_title)
                assert edit_page.get_kind() == '添加'
            with allure.step('填写信息，点击返回'):
                edit_page.input_textbook_title(datas_title)
                edit_page.click_return_btn()
                assert textbook_page_function.verify_page()
            with allure.step('填写信息，点击确认'):
                textbook_page_function.click_edit_mode()
                edit_page = edit_mode.click_add_btn(first_label, first_title)
                edit_page.input_textbook_title(datas_title)
                edit_page.input_content(datas_content)
                edit_page.click_confirm_btn()
            if datas['success']:
                assert textbook_page_function.verify_page()
                assert textbook_page_function.get_el_alert_text() == '添加章节已成功发送请求，请耐心等待审核！'
            else:
                edit_page.click_return_btn()
            with allure.step('检查是否已添加'):
                assert len(textbook_page_function.get_all_textbook()) == len(books)
            with allure.step('登录超管账号，检查请求记录'):
                bar = textbook_page_function.top_side_bar
                login_page = bar.click_menu_logout()
                login_page.login(review_account['school'], review_account['user'], review_account['pwd'])
                review_page = bar.switch_to_resource_review()
                review_page.switch_to_textbook_review()
            with allure.step('检查最后一条请求的信息'):
                review_page.switch_to_last_page()
                if not datas['success']:
                    assert review_page.get_last_record_textbook_title() != ''
                    return
                assert review_page.get_last_record_kind() == '添加'
                assert review_page.get_last_record_textbook_label().startswith(f'{first_label}.')
                assert review_page.get_last_record_textbook_title() == datas_title
                assert review_page.get_last_record_status() == '未审核'
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                    res = cursor.fetchone()
                assert review_page.get_last_record_source() == res.get('USER_NAME')
        except Exception as e:
            screenshot(textbook_page_function.driver)
            raise e


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('教材管理')
@allure.story('删除章节')
@pytest.mark.parametrize("home_page", [
    pytest.param(super_account),
    pytest.param(admin_account),
    pytest.param(teacher_account)
], indirect=True)
class TestDeleteChapter:
    @pytest.mark.textbook
    @pytest.mark.serial
    def test_delete_chapter(self, request, textbook_page, db_conn):
        try:
            param = request.getfixturevalue('home_page').param
            role = param.get('role')
            allure.dynamic.title(f'删除章节-{role}')
            allure.dynamic.description(f'前置条件：\n1. {role}登录后点击教材管理-教材章节')
            books = textbook_page.get_all_textbook()
            book = books[-1]
            label = book.split(' ', 1)[0]
            title = book.split(' ', 1)[1]
            edit_mode = textbook_page.click_edit_mode()
            assert edit_mode.verify_page()
            with allure.step('删除最后一个章节'):
                delete_page = edit_mode.click_delete_btn(label, title)
            with allure.step('检查章节信息'):
                assert delete_page.get_textbook_title() == title
                assert delete_page.get_textbook_label() == label
            delete_page.click_outside_close()
            edit_mode.click_delete_btn(label, title)
            delete_page.click_return_btn()
            edit_mode.click_delete_btn(label, title)
            with allure.step('点击删除按钮'):
                delete_page.click_delete_btn()
                assert delete_page.get_el_alert_text() == '删除请求已成功发送，请耐心等待审核！'
                delete_page.close_if_open()
            with allure.step('检查是否已删除'):
                assert len(textbook_page.get_all_textbook()) == len(books)
                assert textbook_page.get_all_textbook()[-1] == book
            with allure.step('登录超管账号，检查请求记录'):
                bar = textbook_page.top_side_bar
                login_page = bar.click_menu_logout()
                login_page.login(review_account['school'], review_account['user'], review_account['pwd'])
                review_page = bar.switch_to_resource_review()
                review_page.switch_to_textbook_review()
            with allure.step('检查最后一条请求的信息'):
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '删除'
                assert review_page.get_last_record_textbook_label() == label
                assert review_page.get_last_record_textbook_title() == title
                assert review_page.get_last_record_status() == '未审核'
                with db_conn.cursor() as cursor:
                    cursor.execute(f"select * from v_user "
                                   f"where SCHOOL_NAME = '{param['school']}' and USER_ACCOUNT = '{param['user']}'")
                    res = cursor.fetchone()
                assert review_page.get_last_record_source() == res.get('USER_NAME')
        except Exception as e:
            screenshot(textbook_page.driver)
            raise e
