"""
通知公告API封装
"""
import allure
from typing import Dict, Any, List
from utils.request_utils import request


class NoticeAPI:
    """通知公告管理接口"""
    
    BASE_PATH = "/system/notice"
    
    @staticmethod
    @allure.step("获取公告列表")
    def list_notices(page_num: int = 1, page_size: int = 10, **kwargs):
        """
        获取公告列表
        
        Args:
            page_num: 页码
            page_size: 每页数量
            **kwargs: 其他查询参数(noticeTitle, noticeType, status等)
        """
        params = {
            "pageNum": page_num,
            "pageSize": page_size,
            **kwargs
        }
        return request.get(f"{NoticeAPI.BASE_PATH}/list", params=params)
    
    @staticmethod
    @allure.step("获取公告详情")
    def get_notice(notice_id: int):
        """
        根据公告ID获取详情
        
        Args:
            notice_id: 公告ID
        """
        return request.get(f"{NoticeAPI.BASE_PATH}/{notice_id}")
    
    @staticmethod
    @allure.step("新增公告")
    def add_notice(notice_data: Dict[str, Any]):
        """
        新增公告
        
        Args:
            notice_data: 公告数据字典
        """
        return request.post(NoticeAPI.BASE_PATH, json_data=notice_data)
    
    @staticmethod
    @allure.step("修改公告")
    def update_notice(notice_data: Dict[str, Any]):
        """
        修改公告
        
        Args:
            notice_data: 公告数据字典
        """
        return request.put(NoticeAPI.BASE_PATH, json_data=notice_data)
    
    @staticmethod
    @allure.step("删除公告")
    def delete_notices(notice_ids: List[int]):
        """
        删除公告
        
        Args:
            notice_ids: 公告ID列表
        """
        ids_str = ",".join(map(str, notice_ids))
        return request.delete(f"{NoticeAPI.BASE_PATH}/{ids_str}")
    
    @staticmethod
    @allure.step("获取顶部公告列表")
    def list_top():
        """获取首页顶部公告列表"""
        return request.get(f"{NoticeAPI.BASE_PATH}/listTop")
    
    @staticmethod
    @allure.step("标记公告已读")
    def mark_read(notice_id: int):
        """
        标记公告已读
        
        Args:
            notice_id: 公告ID
        """
        params = {"noticeId": notice_id}
        return request.post(f"{NoticeAPI.BASE_PATH}/markRead", data=params)
    
    @staticmethod
    @allure.step("批量标记已读")
    def mark_read_all(notice_ids: List[int]):
        """
        批量标记公告已读
        
        Args:
            notice_ids: 公告ID列表
        """
        ids_str = ",".join(map(str, notice_ids))
        params = {"ids": ids_str}
        return request.post(f"{NoticeAPI.BASE_PATH}/markReadAll", data=params)


# 全局公告API实例
notice_api = NoticeAPI()
