from common.utils import *

login_account = {
    "school": "东莞理工学院",
    "user": "10010",
    "pwd": "123"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('项目审核')
@pytest.mark.parametrize("home_page", [
    pytest.param(login_account)
], indirect=True)
class TestProjectReview:
    @pytest.mark.project_review
    @pytest.mark.serial
    @allure.story('上传项目')
    @pytest.mark.parametrize("opt", ['确认', '否决', '返回'])
    @pytest.mark.parametrize("module", ['个人项目', '结对编程', '团队项目'])
    def test_upload(self, home_page, db_conn, opt, module):
        try:
            allure.dynamic.title(f'{module}-{opt}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-项目审核')
            with allure.step('上传项目'):
                if module == '个人项目':
                    project_page = home_page.top_side_bar.switch_to_personal_project()
                    project_page.verify_personal_page()
                elif module == '结对编程':
                    project_page = home_page.top_side_bar.switch_to_pair_programming()
                    project_page.verify_pair_page()
                else:
                    project_page = home_page.top_side_bar.switch_to_team_project()
                    project_page.verify_team_page()
                upload_page = project_page.click_upload_btn()
                title = f'{module}-上传{opt}'
                intro = title + ' xxx'
                upload_page.input_project_name(title)
                upload_page.click_difficult_btn()
                upload_page.input_project_intro(intro)
                upload_page.click_confirm_btn()
            with allure.step('检查审核详情信息'):
                review_page = home_page.top_side_bar.switch_to_project_review()
                review_page.switch_to_last_page()
                assert review_page.get_project_name_by_index(-1) == title \
                       and review_page.get_request_kind_by_index(-1) == '添加'
                review_detail = review_page.click_detail_btn_by_index(-1)
                assert review_detail.get_project_name() == title
                assert review_detail.get_request_kind() == '添加'
                assert review_detail.get_project_intro() == intro
            with allure.step('审核'):
                if opt == '确认':
                    review_detail.click_confirm_btn()
                    assert review_detail.get_el_alert_text() == '确认成功'
                elif opt == '否决':
                    review_detail.click_reject_btn()
                    assert review_detail.get_el_alert_text() == '否决成功'
                else:
                    review_detail.click_return_btn()
                assert review_page.verify_page()
            with allure.step('检查审核结果'):
                review_page.switch_to_last_page()
                review_page.click_detail_btn_by_index(-1)
                if opt == '返回':
                    assert review_detail.is_confirm_btn_visible() and review_detail.is_reject_btn_visible()
                else:
                    assert not review_detail.is_confirm_btn_visible()
                    assert not review_detail.is_reject_btn_visible()
                if module == '个人项目':
                    project_page = home_page.top_side_bar.switch_to_personal_project()
                    project_page.verify_personal_page()
                elif module == '结对编程':
                    project_page = home_page.top_side_bar.switch_to_pair_programming()
                    project_page.verify_pair_page()
                else:
                    home_page.top_side_bar.switch_to_team_project()
                    project_page.verify_team_page()
                if opt != '确认':
                    assert project_page.get_project_name_by_index(-1) != title
                    return
                assert project_page.get_project_name_by_index(-1) == title
                assert project_page.get_school_by_index(-1) == login_account.get('school')
                if module == '个人项目' or module == '结对编程':
                    assert project_page.get_difficulty_by_index(-1) == '困难'
                detail_page = project_page.click_detail_btn_by_index(-1)
                assert detail_page.get_project_name() == title
                assert detail_page.get_project_intro() == intro
                assert detail_page.get_project_kind() == module[:2]
        except Exception as e:
            screenshot(home_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute('CALL reset_project();')
                db_conn.commit()

    @pytest.mark.project_review
    @pytest.mark.serial
    @allure.story('删除项目')
    @pytest.mark.parametrize("module", ['个人项目', '结对编程', '团队项目'])
    @pytest.mark.parametrize("opt", ['确认', '否决', '返回'])
    def test_delete(self, home_page, db_conn, opt, module):
        try:
            allure.dynamic.title(f'{module}-{opt}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-项目审核')
            with allure.step('数据库添加一个项目'):
                title = f'{module}-删除{opt}'
                kind = module[:2]
                with db_conn.cursor() as cursor:
                    cursor.execute(f"CALL add_project('{login_account['user']}', '{title}', '困难', '{kind}')")
                    db_conn.commit()
            with allure.step('删除项目'):
                if module == '个人项目':
                    project_page = home_page.top_side_bar.switch_to_personal_project()
                    project_page.verify_personal_page()
                elif module == '结对编程':
                    project_page = home_page.top_side_bar.switch_to_pair_programming()
                    project_page.verify_pair_page()
                else:
                    project_page = home_page.top_side_bar.switch_to_team_project()
                    project_page.verify_team_page()
                assert project_page.get_project_name_by_index(-1) == title
                project_page.click_delete_btn_by_index(-1).click_delete_btn()
            with allure.step('审核'):
                review_page = home_page.top_side_bar.switch_to_project_review()
                review_page.switch_to_last_page()
                assert review_page.get_project_name_by_index(-1) == title \
                       and review_page.get_request_kind_by_index(-1) == '删除'
                review_detail = review_page.click_detail_btn_by_index(-1)
                if opt == '确认':
                    review_detail.click_confirm_btn()
                    assert review_detail.get_el_alert_text() == '确认成功'
                elif opt == '否决':
                    review_detail.click_reject_btn()
                    assert review_detail.get_el_alert_text() == '否决成功'
                else:
                    review_detail.click_return_btn()
                assert review_page.verify_page()
            with allure.step('检查审核结果'):
                review_page.switch_to_last_page()
                review_page.click_detail_btn_by_index(-1)
                if opt == '返回':
                    assert review_detail.is_confirm_btn_visible() and review_detail.is_reject_btn_visible()
                else:
                    assert not review_detail.is_confirm_btn_visible()
                    assert not review_detail.is_reject_btn_visible()
                if module == '个人项目':
                    project_page = home_page.top_side_bar.switch_to_personal_project()
                    project_page.verify_personal_page()
                elif module == '结对编程':
                    project_page = home_page.top_side_bar.switch_to_pair_programming()
                    project_page.verify_pair_page()
                else:
                    home_page.top_side_bar.switch_to_team_project()
                    project_page.verify_team_page()
                if opt == '确认':
                    assert project_page.get_project_name_by_index(-1) != title
                else:
                    assert project_page.get_project_name_by_index(-1) == title
        except Exception as e:
            screenshot(home_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute('CALL reset_project();')
                db_conn.commit()

    @pytest.mark.project_review
    @pytest.mark.serial
    @allure.story('删除项目')
    @allure.step('删除项目审核详情')
    @pytest.mark.parametrize("module", ['个人项目', '结对编程', '团队项目'])
    def test_delete_detail(self, home_page, db_conn, module):
        try:
            allure.dynamic.title(module)
            allure.dynamic.description(f'前置条件：\n1. 登录后点击项目管理-项目审核')
            with allure.step('数据库添加一个项目'):
                title = f'{module}-删除审核详情'
                kind = module[:2]
                with db_conn.cursor() as cursor:
                    cursor.execute(f"CALL add_project('{login_account['user']}', '{title}', '困难', '{kind}')")
                    db_conn.commit()
            with allure.step('删除项目'):
                if module == '个人项目':
                    project_page = home_page.top_side_bar.switch_to_personal_project()
                    project_page.verify_personal_page()
                elif module == '结对编程':
                    project_page = home_page.top_side_bar.switch_to_pair_programming()
                    project_page.verify_pair_page()
                else:
                    project_page = home_page.top_side_bar.switch_to_team_project()
                    project_page.verify_team_page()
                assert project_page.get_project_name_by_index(-1) == title
                project_page.click_delete_btn_by_index(-1).click_delete_btn()
            with allure.step('检查审核详情页'):
                review_page = home_page.top_side_bar.switch_to_project_review()
                review_page.switch_to_last_page()
                assert review_page.get_project_name_by_index(-1) == title \
                       and review_page.get_request_kind_by_index(-1) == '删除'
                review_detail = review_page.click_detail_btn_by_index(-1)
                assert review_detail.get_project_name() == title
                assert review_detail.get_project_kind() == module[:2]
                assert review_detail.get_request_kind() == '删除'
        except Exception as e:
            screenshot(home_page.driver)
            raise e
        finally:
            with db_conn.cursor() as cursor:
                cursor.execute('CALL reset_project();')
                db_conn.commit()

    @pytest.mark.project_review
    @pytest.mark.serial
    @allure.story('查看表格')
    @allure.title('筛选')
    def test_review_filter(self, home_page):
        try:
            review_page = home_page.top_side_bar.switch_to_project_review()
            with allure.step('筛选请求类型'):
                review_page.filter_request_kind('添加')
                assert '删除' not in review_page.get_all_request_kind_in_page()
            with allure.step('筛选项目类型'):
                review_page.filter_request_kind()
                review_page.filter_project_kind('个人')
                assert '团队' not in review_page.get_all_project_kind_in_page() \
                       and '结对' not in review_page.get_all_project_kind_in_page()
            with allure.step('筛选审核状态'):
                review_page.filter_project_kind()
                review_page.filter_status('未审核')
                assert '已审核' not in review_page.get_all_status_in_page() \
                       and '未通过' not in review_page.get_all_status_in_page()
        except Exception as e:
            screenshot(home_page.driver)
            raise e
