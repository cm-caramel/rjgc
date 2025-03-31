import time

from common.utils import *

login_account = {
    "school": "东莞理工学院",
    "user": "10010",
    "pwd": "123"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('测试')
@pytest.mark.parametrize("home_page", [
    pytest.param(login_account)
], indirect=True)
class Test01:
    # @pytest.mark.test
    def test01(self, tool_page):
        p = tool_page.click_edit_mode().click_edit_btn_by_index(-1)
        p.input_tool_name('')
        time.sleep(3)
        p.click_confirm_btn()
        rp = tool_page.top_side_bar.switch_to_resource_review()
        rp.switch_to_tool_review()
        rp.switch_to_last_page()
        time.sleep(3)
