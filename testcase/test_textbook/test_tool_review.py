from common.utils import *

login_account = {
    "school": "东莞理工学院",
    "user": "10010",
    "pwd": "123",
    "name": "dgut1"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('工具管理')
@allure.story('工具审核')
@pytest.mark.parametrize("home_page", [
    pytest.param(login_account)
], indirect=True)
class TestToolReview:
    @pytest.mark.resource_review
    @pytest.mark.serial
    def test_review_detail(self, tool_page):
        try:
            allure.dynamic.title('审核详情信息')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-工具列表')
            review_page = tool_page.top_side_bar.switch_to_resource_review()
            review_page.switch_to_tool_review()
            review_page.switch_to_last_page()
            with allure.step('获取最后一条审核记录'):
                kind = review_page.get_last_record_kind()
                user = review_page.get_last_record_source()
                title = review_page.get_last_record_tool_title()
                png = tool_page.driver.get_screenshot_as_png()
                allure.attach(
                    png,
                    name="审核信息截图",
                    attachment_type=allure.attachment_type.PNG
                )
            with allure.step('查看审核详情'):
                review_detail = review_page.click_last_record_detail()
                assert review_detail.get_title() == title
                assert review_detail.get_user() == user
                assert review_detail.get_kind() == kind
        except Exception as e:
            screenshot(tool_page.driver)
            raise e

    @pytest.mark.resource_review
    @pytest.mark.serial
    @pytest.mark.parametrize("datas", ['确认', '否决', '返回'])
    def test_tool_add(self, tool_page, db_conn, datas):
        try:
            allure.dynamic.title(f'新增分类-{datas}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-工具列表')
            tools = tool_page.get_all_tool()
            tool_cnt = len(tools)
            last_tool = tools[-1]
            with allure.step('新增一个分类'):
                add_page = tool_page.click_edit_mode().click_add_kind()
                add_page.input_kind_name('新增分类审核test')
                add_page.click_confirm_btn()
            with allure.step('审核'):
                review_page = tool_page.top_side_bar.switch_to_resource_review()
                review_page.switch_to_tool_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_tool_title() == '新增分类审核test'
                assert review_page.get_last_record_status() == '未审核'
                review_detail = review_page.click_last_record_detail()
                if datas == '确认':
                    review_detail.click_confirm_btn()
                    assert review_page.get_el_alert_text() == '确认成功'
                elif datas == '否决':
                    review_detail.click_reject_btn()
                    assert review_page.get_el_alert_text() == '否决成功'
                else:
                    review_detail.click_return_btn()
            with allure.step('检查该请求记录'):
                review_page.switch_to_tool_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_tool_title() == '新增分类审核test'
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
                tool_page.top_side_bar.switch_to_tool_list()
                tools = tool_page.get_all_tool()
                if datas != '确认':
                    assert len(tools) == tool_cnt
                    assert tools[-1] == last_tool
                    return
                assert len(tools) == tool_cnt + 1
                assert tools[-1] == '新增分类审核test'
        except Exception as e:
            screenshot(tool_page.driver)
            raise e

    @pytest.mark.resource_review
    @pytest.mark.serial
    @pytest.mark.parametrize("datas", ['确认', '否决', '返回'])
    def test_tool_delete(self, tool_page, db_conn, datas):
        try:
            allure.dynamic.title(f'删除分类-{datas}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-工具列表')
            with allure.step('删除最后一个分类'):
                tools = tool_page.get_all_tool()
                last_tool = tools[-1]
                tool_cnt = len(tools)
                tool_page.click_edit_mode().click_delete_btn_by_index(-1).click_delete_btn()
            with allure.step('审核'):
                review_page = tool_page.top_side_bar.switch_to_resource_review()
                review_page.switch_to_tool_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_tool_title() == last_tool
                assert review_page.get_last_record_status() == '未审核'
                review_detail = review_page.click_last_record_detail()
                if datas == '确认':
                    review_detail.click_confirm_btn()
                elif datas == '否决':
                    review_detail.click_reject_btn()
                else:
                    review_detail.click_return_btn()
            with allure.step('检查删除结果'):
                tool_page.top_side_bar.switch_to_tool_list()
                tools = tool_page.get_all_tool()
                if datas != '确认':
                    assert len(tools) == tool_cnt
                    assert tools[-1] == last_tool
                    return
                assert len(tools) == tool_cnt - 1
        except Exception as e:
            screenshot(tool_page.driver)
            raise e

    @pytest.mark.resource_review
    @pytest.mark.serial
    @pytest.mark.parametrize("datas", ['确认', '否决', '返回'])
    def test_tool_edit(self, tool_page, db_conn, datas):
        try:
            allure.dynamic.title(f'修改分类-{datas}')
            allure.dynamic.description(f'前置条件：\n1. 登录后点击教材管理-工具列表')
            with allure.step('修改最后一个分类'):
                last_tool = tool_page.get_all_tool()[-1]
                edit_page = tool_page.click_edit_mode().click_edit_btn_by_index(-1)
                edit_page.input_tool_kind('修改工具类型test')
                edit_page.input_tool_name('修改工具名称test')
                edit_page.input_tool_link('修改工具链接test')
                edit_page.click_confirm_btn()
            with allure.step('审核'):
                review_page = tool_page.top_side_bar.switch_to_resource_review()
                review_page.switch_to_tool_review()
                review_page.switch_to_last_page()
                assert review_page.get_last_record_source() == login_account['name']
                assert review_page.get_last_record_tool_title() == '修改工具名称test'
                assert review_page.get_last_record_status() == '未审核'
                review_detail = review_page.click_last_record_detail()
                if datas == '确认':
                    review_detail.click_confirm_btn()
                elif datas == '否决':
                    review_detail.click_reject_btn()
                else:
                    review_detail.click_return_btn()
            with allure.step('检查修改结果'):
                tool_page.top_side_bar.switch_to_tool_list()
                if datas != '确认':
                    assert tool_page.get_all_tool()[-1] == last_tool
                    return
                assert tool_page.get_all_tool()[-1] == '修改工具类型test'
                detail_page = tool_page.click_tool_by_index(-1)
                assert detail_page.get_tool_name() == '修改工具名称test'
                assert detail_page.get_tool_link() == '修改工具链接test'
        except Exception as e:
            screenshot(tool_page.driver)
            raise e

