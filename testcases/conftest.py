"""
Pytest配置文件 - 包含fixture定义
增强: 防污染数据清理、日志初始化
"""
import pytest
import allure
import json
import os
import inspect
from utils.request_utils import RequestUtils, request
from utils.logger import logger
from utils.db_utils import db
from api.login_api import login_api
from config.settings import ADMIN_USER

# 用于存储测试用例的额外信息（中文标题、请求响应等）
_test_case_info = {}

def get_test_case_info():
    """获取所有测试用例信息"""
    return _test_case_info

def pytest_runtest_setup(item):
    """测试用例执行前 - 收集中文标题"""
    # 对于参数化测试用例，先去掉参数部分（去掉方括号及内容）
    base_name = item.name.split('[')[0]
    
    # 获取测试函数对象
    func = None
    for obj in item.instance.__class__.__dict__.values():
        if hasattr(obj, '__name__') and obj.__name__ == base_name:
            func = obj
            break
    
    # 提取allure.title
    chinese_title = item.name
    if func:
        # 检查是否有allure.title装饰器
        if hasattr(func, 'allure_title'):
            chinese_title = func.allure_title
        else:
            # 尝试从装饰器中获取
            source = inspect.getsource(func)
            if '@allure.title' in source:
                import re
                match = re.search(r'@allure\.title\(["\'](.+?)["\']', source)
                if match:
                    chinese_title = match.group(1)
    
    # 也检查函数的docstring
    if chinese_title == item.name and func and func.__doc__:
        chinese_title = func.__doc__.strip().split('\n')[0]
    
    # 存储测试用例信息
    _test_case_info[item.nodeid] = {
        'chinese_title': chinese_title,
        'requests': []
    }
    
    # 清空请求记录
    RequestUtils.clear_current_test_requests()

def pytest_runtest_teardown(item, nextitem):
    """测试用例执行后 - 收集请求响应"""
    if item.nodeid in _test_case_info:
        # 保存请求响应信息
        _test_case_info[item.nodeid]['requests'] = RequestUtils.get_current_test_requests()
        # 清空请求记录
        RequestUtils.clear_current_test_requests()

def pytest_sessionfinish(session, exitstatus):
    """测试会话结束 - 保存测试用例信息到JSON"""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'test_case_info.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(_test_case_info, f, ensure_ascii=False, indent=2)


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    """测试会话级别的初始化"""
    logger.info("=" * 60)
    logger.info("测试会话开始")
    logger.info("=" * 60)
    allure.dynamic.feature("若依后台管理系统接口测试")
    yield
    request.close()
    db.close()
    logger.info("测试会话结束")


@pytest.fixture(scope="class")
def admin_login():
    """管理员登录fixture - 返回token (含自愈机制)"""
    import bcrypt

    def _do_login():
        resp = login_api.login(
            username=ADMIN_USER["username"],
            password=ADMIN_USER["password"],
            code="",
            uuid=""
        )
        return resp

    with allure.step("管理员登录"):
        response = _do_login()
        json_data = response.json()

        # 登录失败时尝试自愈: 重建admin用户
        if json_data.get("code") != 200:
            logger.warning("登录失败，尝试自愈: %s", json_data.get("msg"))
            with allure.step("自愈: 重建admin用户"):
                try:
                    hashed = bcrypt.hashpw(
                        ADMIN_USER["password"].encode(),
                        bcrypt.gensalt(rounds=10)
                    ).decode().replace("$2b$", "$2a$")
                    db.execute_update(
                        "INSERT INTO sys_user (user_id, dept_id, user_name, nick_name, "
                        "password, status, del_flag) VALUES (1, 103, %s, %s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE password=VALUES(password), "
                        "status=VALUES(status), del_flag=VALUES(del_flag)",
                        (ADMIN_USER["username"], "管理员", hashed, "0", "0")
                    )
                    db.execute_update(
                        "INSERT IGNORE INTO sys_user_role (user_id, role_id) VALUES (1, 1)"
                    )
                    logger.info("自愈成功，重新登录")
                    response = _do_login()
                    json_data = response.json()
                except Exception as e:
                    logger.error("自愈失败: %s", e)

        assert response.status_code == 200, f"HTTP状态码错误: {response.status_code}"
        assert json_data.get("code") == 200, f"登录失败: {json_data.get('msg')}"

        token = json_data.get("token")
        request.set_token(token)
        allure.attach(token, "获取到的Token", allure.attachment_type.TEXT)

    # yield必须放在try-finally外面，确保返回token
    yield token


@pytest.fixture(scope="function")
def fresh_session():
    """每次测试前创建新的session（无token）"""
    new_request = RequestUtils()
    yield new_request
    new_request.close()


