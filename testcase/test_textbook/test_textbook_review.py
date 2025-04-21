import allure

from common.utils import *

login_account = {
    "school": "东莞理工学院",
    "user": "10010",
    "pwd": "123",
    "name": "dgut1"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('教材管理')
@allure.story('教材审核')
@pytest.mark.parametrize("home_page", [
    pytest.param(login_account)
], indirect=True)
class TestTextbookReview:
    @pytest.mark.textbook
    @pytest.mark.resource_review
    @pytest.mark.serial
    @pytest.mark.parametrize("datas", ['确认', '否决', '返回'])
    def test_add_textbook(self, textbook_page, datas):
        try:
            allure.dynamic.title(f'添加新书-{datas}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-教材章节')
            books = textbook_page.get_all_textbook()
            book_cnt = len(books)
            last_book = books[-1]
            new_title = '添加新书审核test'
            new_content = 'xxx审核test'
            with allure.step('添加新书'):
                edit_page = textbook_page.click_edit_mode().click_textbook_add()
                edit_page.input_textbook_title(new_title)
                edit_page.input_content(new_content)
                edit_page.click_confirm_btn()
            with allure.step('检查审核信息'):
                review_page = textbook_page.top_side_bar.switch_to_resource_review()
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '添加'
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_textbook_title() == new_title
                assert review_page.get_last_record_status() == '未审核'
                new_label = review_page.get_last_record_textbook_label()
            with allure.step('审核详情页'):
                review_detail = review_page.click_last_record_detail()
                assert review_detail.get_title() == new_title
                assert review_detail.get_user() == login_account['name']
                assert review_detail.get_kind() == '添加'
            with allure.step('审核'):
                if datas == '确认':
                    review_detail.click_confirm_btn()
                    assert review_page.get_el_alert_text() == '确认成功'
                elif datas == '否决':
                    review_detail.click_reject_btn()
                    assert review_page.get_el_alert_text() == '否决成功'
                else:
                    review_detail.click_return_btn()
                assert review_page.verify_page()
            with allure.step('检查该请求记录'):
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '添加'
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_textbook_title() == new_title
                if datas == '确认':
                    assert review_page.get_last_record_status() == '已通过'
                elif datas == '否决':
                    assert review_page.get_last_record_status() == '未通过'
                else:
                    assert review_page.get_last_record_status() == '未审核'
            with allure.step('检查审核详情页'):
                review_detail = review_page.click_last_record_detail()
                if datas == '返回':
                    assert review_detail.is_confirm_btn_visible()
                    assert review_detail.is_reject_btn_visible()
                else:
                    assert not review_detail.is_confirm_btn_visible()
                    assert not review_detail.is_reject_btn_visible()
            with allure.step('检查审核结果'):
                review_detail.click_return_btn()
                textbook_page.top_side_bar.switch_to_textbook_chapter()
                books = textbook_page.get_all_textbook()
                if datas != '确认':
                    assert len(books) == book_cnt
                    assert books[-1] == last_book
                    return
                assert len(books) == book_cnt + 1
                assert books[-1] == f'{new_label} {new_title}'
        except Exception as e:
            screenshot(textbook_page.driver)
            raise e

    @pytest.mark.textbook
    @pytest.mark.resource_review
    @pytest.mark.serial
    @pytest.mark.parametrize("datas", ['确认', '否决', '返回'])
    def test_add_chapter(self, textbook_page, datas):
        try:
            allure.dynamic.title(f'添加章节-{datas}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-教材章节')
            books = textbook_page.get_all_textbook()
            book_cnt = len(books)
            last_book = books[-1]
            last_label = last_book.split(' ', 1)[0]
            last_title = last_book.split(' ', 1)[1]
            new_title = '添加章节审核test'
            new_content = 'xxx审核test'
            with allure.step('添加章节'):
                edit_page = textbook_page.click_edit_mode().click_add_btn(last_label, last_title)
                edit_page.input_textbook_title(new_title)
                edit_page.input_content(new_content)
                edit_page.click_confirm_btn()
            with allure.step('检查审核信息'):
                review_page = textbook_page.top_side_bar.switch_to_resource_review()
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '添加'
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_textbook_title() == new_title
                assert review_page.get_last_record_status() == '未审核'
                assert review_page.get_last_record_textbook_label().startswith(f'{last_label}.')
                new_label = review_page.get_last_record_textbook_label()
            with allure.step('审核详情页'):
                review_detail = review_page.click_last_record_detail()
                assert review_detail.get_title() == new_title
                assert review_detail.get_user() == login_account['name']
                assert review_detail.get_kind() == '添加'
            with allure.step('审核'):
                if datas == '确认':
                    review_detail.click_confirm_btn()
                    assert review_page.get_el_alert_text() == '确认成功'
                elif datas == '否决':
                    review_detail.click_reject_btn()
                    assert review_page.get_el_alert_text() == '否决成功'
                else:
                    review_detail.click_return_btn()
                assert review_page.verify_page()
            with allure.step('检查该请求记录'):
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '添加'
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_textbook_title() == new_title
                if datas == '确认':
                    assert review_page.get_last_record_status() == '已通过'
                elif datas == '否决':
                    assert review_page.get_last_record_status() == '未通过'
                else:
                    assert review_page.get_last_record_status() == '未审核'
            with allure.step('检查审核详情页'):
                review_detail = review_page.click_last_record_detail()
                if datas == '返回':
                    assert review_detail.is_confirm_btn_visible()
                    assert review_detail.is_reject_btn_visible()
                else:
                    assert not review_detail.is_confirm_btn_visible()
                    assert not review_detail.is_reject_btn_visible()
            with allure.step('检查审核结果'):
                review_detail.click_return_btn()
                textbook_page.top_side_bar.switch_to_textbook_chapter()
                books = textbook_page.get_all_textbook()
                if datas != '确认':
                    assert len(books) == book_cnt
                    assert books[-1] == last_book
                    return
                assert len(books) == book_cnt + 1
                assert books[-1] == f'{new_label} {new_title}'
        except Exception as e:
            screenshot(textbook_page.driver)
            raise e

    @pytest.mark.textbook
    @pytest.mark.resource_review
    @pytest.mark.serial
    @pytest.mark.parametrize("datas", ['确认', '否决', '返回'])
    def test_edit_chapter(self, textbook_page, datas):
        try:
            allure.dynamic.title(f'编辑章节-{datas}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-教材章节')
            books = textbook_page.get_all_textbook()
            book_cnt = len(books)
            last_book = books[-1]
            last_label = last_book.split(' ', 1)[0]
            last_title = last_book.split(' ', 1)[1]
            new_title = '修改章节审核test'
            new_content = 'xxx审核test'
            with allure.step('修改章节'):
                edit_page = textbook_page.click_edit_mode().click_edit_btn(last_label, last_title)
                edit_page.input_textbook_title(new_title)
                edit_page.input_content(new_content)
                edit_page.click_confirm_btn()
            with allure.step('检查审核信息'):
                review_page = textbook_page.top_side_bar.switch_to_resource_review()
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '修改'
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_textbook_title() == last_title
                assert review_page.get_last_record_status() == '未审核'
                assert review_page.get_last_record_textbook_label() == last_label
            with allure.step('审核详情页'):
                review_detail = review_page.click_last_record_detail()
                assert review_detail.get_user() == login_account['name']
                assert review_detail.get_kind() == '修改'
            with allure.step('审核'):
                if datas == '确认':
                    review_detail.click_confirm_btn()
                    assert review_page.get_el_alert_text() == '确认成功'
                elif datas == '否决':
                    review_detail.click_reject_btn()
                    assert review_page.get_el_alert_text() == '否决成功'
                else:
                    review_detail.click_return_btn()
                assert review_page.verify_page()
            with allure.step('检查该请求记录'):
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '修改'
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_textbook_title() == last_title
                if datas == '确认':
                    assert review_page.get_last_record_status() == '已通过'
                elif datas == '否决':
                    assert review_page.get_last_record_status() == '未通过'
                else:
                    assert review_page.get_last_record_status() == '未审核'
            with allure.step('检查审核详情页'):
                review_detail = review_page.click_last_record_detail()
                if datas == '返回':
                    assert review_detail.is_confirm_btn_visible()
                    assert review_detail.is_reject_btn_visible()
                else:
                    assert not review_detail.is_confirm_btn_visible()
                    assert not review_detail.is_reject_btn_visible()
            with allure.step('检查审核结果'):
                review_detail.click_return_btn()
                textbook_page.top_side_bar.switch_to_textbook_chapter()
                books = textbook_page.get_all_textbook()
                assert len(books) == book_cnt
                if datas == '确认':
                    assert books[-1] == f'{last_label} {new_title}'
                else:
                    assert books[-1] == last_book
        except Exception as e:
            screenshot(textbook_page.driver)
            raise e

    @pytest.mark.textbook
    @pytest.mark.resource_review
    @pytest.mark.serial
    @pytest.mark.parametrize("datas", ['确认', '否决', '返回'])
    def test_delete_chapter(self, textbook_page, datas):
        try:
            allure.dynamic.title(f'删除章节-{datas}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-教材章节')
            books = textbook_page.get_all_textbook()
            book_cnt = len(books)
            last_book = books[-1]
            last_label = last_book.split(' ', 1)[0]
            last_title = last_book.split(' ', 1)[1]
            with allure.step('删除章节'):
                del_page = textbook_page.click_edit_mode().click_delete_btn(last_label, last_title)
                del_page.click_delete_btn()
            with allure.step('检查审核信息'):
                review_page = textbook_page.top_side_bar.switch_to_resource_review()
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '删除'
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_textbook_label() == last_label
                assert review_page.get_last_record_textbook_title() == last_title
                assert review_page.get_last_record_status() == '未审核'
            with allure.step('审核详情页'):
                review_detail = review_page.click_last_record_detail()
                assert review_detail.get_user() == login_account['name']
                assert review_detail.get_kind() == '删除'
                try:
                    assert review_detail.get_title() == last_title
                except Exception as e:
                    screenshot(review_detail.driver)
            with allure.step('审核'):
                if datas == '确认':
                    review_detail.click_confirm_btn()
                    assert review_page.get_el_alert_text() == '确认成功'
                elif datas == '否决':
                    review_detail.click_reject_btn()
                    assert review_page.get_el_alert_text() == '否决成功'
                else:
                    review_detail.click_return_btn()
                assert review_page.verify_page()
            with allure.step('检查该请求记录'):
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '删除'
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_textbook_title() == last_title
                if datas == '确认':
                    assert review_page.get_last_record_status() == '已通过'
                elif datas == '否决':
                    assert review_page.get_last_record_status() == '未通过'
                else:
                    assert review_page.get_last_record_status() == '未审核'
            with allure.step('检查审核详情页'):
                review_detail = review_page.click_last_record_detail()
                if datas == '返回':
                    assert review_detail.is_confirm_btn_visible()
                    assert review_detail.is_reject_btn_visible()
                else:
                    assert not review_detail.is_confirm_btn_visible()
                    assert not review_detail.is_reject_btn_visible()
            with allure.step('检查审核结果'):
                review_detail.click_return_btn()
                textbook_page.top_side_bar.switch_to_textbook_chapter()
                books = textbook_page.get_all_textbook()
                if datas == '确认':
                    assert len(books) == book_cnt - 1
                    assert last_book not in books
                else:
                    assert len(books) == book_cnt
                    assert books[-1] == last_book
        except Exception as e:
            screenshot(textbook_page.driver)
            raise e

    @pytest.mark.textbook
    @pytest.mark.resource_review
    @pytest.mark.serial
    def test_delete_textbook_unordered(self, textbook_page):
        try:
            allure.dynamic.title('乱序删除多个章节')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-教材章节')
            books = textbook_page.get_all_textbook()
            book_cnt = len(books)
            with allure.step('添加两本新书'):
                for i in range(2):
                    title = f'删除新书test {i+1}'
                    edit_page = textbook_page.click_edit_mode().click_textbook_add()
                    edit_page.input_textbook_title(title)
                    edit_page.click_confirm_btn()
                    review_page = textbook_page.top_side_bar.switch_to_resource_review()
                    review_page.switch_to_textbook_review()
                    review_page.switch_to_last_page()
                    assert review_page.get_last_record_kind() == '添加'
                    assert review_page.get_last_record_textbook_title() == title
                    review_page.click_last_record_detail().click_confirm_btn()
                    textbook_page.top_side_bar.switch_to_textbook_chapter()
                books = textbook_page.get_all_textbook()
                assert len(books) == book_cnt + 2
            # 新书信息
            first_book = books[-2]
            first_label = first_book.split(' ', 1)[0]
            first_title = first_book.split(' ', 1)[1]
            second_book = books[-1]
            second_label = second_book.split(' ', 1)[0]
            second_title = second_book.split(' ', 1)[1]
            with allure.step('依次点击新书2删除、新书1删除'):
                edit_mode = textbook_page.click_edit_mode()
                edit_mode.click_delete_btn(second_label, second_title).click_delete_btn()
                edit_mode.click_delete_btn(first_label, first_title).click_delete_btn()
            with allure.step('审核删除新书1'):
                review_page = textbook_page.top_side_bar.switch_to_resource_review()
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_kind() == '删除'
                assert review_page.get_last_record_textbook_label() == first_label
                assert review_page.get_last_record_textbook_title() == first_title
                detail_page = review_page.click_last_record_detail()
                detail_page.click_confirm_btn()
            with allure.step('审核删除新书2'):
                review_page.switch_to_textbook_review()
                review_page.switch_to_last_page()
                res = review_page.get_second_last_record_info()
                assert res['kind'] == '删除'
                assert res['label'] == second_label
                assert res['title'] == second_title
                res['btn'].click()
                detail_page.click_confirm_btn()
            with allure.step('检查删除结果'):
                textbook_page.top_side_bar.switch_to_textbook_chapter()
                books = textbook_page.get_all_textbook()
                assert len(books) == book_cnt
        except Exception as e:
            screenshot(textbook_page.driver)
            raise e
