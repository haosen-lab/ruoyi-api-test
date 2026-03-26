"""
部门管理API封装
"""
import allure
from typing import Dict, Any, List
from utils.request_utils import request


class DeptAPI:
    """部门管理接口"""
    
    BASE_PATH = "/system/dept"
    
    @staticmethod
    @allure.step("获取部门列表")
    def list_depts(**kwargs):
        """
        获取部门列表
        
        Args:
            **kwargs: 查询参数(deptName, status等)
        """
        return request.get(f"{DeptAPI.BASE_PATH}/list", params=kwargs)
    
    @staticmethod
    @allure.step("获取部门列表(排除节点)")
    def list_depts_exclude(dept_id: int):
        """
        查询部门列表（排除节点）
        
        Args:
            dept_id: 要排除的部门ID
        """
        return request.get(f"{DeptAPI.BASE_PATH}/list/exclude/{dept_id}")
    
    @staticmethod
    @allure.step("获取部门详情")
    def get_dept(dept_id: int):
        """
        根据部门ID获取详情
        
        Args:
            dept_id: 部门ID
        """
        return request.get(f"{DeptAPI.BASE_PATH}/{dept_id}")
    
    @staticmethod
    @allure.step("新增部门")
    def add_dept(dept_data: Dict[str, Any]):
        """
        新增部门
        
        Args:
            dept_data: 部门数据字典
        """
        return request.post(DeptAPI.BASE_PATH, json_data=dept_data)
    
    @staticmethod
    @allure.step("修改部门")
    def update_dept(dept_data: Dict[str, Any]):
        """
        修改部门
        
        Args:
            dept_data: 部门数据字典
        """
        return request.put(DeptAPI.BASE_PATH, json_data=dept_data)
    
    @staticmethod
    @allure.step("删除部门")
    def delete_dept(dept_id: int):
        """
        删除部门
        
        Args:
            dept_id: 部门ID
        """
        return request.delete(f"{DeptAPI.BASE_PATH}/{dept_id}")
    
    @staticmethod
    @allure.step("保存部门排序")
    def update_sort(dept_ids: List[int], order_nums: List[int]):
        """
        保存部门排序
        
        Args:
            dept_ids: 部门ID列表
            order_nums: 排序号列表
        """
        data = {
            "deptIds": ",".join(map(str, dept_ids)),
            "orderNums": ",".join(map(str, order_nums))
        }
        return request.put(f"{DeptAPI.BASE_PATH}/updateSort", json_data=data)


# 全局部门API实例
dept_api = DeptAPI()
