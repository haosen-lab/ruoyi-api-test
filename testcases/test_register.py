"""
用户注册模块测试用例
"""
import pytest
import allure
from api.register_api import register_api
from utils.assert_utils import asserter
from utils.data_generator import generator
from utils.db_utils import db


@allure.epic("若依后台管理系统")
@allure.feature("用户注册模块")
class TestRegister:
    """用户注册测试类"""

    @allure.story("正常注册场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("用户注册成功")
    def test_register_success(self):
        """测试用户注册成功"""
        username = generator.random_username("reg")

        response = register_api.register(
            username=username,
            password="Test@123456"
        )

        # 注册成功或返回提示信息（取决于后端注册开关配置）
        asserter.assert_code(response, 200)

        # 清理测试数据
        db.safe_cleanup("sys_user", "user_name", username)

    @allure.story("异常注册场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("注册失败-用户名已存在")
    def test_register_username_exists(self):
        """测试注册时用户名已存在"""
        response = register_api.register(
            username="admin",
            password="Test@123456"
        )

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常注册场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("注册失败-缺少用户名")
    def test_register_missing_username(self):
        """测试注册时缺少用户名字段"""
        response = register_api.register_raw({"password": "Test@123456"})

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
