import time

from common.utils import *

login_account = {
    "school": "东莞理工学院",
    "user": "10020",
    "pwd": "123"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('测试')
@pytest.mark.parametrize("home_page", [
    pytest.param(login_account)
], indirect=True)
class Test01:
    # @pytest.mark.test
    def test01(self, user_page, db_conn):
        user_page.filter_user_kind('教师')
        time.sleep(0.1)
        arr = user_page.get_all_user_kind_in_page()
        assert len(arr) == 1 and '教师' in arr
        time.sleep(2)


class Test02:
    # @pytest.mark.test
    def test02(self):
        a = ''
        b = None

