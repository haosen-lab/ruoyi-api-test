"""
登录日志管理API封装
"""
import allure
from typing import Dict, Any, List
from utils.request_utils import request


class LoginLogAPI:
    """登录日志管理接口"""

    BASE_PATH = "/monitor/logininfor"

    @staticmethod
    @allure.step("获取登录日志列表")
    def list_loginlogs(page_num: int = 1, page_size: int = 10, **kwargs):
        """
        获取登录日志列表

        Args:
            page_num: 页码
            page_size: 每页数量
            **kwargs: 其他查询参数
        """
        params = {
            "pageNum": page_num,
            "pageSize": page_size,
            **kwargs
        }
        return request.get(f"{LoginLogAPI.BASE_PATH}/list", params=params)

    @staticmethod
    @allure.step("删除登录日志")
    def delete_loginlog(info_ids: List[int]):
        """
        删除登录日志

        Args:
            info_ids: 登录日志ID列表
        """
        ids_str = ",".join(map(str, info_ids))
        return request.delete(f"{LoginLogAPI.BASE_PATH}/{ids_str}")

    @staticmethod
    @allure.step("清空登录日志")
    def clean_loginlog():
        """清空所有登录日志"""
        return request.delete(f"{LoginLogAPI.BASE_PATH}/clean")

    @staticmethod
    @allure.step("导出登录日志")
    def export_loginlogs(**kwargs):
        """
        导出登录日志

        Args:
            **kwargs: 查询参数
        """
        return request.post(f"{LoginLogAPI.BASE_PATH}/export", data=kwargs)

    @staticmethod
    @allure.step("解锁账户")
    def unlock(login_name: str):
        """
        解锁账户

        Args:
            login_name: 登录账户名
        """
        params = {"loginName": login_name}
        return request.post(f"{LoginLogAPI.BASE_PATH}/unlock", data=params)


loginlog_api = LoginLogAPI()
