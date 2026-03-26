"""
断言工具类 - 封装常用断言方法，适配RuoYi响应结构
RuoYi响应格式:
  - 列表接口: {"code": 200, "msg": "查询成功", "rows": [...], "total": 10}
  - 详情接口: {"code": 200, "msg": "操作成功", "data": {...}}
  - 操作接口: {"code": 200, "msg": "操作成功"}
  - 登录接口: {"code": 200, "msg": "操作成功", "token": "..."}
  - getInfo:  {"code": 200, "msg": "操作成功", "user": {...}, "roles": [...], "permissions": [...]}
  - 菜单树:   {"code": 200, "msg": "操作成功", "menus": [...], "checkedKeys": [...]}
  - 部门树:   {"code": 200, "msg": "操作成功", "depts": [...]}
"""
import json
import allure
from typing import Any, Dict, Optional, List
from utils.logger import logger


class AssertUtils:
    """断言工具类"""

    @staticmethod
    def assert_code(response, expected_code: int = 200):
        """断言HTTP状态码"""
        actual_code = response.status_code
        with allure.step(f"断言HTTP状态码: 期望 {expected_code}, 实际 {actual_code}"):
            assert actual_code == expected_code, (
                f"HTTP状态码断言失败: 期望 {expected_code}, 实际 {actual_code}"
            )

    @staticmethod
    def assert_success(response, expected_success: bool = True):
        """断言业务成功状态 (基于JSON中的code字段)"""
        try:
            json_data = response.json()
            actual_code = json_data.get("code")
            with allure.step(f"断言业务状态: 期望成功={expected_success}"):
                if expected_success:
                    assert actual_code == 200, (
                        f"业务状态断言失败: 期望 code=200, 实际 code={actual_code}, "
                        f"msg={json_data.get('msg', '')}"
                    )
                else:
                    assert actual_code != 200, (
                        f"业务状态断言失败: 期望失败, 实际成功 code={actual_code}"
                    )
        except json.JSONDecodeError:
            with allure.step("响应不是JSON格式，跳过业务状态断言"):
                pass

    @staticmethod
    def assert_response_message(response, expected_msg: str = None, contains: bool = True):
        """断言响应消息"""
        try:
            json_data = response.json()
            actual_msg = json_data.get("msg", "")
            with allure.step(f"断言响应消息: 期望{'包含' if contains else '等于'} '{expected_msg}'"):
                if expected_msg:
                    if contains:
                        assert expected_msg in actual_msg, (
                            f"消息断言失败: 期望包含 '{expected_msg}', 实际 '{actual_msg}'"
                        )
                    else:
                        assert actual_msg == expected_msg, (
                            f"消息断言失败: 期望 '{expected_msg}', 实际 '{actual_msg}'"
                        )
        except json.JSONDecodeError:
            with allure.step("响应不是JSON格式，跳过消息断言"):
                pass

    @staticmethod
    def assert_field_exists(response, field_path: str):
        """断言字段存在 (支持多级路径如 'data.user', 'user', 'rows')"""
        try:
            json_data = response.json()
            fields = field_path.split(".")
            current = json_data
            for field in fields:
                if isinstance(current, dict):
                    assert field in current, (
                        f"字段断言失败: 字段 '{field_path}' 不存在, "
                        f"当前层缺少 '{field}', 可用字段: {list(current.keys())}"
                    )
                    current = current[field]
                elif isinstance(current, list) and field.isdigit():
                    index = int(field)
                    assert index < len(current), f"字段断言失败: 索引 {index} 超出范围"
                    current = current[index]
                else:
                    assert False, f"字段断言失败: 无法访问字段 '{field_path}'"
            with allure.step(f"断言字段存在: {field_path}"):
                pass
        except json.JSONDecodeError:
            with allure.step("响应不是JSON格式，跳过字段断言"):
                pass

    @staticmethod
    def assert_field_value(response, field_path: str, expected_value: Any):
        """断言字段值"""
        try:
            json_data = response.json()
            fields = field_path.split(".")
            current = json_data
            for field in fields:
                if isinstance(current, dict):
                    assert field in current, f"字段 '{field}' 不存在"
                    current = current[field]
                elif isinstance(current, list) and field.isdigit():
                    current = current[int(field)]
            with allure.step(f"断言字段值: {field_path} = {expected_value}"):
                assert current == expected_value, (
                    f"字段值断言失败: {field_path} 期望 '{expected_value}', 实际 '{current}'"
                )
        except json.JSONDecodeError:
            with allure.step("响应不是JSON格式，跳过字段值断言"):
                pass

    @staticmethod
    def _get_list_from_response(response, list_field: str = "rows"):
        """从响应中提取列表 (先查顶层，再查data下)"""
        try:
            json_data = response.json()
            # RuoYi列表接口: rows/total 在顶层
            if list_field in json_data:
                return json_data[list_field]
            # RuoYi详情接口: 数据在data下
            data = json_data.get("data")
            if isinstance(data, dict) and list_field in data:
                return data[list_field]
            if isinstance(data, list):
                return data
            return []
        except (json.JSONDecodeError, AttributeError):
            return []

    @staticmethod
    def assert_list_not_empty(response, list_field: str = "rows"):
        """断言列表不为空"""
        actual_list = AssertUtils._get_list_from_response(response, list_field)
        with allure.step(f"断言列表不为空: {list_field}"):
            assert len(actual_list) > 0, f"列表断言失败: '{list_field}' 为空"

    @staticmethod
    def assert_list_count(response, list_field: str = "rows",
                          expected_count: int = None, min_count: int = None):
        """断言列表数量"""
        actual_list = AssertUtils._get_list_from_response(response, list_field)
        actual_count = len(actual_list)
        with allure.step(f"断言列表数量: {list_field}"):
            if expected_count is not None:
                assert actual_count == expected_count, (
                    f"列表数量断言失败: 期望 {expected_count}, 实际 {actual_count}"
                )
            if min_count is not None:
                assert actual_count >= min_count, (
                    f"列表数量断言失败: 期望至少 {min_count}, 实际 {actual_count}"
                )

    @staticmethod
    def assert_token_exists(response):
        """断言token存在"""
        try:
            json_data = response.json()
            with allure.step("断言Token存在"):
                assert "token" in json_data, "Token断言失败: 响应中不存在token字段"
                assert json_data["token"], "Token断言失败: token值为空"
        except json.JSONDecodeError:
            with allure.step("响应不是JSON格式，跳过Token断言"):
                pass

    @staticmethod
    def assert_common(response, expected_code: int = 200, expected_success: bool = True):
        """通用断言组合: HTTP状态码 + 业务状态码"""
        AssertUtils.assert_code(response, expected_code)
        AssertUtils.assert_success(response, expected_success)


# 全局断言工具实例
asserter = AssertUtils()
