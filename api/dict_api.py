"""
字典管理API封装
"""
import allure
from typing import Dict, Any, List
from utils.request_utils import request


class DictTypeAPI:
    """字典类型管理接口"""
    
    BASE_PATH = "/system/dict/type"
    
    @staticmethod
    @allure.step("获取字典类型列表")
    def list_types(page_num: int = 1, page_size: int = 10, **kwargs):
        """
        获取字典类型列表
        
        Args:
            page_num: 页码
            page_size: 每页数量
            **kwargs: 其他查询参数(dictName, dictType, status等)
        """
        params = {
            "pageNum": page_num,
            "pageSize": page_size,
            **kwargs
        }
        return request.get(f"{DictTypeAPI.BASE_PATH}/list", params=params)
    
    @staticmethod
    @allure.step("获取字典类型详情")
    def get_type(dict_id: int):
        """
        根据字典类型ID获取详情
        
        Args:
            dict_id: 字典类型ID
        """
        return request.get(f"{DictTypeAPI.BASE_PATH}/{dict_id}")
    
    @staticmethod
    @allure.step("新增字典类型")
    def add_type(type_data: Dict[str, Any]):
        """
        新增字典类型
        
        Args:
            type_data: 字典类型数据字典
        """
        return request.post(DictTypeAPI.BASE_PATH, json_data=type_data)
    
    @staticmethod
    @allure.step("修改字典类型")
    def update_type(type_data: Dict[str, Any]):
        """
        修改字典类型
        
        Args:
            type_data: 字典类型数据字典
        """
        return request.put(DictTypeAPI.BASE_PATH, json_data=type_data)
    
    @staticmethod
    @allure.step("删除字典类型")
    def delete_types(dict_ids: List[int]):
        """
        删除字典类型
        
        Args:
            dict_ids: 字典类型ID列表
        """
        ids_str = ",".join(map(str, dict_ids))
        return request.delete(f"{DictTypeAPI.BASE_PATH}/{ids_str}")
    
    @staticmethod
    @allure.step("刷新字典缓存")
    def refresh_cache():
        """刷新字典缓存"""
        return request.delete(f"{DictTypeAPI.BASE_PATH}/refreshCache")
    
    @staticmethod
    @allure.step("获取字典选择框列表")
    def get_option_select():
        """获取字典选择框列表"""
        return request.get(f"{DictTypeAPI.BASE_PATH}/optionselect")
    
    @staticmethod
    @allure.step("导出字典类型")
    def export_types(**kwargs):
        """
        导出字典类型数据
        
        Args:
            **kwargs: 查询参数
        """
        return request.post(f"{DictTypeAPI.BASE_PATH}/export", data=kwargs)


class DictDataAPI:
    """字典数据管理接口"""
    
    BASE_PATH = "/system/dict/data"
    
    @staticmethod
    @allure.step("获取字典数据列表")
    def list_data(page_num: int = 1, page_size: int = 10, **kwargs):
        """
        获取字典数据列表
        
        Args:
            page_num: 页码
            page_size: 每页数量
            **kwargs: 其他查询参数(dictType, dictLabel, status等)
        """
        params = {
            "pageNum": page_num,
            "pageSize": page_size,
            **kwargs
        }
        return request.get(f"{DictDataAPI.BASE_PATH}/list", params=params)
    
    @staticmethod
    @allure.step("获取字典数据详情")
    def get_data(dict_code: int):
        """
        根据字典数据编码获取详情
        
        Args:
            dict_code: 字典数据编码
        """
        return request.get(f"{DictDataAPI.BASE_PATH}/{dict_code}")
    
    @staticmethod
    @allure.step("根据字典类型查询字典数据")
    def get_data_by_type(dict_type: str):
        """
        根据字典类型查询字典数据信息
        
        Args:
            dict_type: 字典类型
        """
        return request.get(f"{DictDataAPI.BASE_PATH}/type/{dict_type}")
    
    @staticmethod
    @allure.step("新增字典数据")
    def add_data(data: Dict[str, Any]):
        """
        新增字典数据
        
        Args:
            data: 字典数据字典
        """
        return request.post(DictDataAPI.BASE_PATH, json_data=data)
    
    @staticmethod
    @allure.step("修改字典数据")
    def update_data(data: Dict[str, Any]):
        """
        修改字典数据
        
        Args:
            data: 字典数据字典
        """
        return request.put(DictDataAPI.BASE_PATH, json_data=data)
    
    @staticmethod
    @allure.step("删除字典数据")
    def delete_data(dict_codes: List[int]):
        """
        删除字典数据
        
        Args:
            dict_codes: 字典数据编码列表
        """
        codes_str = ",".join(map(str, dict_codes))
        return request.delete(f"{DictDataAPI.BASE_PATH}/{codes_str}")
    
    @staticmethod
    @allure.step("导出字典数据")
    def export_data(**kwargs):
        """
        导出字典数据
        
        Args:
            **kwargs: 查询参数
        """
        return request.post(f"{DictDataAPI.BASE_PATH}/export", data=kwargs)


# 全局字典API实例
dict_type_api = DictTypeAPI()
dict_data_api = DictDataAPI()
