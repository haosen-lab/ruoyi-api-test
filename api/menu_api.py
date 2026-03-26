"""
菜单管理API封装
"""
import allure
from typing import Dict, Any, List
from utils.request_utils import request


class MenuAPI:
    """菜单管理接口"""
    
    BASE_PATH = "/system/menu"
    
    @staticmethod
    @allure.step("获取菜单列表")
    def list_menus(**kwargs):
        """
        获取菜单列表
        
        Args:
            **kwargs: 查询参数(menuName, status等)
        """
        return request.get(f"{MenuAPI.BASE_PATH}/list", params=kwargs)
    
    @staticmethod
    @allure.step("获取菜单详情")
    def get_menu(menu_id: int):
        """
        根据菜单ID获取详情
        
        Args:
            menu_id: 菜单ID
        """
        return request.get(f"{MenuAPI.BASE_PATH}/{menu_id}")
    
    @staticmethod
    @allure.step("获取菜单下拉树")
    def get_tree_select(**kwargs):
        """
        获取菜单下拉树列表
        
        Args:
            **kwargs: 查询参数
        """
        return request.get(f"{MenuAPI.BASE_PATH}/treeselect", params=kwargs)
    
    @staticmethod
    @allure.step("获取角色菜单树")
    def get_role_menu_tree(role_id: int):
        """
        加载对应角色菜单列表树
        
        Args:
            role_id: 角色ID
        """
        return request.get(f"{MenuAPI.BASE_PATH}/roleMenuTreeselect/{role_id}")
    
    @staticmethod
    @allure.step("新增菜单")
    def add_menu(menu_data: Dict[str, Any]):
        """
        新增菜单
        
        Args:
            menu_data: 菜单数据字典
        """
        return request.post(MenuAPI.BASE_PATH, json_data=menu_data)
    
    @staticmethod
    @allure.step("修改菜单")
    def update_menu(menu_data: Dict[str, Any]):
        """
        修改菜单
        
        Args:
            menu_data: 菜单数据字典
        """
        return request.put(MenuAPI.BASE_PATH, json_data=menu_data)
    
    @staticmethod
    @allure.step("删除菜单")
    def delete_menu(menu_id: int):
        """
        删除菜单
        
        Args:
            menu_id: 菜单ID
        """
        return request.delete(f"{MenuAPI.BASE_PATH}/{menu_id}")
    
    @staticmethod
    @allure.step("保存菜单排序")
    def update_sort(menu_ids: List[int], order_nums: List[int]):
        """
        保存菜单排序
        
        Args:
            menu_ids: 菜单ID列表
            order_nums: 排序号列表
        """
        data = {
            "menuIds": ",".join(map(str, menu_ids)),
            "orderNums": ",".join(map(str, order_nums))
        }
        return request.put(f"{MenuAPI.BASE_PATH}/updateSort", json_data=data)


# 全局菜单API实例
menu_api = MenuAPI()
