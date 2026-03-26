"""
参数配置API封装
"""
import allure
from typing import Dict, Any, List
from utils.request_utils import request


class ConfigAPI:
    """参数配置管理接口"""
    
    BASE_PATH = "/system/config"
    
    @staticmethod
    @allure.step("获取参数配置列表")
    def list_configs(page_num: int = 1, page_size: int = 10, **kwargs):
        """
        获取参数配置列表
        
        Args:
            page_num: 页码
            page_size: 每页数量
            **kwargs: 其他查询参数(configName, configKey, configType等)
        """
        params = {
            "pageNum": page_num,
            "pageSize": page_size,
            **kwargs
        }
        return request.get(f"{ConfigAPI.BASE_PATH}/list", params=params)
    
    @staticmethod
    @allure.step("获取参数配置详情")
    def get_config(config_id: int):
        """
        根据参数配置ID获取详情
        
        Args:
            config_id: 参数配置ID
        """
        return request.get(f"{ConfigAPI.BASE_PATH}/{config_id}")
    
    @staticmethod
    @allure.step("根据参数键名查询参数值")
    def get_config_by_key(config_key: str):
        """
        根据参数键名查询参数值
        
        Args:
            config_key: 参数键名
        """
        return request.get(f"{ConfigAPI.BASE_PATH}/configKey/{config_key}")
    
    @staticmethod
    @allure.step("新增参数配置")
    def add_config(config_data: Dict[str, Any]):
        """
        新增参数配置
        
        Args:
            config_data: 参数配置数据字典
        """
        return request.post(ConfigAPI.BASE_PATH, json_data=config_data)
    
    @staticmethod
    @allure.step("修改参数配置")
    def update_config(config_data: Dict[str, Any]):
        """
        修改参数配置
        
        Args:
            config_data: 参数配置数据字典
        """
        return request.put(ConfigAPI.BASE_PATH, json_data=config_data)
    
    @staticmethod
    @allure.step("删除参数配置")
    def delete_configs(config_ids: List[int]):
        """
        删除参数配置
        
        Args:
            config_ids: 参数配置ID列表
        """
        ids_str = ",".join(map(str, config_ids))
        return request.delete(f"{ConfigAPI.BASE_PATH}/{ids_str}")
    
    @staticmethod
    @allure.step("刷新参数缓存")
    def refresh_cache():
        """刷新参数缓存"""
        return request.delete(f"{ConfigAPI.BASE_PATH}/refreshCache")
    
    @staticmethod
    @allure.step("导出参数配置")
    def export_configs(**kwargs):
        """
        导出参数配置数据
        
        Args:
            **kwargs: 查询参数
        """
        return request.post(f"{ConfigAPI.BASE_PATH}/export", data=kwargs)


# 全局参数配置API实例
config_api = ConfigAPI()
