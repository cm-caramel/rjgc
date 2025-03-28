from common.utils import *

login_account = {
    "school": "东莞理工学院",
    "user": "10010",
    "pwd": "123",
    "role": "超管"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('测试')
@pytest.mark.parametrize("home_page", [
    pytest.param(login_account)
], indirect=True)
class Test01:
    # @pytest.mark.test
    def test01(self, home_page):
        p = home_page.top_side_bar.switch_to_resource_review()
        p.switch_to_last_page()
        print(p.get_second_last_record())
