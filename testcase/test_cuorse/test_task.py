from common.utils import *

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


@allure.epic('软件工程导论实践教学管理平台')
@allure.feature('课程管理')
@pytest.mark.parametrize("home_page", [
        pytest.param(admin_account),
        pytest.param(teacher_account)
    ], indirect=True)
class TestTask:
    # @pytest.mark.test
    # @pytest.mark.parallel
    @allure.story('检查行政班')
    def test_class_check(self, request, course_page, db_conn):
        pass
        # try:
        #     param = request.getfixturevalue('home_page').param
        #     role = param.get('role')
        #     allure.dynamic.title(role)
        #     allure.dynamic.description(f'前置条件：\n1. {role}登录后点击课程管理')
        #     course_page.verify_page()

