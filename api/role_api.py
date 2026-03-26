"""
角色管理API封装
"""
import allure
from typing import Dict, Any, List
from utils.request_utils import request


class RoleAPI:
    """角色管理接口"""
    
    BASE_PATH = "/system/role"
    
    @staticmethod
    @allure.step("获取角色列表")
    def list_roles(page_num: int = 1, page_size: int = 10, **kwargs):
        """
        获取角色列表
        
        Args:
            page_num: 页码
            page_size: 每页数量
            **kwargs: 其他查询参数(roleName, roleKey, status等)
        """
        params = {
            "pageNum": page_num,
            "pageSize": page_size,
            **kwargs
        }
        return request.get(f"{RoleAPI.BASE_PATH}/list", params=params)
    
    @staticmethod
    @allure.step("获取角色详情")
    def get_role(role_id: int):
        """
        根据角色ID获取详情
        
        Args:
            role_id: 角色ID
        """
        return request.get(f"{RoleAPI.BASE_PATH}/{role_id}")
    
    @staticmethod
    @allure.step("新增角色")
    def add_role(role_data: Dict[str, Any]):
        """
        新增角色
        
        Args:
            role_data: 角色数据字典
        """
        return request.post(RoleAPI.BASE_PATH, json_data=role_data)
    
    @staticmethod
    @allure.step("修改角色")
    def update_role(role_data: Dict[str, Any]):
        """
        修改角色
        
        Args:
            role_data: 角色数据字典
        """
        return request.put(RoleAPI.BASE_PATH, json_data=role_data)
    
    @staticmethod
    @allure.step("删除角色")
    def delete_roles(role_ids: List[int]):
        """
        删除角色
        
        Args:
            role_ids: 角色ID列表
        """
        ids_str = ",".join(map(str, role_ids))
        return request.delete(f"{RoleAPI.BASE_PATH}/{ids_str}")
    
    @staticmethod
    @allure.step("修改角色状态")
    def change_status(role_id: int, status: str):
        """
        修改角色状态
        
        Args:
            role_id: 角色ID
            status: 状态(0-正常, 1-停用)
        """
        data = {
            "roleId": role_id,
            "status": status
        }
        return request.put(f"{RoleAPI.BASE_PATH}/changeStatus", json_data=data)
    
    @staticmethod
    @allure.step("修改数据权限")
    def update_data_scope(role_data: Dict[str, Any]):
        """
        修改角色数据权限
        
        Args:
            role_data: 角色数据字典(包含roleId, dataScope, deptIds)
        """
        return request.put(f"{RoleAPI.BASE_PATH}/dataScope", json_data=role_data)
    
    @staticmethod
    @allure.step("获取角色选择框列表")
    def get_option_select():
        """获取角色选择框列表"""
        return request.get(f"{RoleAPI.BASE_PATH}/optionselect")
    
    @staticmethod
    @allure.step("查询已分配用户角色列表")
    def get_allocated_users(role_id: int, page_num: int = 1, page_size: int = 10):
        """
        查询已分配用户角色列表
        
        Args:
            role_id: 角色ID
            page_num: 页码
            page_size: 每页数量
        """
        params = {
            "roleId": role_id,
            "pageNum": page_num,
            "pageSize": page_size
        }
        return request.get(f"{RoleAPI.BASE_PATH}/authUser/allocatedList", params=params)
    
    @staticmethod
    @allure.step("查询未分配用户角色列表")
    def get_unallocated_users(role_id: int, page_num: int = 1, page_size: int = 10):
        """
        查询未分配用户角色列表
        
        Args:
            role_id: 角色ID
            page_num: 页码
            page_size: 每页数量
        """
        params = {
            "roleId": role_id,
            "pageNum": page_num,
            "pageSize": page_size
        }
        return request.get(f"{RoleAPI.BASE_PATH}/authUser/unallocatedList", params=params)
    
    @staticmethod
    @allure.step("取消授权用户")
    def cancel_auth_user(role_id: int, user_id: int):
        """
        取消授权用户
        
        Args:
            role_id: 角色ID
            user_id: 用户ID
        """
        data = {
            "roleId": role_id,
            "userId": user_id
        }
        return request.put(f"{RoleAPI.BASE_PATH}/authUser/cancel", json_data=data)
    
    @staticmethod
    @allure.step("批量取消授权用户")
    def cancel_auth_user_all(role_id: int, user_ids: List[int]):
        """
        批量取消授权用户
        
        Args:
            role_id: 角色ID
            user_ids: 用户ID列表
        """
        params = {
            "roleId": role_id,
            "userIds": ",".join(map(str, user_ids))
        }
        return request.put(f"{RoleAPI.BASE_PATH}/authUser/cancelAll", data=params)
    
    @staticmethod
    @allure.step("批量选择用户授权")
    def select_auth_user_all(role_id: int, user_ids: List[int]):
        """
        批量选择用户授权
        
        Args:
            role_id: 角色ID
            user_ids: 用户ID列表
        """
        params = {
            "roleId": role_id,
            "userIds": ",".join(map(str, user_ids))
        }
        return request.put(f"{RoleAPI.BASE_PATH}/authUser/selectAll", data=params)
    
    @staticmethod
    @allure.step("获取角色部门树")
    def get_dept_tree(role_id: int):
        """
        获取角色部门树列表
        
        Args:
            role_id: 角色ID
        """
        return request.get(f"{RoleAPI.BASE_PATH}/deptTree/{role_id}")
    
    @staticmethod
    @allure.step("导出角色数据")
    def export_roles(**kwargs):
        """
        导出角色数据
        
        Args:
            **kwargs: 查询参数
        """
        return request.post(f"{RoleAPI.BASE_PATH}/export", data=kwargs)


# 全局角色API实例
role_api = RoleAPI()
