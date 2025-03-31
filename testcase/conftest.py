from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from common.db_conn_pool import DBConnPool
from common.utils import *
from page.login_page import LoginPage
from common.exceptions import *

'''
1. 测试环境是否可用：mysql，request
2. 重试机制
3. pytest自动捕获及处理
'''


@pytest.fixture(scope='session')
def db_pool():
    pool = DBConnPool(conf['mysql_host'], conf['mysql_port'], conf['mysql_user'], conf['mysql_pwd'], conf['mysql_db'])
    yield pool


@pytest.fixture(scope='function')
def db_conn(db_pool):
    conn = db_pool.get_conn()
    yield conn
    conn.close()


@pytest.fixture(scope='function')
def login_page_d():
    if conf['headless']:
        options = Options()
        options.add_argument('--headless')
        d = webdriver.Chrome(service=Service(conf['driver_path']), options=options)
    else:
        d = webdriver.Chrome(service=Service(conf['driver_path']))
    d.maximize_window()
    d.get(conf['base_url'])
    yield d
    d.quit()


@pytest.fixture(scope='function')
def home_page_function(request):
    try:
        if conf['headless']:
            options = Options()
            options.add_argument('--headless')
            d = webdriver.Chrome(service=Service(conf['driver_path']), options=options)
        else:
            d = webdriver.Chrome(service=Service(conf['driver_path']))
        d.maximize_window()
        d.get(conf['base_url'])
        school = request.param.get('school')
        user = request.param.get('user')
        pwd = request.param.get('pwd')
        login_page = LoginPage(d)
        p = login_page.login(school, user, pwd)
        p.param = request.param
        assert p.verify_page()
        yield p
    except Exception as e:
        raise LoginException(f'\n\n登录失败：{school}, {user}, {pwd}\n{str(e)}') from e
    finally:
        d.quit()


@pytest.fixture(scope='class')
def home_page(request):
    try:
        if conf['headless']:
            options = Options()
            options.add_argument('--headless')
            d = webdriver.Chrome(service=Service(conf['driver_path']), options=options)
        else:
            d = webdriver.Chrome(service=Service(conf['driver_path']))
        d.maximize_window()
        d.get(conf['base_url'])
        school = request.param.get('school')
        user = request.param.get('user')
        pwd = request.param.get('pwd')
        login_page = LoginPage(d)
        p = login_page.login(school, user, pwd)
        p.param = request.param
        assert p.verify_page()
        yield p
    except Exception as e:
        raise LoginException(f'\n\n登录失败：{school}, {user}, {pwd}\n{str(e)}') from e
    finally:
        d.quit()


@pytest.fixture(scope='function')
def personal_info_page(home_page):
    p = home_page.top_side_bar.click_menu_personal_info()
    yield p


@pytest.fixture(scope='function')
def change_pwd_page(home_page):
    p = home_page.top_side_bar.click_menu_change_pwd()
    yield p


@pytest.fixture(scope='function')
def textbook_page_function(home_page_function):
    if home_page_function.param.get('role') == '学生':
        p = home_page_function.top_side_bar.switch_to_textbook_chapter_stu()
    else:
        p = home_page_function.top_side_bar.switch_to_textbook_chapter()
    yield p


@pytest.fixture(scope='function')
def textbook_page(home_page):
    if home_page.param.get('role') == '学生':
        p = home_page.top_side_bar.switch_to_textbook_chapter_stu()
    else:
        p = home_page.top_side_bar.switch_to_textbook_chapter()
    yield p


@pytest.fixture(scope='function')
def tool_page_function(home_page_function):
    if home_page_function.param.get('role') == '学生':
        p = home_page_function.top_side_bar.switch_to_tool_list_stu()
    else:
        p = home_page_function.top_side_bar.switch_to_tool_list()
    yield p


@pytest.fixture(scope='function')
def tool_page(home_page):
    if home_page.param.get('role') == '学生':
        p = home_page.top_side_bar.switch_to_tool_list_stu()
    else:
        p = home_page.top_side_bar.switch_to_tool_list()
    yield p
