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
    def test01(self, course_page):
        p = course_page.click_course_by_index(0)
        p = p.click_class_detail_by_index(1)
        p = p.click_import_btn()
        print(p.get_name_by_index(0))
        print(p.is_add_btn_visible_by_index(0))
        time.sleep(1)


class Test02:
    # @pytest.mark.test
    def test02(self, db_conn):
        with db_conn.cursor() as cursor:
            cursor.execute(f"SELECT DISTINCT USER_CLASS "
                           f"FROM v_user "
                           f"WHERE SCHOOL_NAME = '东莞理工学院' AND USER_CLASS IS NOT NULL;")
            res = cursor.fetchall()
        arr = []
        for item in res:
            arr.append(item['USER_CLASS'])
        print(arr)

