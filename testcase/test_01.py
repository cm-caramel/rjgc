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
    @pytest.mark.parametrize("module", ['个人项目', '结对编程', '团队项目'])
    @pytest.mark.parametrize("opt", ['确认', '否决', '返回'])
    def test01(self, home_page, db_conn, opt, module):
        try:
            title = f'{module}-删除{opt}'
            kind = module[:2]
            with db_conn.cursor() as cursor:
                cursor.execute(f"CALL add_project('{login_account['user']}', '{title}', '困难', '{kind}')")
                db_conn.commit()
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
        except Exception as e:
            screenshot(home_page.driver)
            raise e
        # finally:
        #     with db_conn.cursor() as cursor:
        #         cursor.execute('CALL reset_project();')
        #         db_conn.commit()


class Test02:
    # @pytest.mark.test
    def test02(self):
        a = 'https://www.baidu.com'
        print(a.split('https://')[1])
