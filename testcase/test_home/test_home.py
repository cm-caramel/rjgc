from common.utils import *

login_account = {
    "school": "东莞理工学院",
    "user": "10010",
    "pwd": "123"
}


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('首页')
@allure.story('首页')
@pytest.mark.parametrize("home_page", [
        pytest.param(login_account)
    ], indirect=True)
class TestHome:
    @pytest.mark.home
    @pytest.mark.parallel
    @allure.title('点击消息')
    def test_click_msg(self, home_page):
        try:
            home_page.click_msg_btn()
            with allure.step('跳转到消息页'):
                assert home_page.has_page_change()
        except Exception as e:
            screenshot(home_page.driver)
            raise e

    @pytest.mark.home
    @pytest.mark.parallel
    @allure.title('点击待办事项')
    def test_click_task(self, home_page):
        try:
            home_page.click_task_btn()
            with allure.step('跳转到待办事项页'):
                assert home_page.has_page_change()
        except Exception as e:
            screenshot(home_page.driver)
            raise e

    @pytest.mark.home
    @pytest.mark.parallel
    @allure.title('点击导入学生用户')
    def test_import_student(self, home_page):
        try:
            home_page.click_student_btn()
            with allure.step('跳转到导入学生用户页'):
                assert home_page.has_page_change()
        except Exception as e:
            screenshot(home_page.driver)
            raise e

    @pytest.mark.home
    @pytest.mark.parallel
    @allure.title('点击导入教师用户')
    def test_import_teacher(self, home_page):
        try:
            home_page.click_teacher_btn()
            with allure.step('跳转到导入教师用户页'):
                assert home_page.has_page_change()
        except Exception as e:
            screenshot(home_page.driver)
            raise e
