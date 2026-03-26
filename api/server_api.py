"""
服务器监控API封装
"""
import allure
from utils.request_utils import request


class ServerAPI:
    """服务器监控接口"""

    @staticmethod
    @allure.step("获取服务器信息")
    def get_server_info():
        """获取服务器详细信息"""
        return request.get("/monitor/server")


# 全局服务器监控API实例
server_api = ServerAPI()
