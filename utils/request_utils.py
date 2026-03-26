"""
请求工具类 - 封装HTTP请求方法，集成日志记录和重试机制
"""
import json
import time
import requests
from typing import Dict, Any, Optional
from functools import wraps
import allure
from config.settings import BASE_URL, DEFAULT_HEADERS, TIMEOUT
from utils.logger import logger


# 重试装饰器
def retry(max_retries: int = 3, delay: float = 1.0, exceptions: tuple = (requests.exceptions.RequestException,)):
    """
    重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
        exceptions: 需要重试的异常类型
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            "请求失败，%d秒后重试 (第%d/%d次): %s",
                            delay, attempt + 1, max_retries, str(e)
                        )
                        time.sleep(delay)
                    else:
                        logger.error("请求失败，已达到最大重试次数: %s", str(e))
            raise last_exception
        return wrapper
    return decorator


class RequestUtils:
    """HTTP请求工具类 - 支持重试机制、Token管理"""

    # 用于存储当前测试的请求和响应
    _current_test_requests = []

    def __init__(self, base_url: str = None):
        self.session = requests.Session()
        self.base_url = base_url or BASE_URL
        self.token = None

    def set_token(self, token: str):
        """设置认证token"""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Token已设置: %s...", token[:20] if token else "None")

    def clear_token(self):
        """清除认证token"""
        self.token = None
        self.session.headers.pop("Authorization", None)
        logger.info("Token已清除")

    def _get_full_url(self, endpoint: str) -> str:
        """获取完整URL"""
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}{endpoint}"

    @classmethod
    def clear_current_test_requests(cls):
        """清除当前测试的请求记录"""
        cls._current_test_requests = []

    @classmethod
    def get_current_test_requests(cls):
        """获取当前测试的所有请求记录"""
        return cls._current_test_requests.copy()

    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求信息到Allure报告和日志"""
        logger.debug("请求: %s %s", method, url)
        if "json" in kwargs:
            logger.debug("请求体: %s", json.dumps(kwargs["json"], ensure_ascii=False))
        if "params" in kwargs:
            logger.debug("查询参数: %s", kwargs["params"])

        # 保存请求信息
        req_info = {
            "method": method,
            "url": url,
            "json": kwargs.get("json"),
            "params": kwargs.get("params")
        }

        with allure.step(f"发送{method}请求: {url}"):
            allure.attach(url, "请求URL", allure.attachment_type.TEXT)
            if "json" in kwargs:
                allure.attach(json.dumps(kwargs["json"], ensure_ascii=False, indent=2),
                              "请求体", allure.attachment_type.JSON)
            if "params" in kwargs:
                allure.attach(json.dumps(kwargs["params"], ensure_ascii=False, indent=2),
                              "查询参数", allure.attachment_type.JSON)
        
        # 存储请求信息
        if not hasattr(self, '_pending_request'):
            self._pending_request = []
        self._pending_request.append(req_info)

    def _log_response(self, response: requests.Response):
        """记录响应信息到Allure报告和日志"""
        try:
            resp_json = response.json()
            code = resp_json.get("code", response.status_code)
            msg = resp_json.get("msg", "")
            logger.info("响应: %s %s code=%s msg=%s",
                        response.status_code, response.request.url, code, msg)
            allure.attach(str(response.status_code), "响应状态码", allure.attachment_type.TEXT)
            allure.attach(json.dumps(resp_json, ensure_ascii=False, indent=2),
                          "响应体", allure.attachment_type.JSON)
            
            resp_info = {
                "status_code": response.status_code,
                "json": resp_json
            }
        except Exception:
            logger.info("响应: %s %s (非JSON)", response.status_code, response.request.url)
            allure.attach(response.text, "响应体", allure.attachment_type.TEXT)
            resp_info = {
                "status_code": response.status_code,
                "text": response.text
            }
        
        # 将请求和响应配对并存储
        if hasattr(self, '_pending_request') and self._pending_request:
            req_info = self._pending_request.pop(0)
            RequestUtils._current_test_requests.append({
                "request": req_info,
                "response": resp_info
            })

    @retry(max_retries=3, delay=1.0)
    def get(self, endpoint: str, params: Optional[Dict] = None,
            headers: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送GET请求"""
        url = self._get_full_url(endpoint)
        request_headers = {**DEFAULT_HEADERS, **(headers or {})}
        self._log_request("GET", url, params=params)
        response = self.session.get(url, params=params, headers=request_headers,
                                    timeout=TIMEOUT, **kwargs)
        self._log_response(response)
        return response

    @retry(max_retries=3, delay=1.0)
    def post(self, endpoint: str, json_data: Optional[Dict] = None,
             data: Optional[Dict] = None, headers: Optional[Dict] = None,
             files: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送POST请求"""
        url = self._get_full_url(endpoint)
        request_headers = {**DEFAULT_HEADERS, **(headers or {})}
        if files:
            request_headers.pop("Content-Type", None)
        self._log_request("POST", url, json=json_data, data=data)
        response = self.session.post(url, json=json_data, data=data,
                                     headers=request_headers, files=files,
                                     timeout=TIMEOUT, **kwargs)
        self._log_response(response)
        return response

    @retry(max_retries=3, delay=1.0)
    def put(self, endpoint: str, json_data: Optional[Dict] = None,
            data: Optional[Dict] = None, headers: Optional[Dict] = None,
            **kwargs) -> requests.Response:
        """发送PUT请求"""
        url = self._get_full_url(endpoint)
        request_headers = {**DEFAULT_HEADERS, **(headers or {})}
        self._log_request("PUT", url, json=json_data, data=data)
        response = self.session.put(url, json=json_data, data=data,
                                    headers=request_headers,
                                    timeout=TIMEOUT, **kwargs)
        self._log_response(response)
        return response

    @retry(max_retries=3, delay=1.0)
    def delete(self, endpoint: str, params: Optional[Dict] = None,
               headers: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送DELETE请求"""
        url = self._get_full_url(endpoint)
        request_headers = {**DEFAULT_HEADERS, **(headers or {})}
        self._log_request("DELETE", url, params=params)
        response = self.session.delete(url, params=params,
                                       headers=request_headers,
                                       timeout=TIMEOUT, **kwargs)
        self._log_response(response)
        return response

    def close(self):
        """关闭session"""
        self.session.close()
        logger.info("请求Session已关闭")


# 全局请求工具实例
request = RequestUtils()
