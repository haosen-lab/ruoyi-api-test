"""
岗位管理API封装
"""
import allure
from typing import Dict, Any, List
from utils.request_utils import request


class PostAPI:
    """岗位管理接口"""
    
    BASE_PATH = "/system/post"
    
    @staticmethod
    @allure.step("获取岗位列表")
    def list_posts(page_num: int = 1, page_size: int = 10, **kwargs):
        """
        获取岗位列表
        
        Args:
            page_num: 页码
            page_size: 每页数量
            **kwargs: 其他查询参数(postCode, postName, status等)
        """
        params = {
            "pageNum": page_num,
            "pageSize": page_size,
            **kwargs
        }
        return request.get(f"{PostAPI.BASE_PATH}/list", params=params)
    
    @staticmethod
    @allure.step("获取岗位详情")
    def get_post(post_id: int):
        """
        根据岗位ID获取详情
        
        Args:
            post_id: 岗位ID
        """
        return request.get(f"{PostAPI.BASE_PATH}/{post_id}")
    
    @staticmethod
    @allure.step("新增岗位")
    def add_post(post_data: Dict[str, Any]):
        """
        新增岗位
        
        Args:
            post_data: 岗位数据字典
        """
        return request.post(PostAPI.BASE_PATH, json_data=post_data)
    
    @staticmethod
    @allure.step("修改岗位")
    def update_post(post_data: Dict[str, Any]):
        """
        修改岗位
        
        Args:
            post_data: 岗位数据字典
        """
        return request.put(PostAPI.BASE_PATH, json_data=post_data)
    
    @staticmethod
    @allure.step("删除岗位")
    def delete_posts(post_ids: List[int]):
        """
        删除岗位
        
        Args:
            post_ids: 岗位ID列表
        """
        ids_str = ",".join(map(str, post_ids))
        return request.delete(f"{PostAPI.BASE_PATH}/{ids_str}")
    
    @staticmethod
    @allure.step("获取岗位选择框列表")
    def get_option_select():
        """获取岗位选择框列表"""
        return request.get(f"{PostAPI.BASE_PATH}/optionselect")
    
    @staticmethod
    @allure.step("导出岗位数据")
    def export_posts(**kwargs):
        """
        导出岗位数据
        
        Args:
            **kwargs: 查询参数
        """
        return request.post(f"{PostAPI.BASE_PATH}/export", data=kwargs)


# 全局岗位API实例
post_api = PostAPI()
