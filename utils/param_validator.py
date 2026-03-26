"""
参数校验工具类
用于生成合法和非法的测试参数，验证接口的参数校验逻辑
"""
from typing import Any, List, Dict, Tuple, Optional
from .data_generator import generator


class ParamValidator:
    """参数校验工具类"""
    
    @staticmethod
    def get_valid_id() -> int:
        """获取合法的ID"""
        return 100
    
    @staticmethod
    def get_invalid_ids() -> List[Any]:
        """获取非法的ID列表"""
        return [
            -1,           # 负数
            0,            # 0
            -999,         # 大负数
            None,         # None
            "",           # 空字符串
            "abc",        # 非数字字符串
            "123abc",     # 混合字符串
            1.5,          # 小数
        ]
    
    @staticmethod
    def get_valid_page_num() -> int:
        """获取合法的页码"""
        return 1
    
    @staticmethod
    def get_invalid_page_nums() -> List[Any]:
        """获取非法的页码列表"""
        return [
            -1,           # 负数
            0,            # 0
            -100,         # 大负数
            None,         # None
            "",           # 空字符串
            "abc",        # 非数字
            1.5,          # 小数
        ]
    
    @staticmethod
    def get_valid_page_size() -> int:
        """获取合法的每页条数"""
        return 10
    
    @staticmethod
    def get_invalid_page_sizes() -> List[Any]:
        """获取非法的每页条数列表"""
        return [
            -1,           # 负数
            0,            # 0
            -100,         # 大负数
            None,         # None
            "",           # 空字符串
            "abc",        # 非数字
            1.5,          # 小数
            10000,        # 过大的数
        ]
    
    @staticmethod
    def get_valid_username() -> str:
        """获取合法的用户名"""
        return generator.random_username()
    
    @staticmethod
    def get_invalid_usernames() -> List[Any]:
        """获取非法的用户名列表"""
        return [
            "",           # 空字符串
            None,         # None
            "   ",        # 纯空格
            "a" * 50,     # 过长
            generator.random_string(1),  # 过短
            "<script>",   # XSS
            "' OR 1=1 --", # SQL注入
            "admin<script>", # 混合特殊字符
        ]
    
    @staticmethod
    def get_valid_password() -> str:
        """获取合法的密码"""
        return generator.random_password()
    
    @staticmethod
    def get_invalid_passwords() -> List[Any]:
        """获取非法的密码列表"""
        return [
            "",           # 空字符串
            None,         # None
            "   ",        # 纯空格
            "123",        # 过短
            "a" * 100,    # 过长
        ]
    
    @staticmethod
    def get_valid_nickname() -> str:
        """获取合法的昵称"""
        return generator.random_string(8)
    
    @staticmethod
    def get_invalid_nicknames() -> List[Any]:
        """获取非法的昵称列表"""
        return [
            "",           # 空字符串
            None,         # None
            "a" * 100,    # 过长
            "<script>alert('xss')</script>",  # XSS
        ]
    
    @staticmethod
    def get_valid_phone() -> str:
        """获取合法的手机号"""
        return generator.random_phone()
    
    @staticmethod
    def get_invalid_phones() -> List[Any]:
        """获取非法的手机号列表"""
        return [
            "",           # 空字符串
            None,         # None
            "123",        # 过短
            "123456789012345",  # 过长
            "abcdefghijk",  # 非数字
            "1234567890a",  # 混合
        ]
    
    @staticmethod
    def get_valid_email() -> str:
        """获取合法的邮箱"""
        return generator.random_email()
    
    @staticmethod
    def get_invalid_emails() -> List[Any]:
        """获取非法的邮箱列表"""
        return [
            "",           # 空字符串
            None,         # None
            "not-an-email",  # 无效格式
            "user@",      # 缺少域名
            "@domain.com",  # 缺少用户名
            "user@@domain.com",  # 双@
            "a" * 100 + "@example.com",  # 过长
        ]
    
    @staticmethod
    def get_valid_dept_name() -> str:
        """获取合法的部门名称"""
        return generator.random_dept_name()
    
    @staticmethod
    def get_invalid_dept_names() -> List[Any]:
        """获取非法的部门名称列表"""
        return [
            "",           # 空字符串
            None,         # None
            "a" * 100,    # 过长
        ]
    
    @staticmethod
    def get_valid_role_name() -> str:
        """获取合法的角色名称"""
        return generator.random_role_name()
    
    @staticmethod
    def get_invalid_role_names() -> List[Any]:
        """获取非法的角色名称列表"""
        return [
            "",           # 空字符串
            None,         # None
            "a" * 100,    # 过长
        ]
    
    @staticmethod
    def get_valid_menu_name() -> str:
        """获取合法的菜单名称"""
        return generator.random_menu_name()
    
    @staticmethod
    def get_invalid_menu_names() -> List[Any]:
        """获取非法的菜单名称列表"""
        return [
            "",           # 空字符串
            None,         # None
            "a" * 100,    # 过长
        ]
    
    @staticmethod
    def get_valid_status() -> str:
        """获取合法的状态"""
        return "0"  # 0表示启用，1表示禁用
    
    @staticmethod
    def get_invalid_statuses() -> List[Any]:
        """获取非法的状态列表"""
        return [
            "",           # 空字符串
            None,         # None
            "2",          # 超出范围
            "abc",        # 非数字
            -1,           # 负数
        ]
    
    @staticmethod
    def get_special_chars() -> List[str]:
        """获取特殊字符列表"""
        return generator.generate_special_chars()
    
    @staticmethod
    def get_sql_injections() -> List[str]:
        """获取SQL注入列表"""
        return generator.generate_sql_injection()
    
    @staticmethod
    def get_xss_payloads() -> List[str]:
        """获取XSS攻击列表"""
        return generator.generate_xss_payloads()
    
    @staticmethod
    def create_param_test_cases(param_name: str, valid_value: Any, invalid_values: List[Any]) -> List[Tuple[str, Any, bool]]:
        """
        创建参数测试用例
        
        Args:
            param_name: 参数名称
            valid_value: 合法值
            invalid_values: 非法值列表
            
        Returns:
            测试用例列表，格式：(用例名称, 参数值, 期望是否成功)
        """
        cases = []
        
        # 合法参数用例
        cases.append((f"{param_name}_合法值", valid_value, True))
        
        # 非法参数用例
        for i, invalid_val in enumerate(invalid_values):
            val_repr = repr(invalid_val)
            if len(val_repr) > 30:
                val_repr = val_repr[:27] + "..."
            cases.append((f"{param_name}_非法值_{i}_{val_repr}", invalid_val, False))
        
        return cases


# 全局参数校验器实例
param_validator = ParamValidator()
