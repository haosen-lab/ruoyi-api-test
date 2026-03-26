"""
用户注册API封装
"""
import allure
from utils.request_utils import request


class RegisterAPI:
    """用户注册接口"""

    @staticmethod
    @allure.step("用户注册")
    def register(username: str, password: str, code: str = "", uuid: str = ""):
        """
        用户注册接口

        Args:
            username: 用户名
            password: 密码
            code: 验证码
            uuid: 验证码UUID
        """
        data = {
            "username": username,
            "password": password
        }
        if code or uuid:
            data["code"] = code
            data["uuid"] = uuid
        return request.post("/register", json_data=data)

    @staticmethod
    @allure.step("用户注册(原始数据)")
    def register_raw(data: dict):
        """
        用户注册接口 - 发送原始数据

        Args:
            data: 请求数据字典
        """
        return request.post("/register", json_data=data)


# 全局注册API实例
register_api = RegisterAPI()
