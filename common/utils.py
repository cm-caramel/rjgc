import allure
import pytest
import yaml

# 读取配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    conf = yaml.safe_load(file)
sql_check = conf['sql_check']


def screenshot(driver):
    png = driver.get_screenshot_as_png()
    allure.attach(
        png,
        name="失败截图",
        attachment_type=allure.attachment_type.PNG
    )


def read_data_yaml(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            datas = yaml.safe_load(f)
        return datas
    except Exception as e:
        pytest.fail(f"\n读取数据文件出错：{path}\n\n{str(e)}", False)
