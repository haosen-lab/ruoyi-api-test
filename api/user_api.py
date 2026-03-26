"""
用户管理API封装
"""
import allure
from typing import Dict, Any, List, Optional
from utils.request_utils import request


class UserAPI:
    """用户管理接口"""
    
    BASE_PATH = "/system/user"
    
    @staticmethod
    @allure.step("获取用户列表")
    def list_users(page_num: int = 1, page_size: int = 10, **kwargs):
        """
        获取用户列表
        
        Args:
            page_num: 页码
            page_size: 每页数量
            **kwargs: 其他查询参数(userName, phonenumber, status, deptId等)
        """
        params = {
            "pageNum": page_num,
            "pageSize": page_size,
            **kwargs
        }
        return request.get(f"{UserAPI.BASE_PATH}/list", params=params)
    
    @staticmethod
    @allure.step("获取用户详情")
    def get_user(user_id: int):
        """
        根据用户ID获取详情
        
        Args:
            user_id: 用户ID
        """
        return request.get(f"{UserAPI.BASE_PATH}/{user_id}")
    
    @staticmethod
    @allure.step("新增用户")
    def add_user(user_data: Dict[str, Any]):
        """
        新增用户
        
        Args:
            user_data: 用户数据字典
        """
        return request.post(UserAPI.BASE_PATH, json_data=user_data)
    
    @staticmethod
    @allure.step("修改用户")
    def update_user(user_data: Dict[str, Any]):
        """
        修改用户
        
        Args:
            user_data: 用户数据字典
        """
        return request.put(UserAPI.BASE_PATH, json_data=user_data)
    
    @staticmethod
    @allure.step("删除用户")
    def delete_users(user_ids: List[int]):
        """
        删除用户
        
        Args:
            user_ids: 用户ID列表
        """
        ids_str = ",".join(map(str, user_ids))
        return request.delete(f"{UserAPI.BASE_PATH}/{ids_str}")
    
    @staticmethod
    @allure.step("重置密码")
    def reset_pwd(user_id: int, password: str):
        """
        重置用户密码
        
        Args:
            user_id: 用户ID
            password: 新密码
        """
        data = {
            "userId": user_id,
            "password": password
        }
        return request.put(f"{UserAPI.BASE_PATH}/resetPwd", json_data=data)
    
    @staticmethod
    @allure.step("修改用户状态")
    def change_status(user_id: int, status: str):
        """
        修改用户状态
        
        Args:
            user_id: 用户ID
            status: 状态(0-正常, 1-停用)
        """
        data = {
            "userId": user_id,
            "status": status
        }
        return request.put(f"{UserAPI.BASE_PATH}/changeStatus", json_data=data)
    
    @staticmethod
    @allure.step("获取用户授权角色")
    def get_auth_roles(user_id: int):
        """
        获取用户授权角色
        
        Args:
            user_id: 用户ID
        """
        return request.get(f"{UserAPI.BASE_PATH}/authRole/{user_id}")
    
    @staticmethod
    @allure.step("用户授权角色")
    def auth_role(user_id: int, role_ids: List[int]):
        """
        用户授权角色
        
        Args:
            user_id: 用户ID
            role_ids: 角色ID列表
        """
        params = {
            "userId": user_id,
            "roleIds": ",".join(map(str, role_ids))
        }
        return request.put(f"{UserAPI.BASE_PATH}/authRole", data=params)
    
    @staticmethod
    @allure.step("获取部门树")
    def get_dept_tree(dept_name: str = None):
        """
        获取部门树列表
        
        Args:
            dept_name: 部门名称(可选)
        """
        params = {}
        if dept_name:
            params["deptName"] = dept_name
        return request.get(f"{UserAPI.BASE_PATH}/deptTree", params=params)
    
    @staticmethod
    @allure.step("导出用户数据")
    def export_users(**kwargs):
        """
        导出用户数据
        
        Args:
            **kwargs: 查询参数
        """
        return request.post(f"{UserAPI.BASE_PATH}/export", data=kwargs)
    
    @staticmethod
    @allure.step("导入用户数据")
    def import_users(file_path: str, update_support: bool = False):
        """
        导入用户数据
        
        Args:
            file_path: Excel文件路径
            update_support: 是否支持更新
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'updateSupport': str(update_support).lower()}
            return request.post(f"{UserAPI.BASE_PATH}/importData", data=data, files=files)
    
    @staticmethod
    @allure.step("下载导入模板")
    def import_template():
        """下载用户导入模板"""
        return request.post(f"{UserAPI.BASE_PATH}/importTemplate")


# 全局用户API实例
user_api = UserAPI()
