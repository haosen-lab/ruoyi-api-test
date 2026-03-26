"""
登录认证API封装
"""
import allure
from typing import Dict, Any, Optional
from utils.request_utils import request, RequestUtils


class LoginAPI:
    """登录认证接口"""
    
    BASE_PATH = ""
    
    @staticmethod
    @allure.step("用户登录")
    def login(username: str, password: str, code: str = "", uuid: str = "",
              req: RequestUtils = None):
        """
        用户登录接口
        
        Args:
            username: 用户名
            password: 密码
            code: 验证码
            uuid: 验证码UUID
            req: 自定义请求实例（可选，用于测试特殊场景）
        """
        req = req or request
        data = {
            "username": username,
            "password": password
        }
        # 验证码和UUID都为空时，不添加到请求中
        if code or uuid:
            data["code"] = code
            data["uuid"] = uuid
        return req.post("/login", json_data=data)
    
    @staticmethod
    @allure.step("获取验证码")
    def get_captcha(req: RequestUtils = None):
        """获取验证码"""
        req = req or request
        return req.get("/captchaImage")
    
    @staticmethod
    @allure.step("获取用户信息")
    def get_info(req: RequestUtils = None):
        """
        获取当前登录用户信息
        
        Args:
            req: 自定义请求实例（可选，用于测试特殊场景）
        """
        req = req or request
        return req.get("/getInfo")
    
    @staticmethod
    @allure.step("获取路由信息")
    def get_routers(req: RequestUtils = None):
        """
        获取用户路由信息
        
        Args:
            req: 自定义请求实例（可选，用于测试特殊场景）
        """
        req = req or request
        return req.get("/getRouters")
    
    @staticmethod
    @allure.step("用户登出")
    def logout(req: RequestUtils = None):
        """用户登出"""
        req = req or request
        return req.post("/logout")

    @staticmethod
    @allure.step("用户登录(原始数据)")
    def login_raw(data: dict, req: RequestUtils = None):
        """
        用户登录接口 - 发送原始数据

        Args:
            data: 请求数据字典
            req: 自定义请求实例（可选，用于测试特殊场景）
        """
        req = req or request
        return req.post("/login", json_data=data)


# 全局登录API实例
login_api = LoginAPI()