@pytest.fixture(scope="function")
def fresh_session_with_admin():
    """每次测试前创建新的session并登录为管理员"""
    new_request = RequestUtils()
    response = login_api.login(
        username=ADMIN_USER["username"],
        password=ADMIN_USER["password"],
        code="",
        uuid=""
    )
    if response.status_code == 200:
        json_data = response.json()
        if json_data.get("code") == 200:
            new_request.set_token(json_data.get("token"))
    yield new_request
    new_request.close()


# ============ 测试数据生成 fixtures ============

@pytest.fixture(scope="function")
def test_user_data():
    """生成测试用户数据，测试后自动清理"""
    from utils.data_generator import generator
    user_data = {
        "userName": generator.random_username(),
        "nickName": generator.random_string(6, "测试用户"),
        "password": generator.random_password(),
        "phonenumber": generator.random_phone(),
        "email": generator.random_email(),
        "sex": "0",
        "status": "0",
        "deptId": 100,
        "roleIds": [1],
        "postIds": [1],
        "remark": generator.random_remark()
    }
    yield user_data
    db.safe_cleanup("sys_user", "user_name", user_data['userName'])


@pytest.fixture(scope="function")
def test_dept_data():
    """生成测试部门数据，测试后自动清理"""
    from utils.data_generator import generator
    dept_data = {
        "parentId": 100,
        "deptName": generator.random_dept_name(),
        "orderNum": 0,
        "leader": generator.random_string(4, "负责人"),
        "phone": generator.random_phone(),
        "email": generator.random_email(),
        "status": "0"
    }
    yield dept_data
    db.safe_cleanup("sys_dept", "dept_name", dept_data['deptName'])


@pytest.fixture(scope="function")
def test_role_data():
    """生成测试角色数据，测试后自动清理"""
    from utils.data_generator import generator
    role_data = {
        "roleName": generator.random_role_name(),
        "roleKey": f"role:{generator.random_string(8).lower()}",
        "roleSort": 0,
        "status": "0",
        "menuIds": [1, 2, 3],
        "deptIds": [],
        "dataScope": "1",
        "remark": generator.random_remark()
    }
    yield role_data
    db.safe_cleanup("sys_role", "role_name", role_data['roleName'])


@pytest.fixture(scope="function")
def test_menu_data():
    """生成测试菜单数据，测试后自动清理"""
    from utils.data_generator import generator
    menu_data = {
        "menuName": generator.random_menu_name(),
        "parentId": 0,
        "orderNum": 0,
        "path": generator.random_string(8).lower(),
        "component": "Layout",
        "isFrame": "1",
        "isCache": "0",
        "menuType": "M",
        "visible": "0",
        "status": "0",
        "icon": "el-icon-s-home",
        "perms": f"system:{generator.random_string(6).lower()}:list"
    }
    yield menu_data
    db.safe_cleanup("sys_menu", "menu_name", menu_data['menuName'])


@pytest.fixture(scope="function")
def test_dict_type_data():
    """生成测试字典类型数据，测试后自动清理"""
    from utils.data_generator import generator
    dict_type_data = {
        "dictName": generator.random_string(8, "字典"),
        "dictType": generator.random_dict_type(),
        "status": "0",
        "remark": generator.random_remark()
    }
    yield dict_type_data
    db.delete_dict_type_by_type(dict_type_data['dictType'])


@pytest.fixture(scope="function")
def test_dict_data_data():
    """生成测试字典数据"""
    from utils.data_generator import generator
    dict_data_data = {
        "dictSort": 0,
        "dictLabel": generator.random_dict_label(),
        "dictValue": generator.random_string(5),
        "dictType": "sys_common_status",
        "cssClass": "",
        "listClass": "success",
        "isDefault": "N",
        "status": "0",
        "remark": generator.random_remark()
    }
    yield dict_data_data


@pytest.fixture(scope="function")
def test_config_data():
    """生成测试配置数据 (configType=N可删除)，测试后自动清理"""
    from utils.data_generator import generator
    config_data = {
        "configName": generator.random_string(8, "配置"),
        "configKey": generator.random_config_key(),
        "configValue": generator.random_string(10),
        "configType": "N",
        "remark": generator.random_remark()
    }
    yield config_data
    db.safe_cleanup("sys_config", "config_key", config_data['configKey'])


@pytest.fixture(scope="function")
def test_notice_data():
    """生成测试公告数据，测试后自动清理"""
    from utils.data_generator import generator
    notice_data = {
        "noticeTitle": generator.random_notice_title(),
        "noticeType": "1",
        "noticeContent": generator.random_remark(),
        "status": "0"
    }
    yield notice_data
    db.safe_cleanup("sys_notice", "notice_title", notice_data['noticeTitle'])


@pytest.fixture(scope="function")
def test_post_data():
    """生成测试岗位数据，测试后自动清理"""
    from utils.data_generator import generator
    post_data = {
        "postCode": generator.random_string(8).upper(),
        "postName": generator.random_post_name(),
        "postSort": 0,
        "status": "0",
        "remark": generator.random_remark()
    }
    yield post_data
    db.safe_cleanup("sys_post", "post_name", post_data['postName'])
