"""
操作日志管理API封装
"""
import allure
from typing import Dict, Any, List
from utils.request_utils import request


class OperLogAPI:
    """操作日志管理接口"""

    BASE_PATH = "/monitor/operlog"

    @staticmethod
    @allure.step("获取操作日志列表")
    def list_operlogs(page_num: int = 1, page_size: int = 10, **kwargs):
        """
        获取操作日志列表

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
        return request.get(f"{OperLogAPI.BASE_PATH}/list", params=params)

    @staticmethod
    @allure.step("获取操作日志详情")
    def get_operlog(oper_id: int):
        """
        根据操作日志ID获取详情

        Args:
            oper_id: 操作日志ID
        """
        return request.get(f"{OperLogAPI.BASE_PATH}/{oper_id}")

    @staticmethod
    @allure.step("删除操作日志")
    def delete_operlog(oper_ids: List[int]):
        """
        删除操作日志

        Args:
            oper_ids: 操作日志ID列表
        """
        ids_str = ",".join(map(str, oper_ids))
        return request.delete(f"{OperLogAPI.BASE_PATH}/{ids_str}")

    @staticmethod
    @allure.step("清空操作日志")
    def clean_operlog():
        """清空所有操作日志"""
        return request.delete(f"{OperLogAPI.BASE_PATH}/clean")

    @staticmethod
    @allure.step("导出操作日志")
    def export_operlogs(**kwargs):
        """
        导出操作日志

        Args:
            **kwargs: 查询参数
        """
        return request.post(f"{OperLogAPI.BASE_PATH}/export", data=kwargs)


operlog_api = OperLogAPI()
