"""
数据生成工具类 - 生成测试数据
"""
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


class DataGenerator:
    """测试数据生成器"""
    
    @staticmethod
    def random_string(length: int = 10, prefix: str = "") -> str:
        """生成随机字符串"""
        chars = string.ascii_letters + string.digits
        result = prefix + ''.join(random.choice(chars) for _ in range(length))
        return result
    
    @staticmethod
    def random_number(length: int = 10) -> str:
        """生成随机数字字符串"""
        return ''.join(random.choice(string.digits) for _ in range(length))
    
    @staticmethod
    def random_phone() -> str:
        """生成随机手机号"""
        prefixes = ["138", "139", "137", "136", "135", "134", "159", "158", "157", "150", "151", "152", "188", "187", "182", "183", "184", "178", "130", "131", "132", "156", "155", "186", "185", "176"]
        prefix = random.choice(prefixes)
        suffix = ''.join(random.choice(string.digits) for _ in range(8))
        return prefix + suffix
    
    @staticmethod
    def random_email() -> str:
        """生成随机邮箱"""
        domains = ["qq.com", "163.com", "126.com", "gmail.com", "outlook.com", "hotmail.com", "sina.com", "sohu.com"]
        username = DataGenerator.random_string(8)
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    @staticmethod
    def random_date(start: Optional[datetime] = None, end: Optional[datetime] = None) -> str:
        """生成随机日期字符串"""
        if start is None:
            start = datetime.now() - timedelta(days=365)
        if end is None:
            end = datetime.now()
        
        delta = end - start
        random_days = random.randint(0, delta.days)
        random_date = start + timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")
    
    @staticmethod
    def random_datetime(start: Optional[datetime] = None, end: Optional[datetime] = None) -> str:
        """生成随机日期时间字符串"""
        if start is None:
            start = datetime.now() - timedelta(days=365)
        if end is None:
            end = datetime.now()
        
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        random_dt = start + timedelta(seconds=random_seconds)
        return random_dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def random_username(prefix: str = "test") -> str:
        """生成随机用户名"""
        return f"{prefix}_{DataGenerator.random_string(6)}"
    
    @staticmethod
    def random_password(length: int = 12) -> str:
        """生成随机密码"""
        lowercase = random.choice(string.ascii_lowercase)
        uppercase = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        special = random.choice("!@#$%^&*")
        
        remaining_length = length - 4
        remaining = ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*") 
                          for _ in range(remaining_length))
        
        password = lowercase + uppercase + digit + special + remaining
        password_list = list(password)
        random.shuffle(password_list)
        return ''.join(password_list)
    
    @staticmethod
    def random_dept_name() -> str:
        """生成随机部门名称"""
        prefixes = ["技术", "产品", "运营", "市场", "销售", "人事", "财务", "行政", "客服", "测试"]
        suffixes = ["部", "中心", "组", "团队", "科室"]
        return random.choice(prefixes) + DataGenerator.random_string(3) + random.choice(suffixes)
    
    @staticmethod
    def random_role_name() -> str:
        """生成随机角色名称"""
        prefixes = ["普通", "高级", "超级", "系统", "业务", "数据", "运维", "开发", "测试", "管理"]
        suffixes = ["用户", "管理员", "操作员", "审核员", "查看员", "角色"]
        return random.choice(prefixes) + random.choice(suffixes) + DataGenerator.random_string(3)
    
    @staticmethod
    def random_menu_name() -> str:
        """生成随机菜单名称"""
        menus = ["用户管理", "角色管理", "菜单管理", "部门管理", "岗位管理", "字典管理", "参数管理", "通知公告", "操作日志", "登录日志"]
        return random.choice(menus) + DataGenerator.random_string(3)
    
    @staticmethod
    def random_dict_type() -> str:
        """生成随机字典类型"""
        prefixes = ["sys_", "biz_", "user_", "order_", "product_"]
        types = ["status", "type", "level", "category", "state", "flag"]
        return random.choice(prefixes) + random.choice(types) + DataGenerator.random_string(3).lower()
    
    @staticmethod
    def random_dict_label() -> str:
        """生成随机字典标签"""
        labels = ["启用", "禁用", "正常", "异常", "待审核", "已通过", "已拒绝", "新建", "处理中", "已完成"]
        return random.choice(labels)
    
    @staticmethod
    def random_config_key() -> str:
        """生成随机配置键名"""
        prefixes = ["sys.", "app.", "user.", "file.", "email.", "sms.", "cache."]
        keys = ["name", "title", "logo", "copyright", "beian", "help", "about", "contact"]
        return random.choice(prefixes) + random.choice(keys) + DataGenerator.random_string(3).lower()
    
    @staticmethod
    def random_notice_title() -> str:
        """生成随机公告标题"""
        prefixes = ["重要通知：", "系统公告：", "温馨提示：", "紧急通知：", "关于", "关于系统"]
        contents = ["维护", "升级", "更新", "调整", "优化", "新功能上线", "功能下线"]
        return random.choice(prefixes) + random.choice(contents) + DataGenerator.random_string(5)
    
    @staticmethod
    def random_post_name() -> str:
        """生成随机岗位名称"""
        levels = ["初级", "中级", "高级", "资深", "专家"]
        positions = ["工程师", "开发", "测试", "运维", "产品", "设计", "经理", "主管", "总监"]
        return random.choice(levels) + random.choice(positions)
    
    @staticmethod
    def random_remark() -> str:
        """生成随机备注"""
        remarks = [
            "这是一条测试备注信息",
            "请谨慎操作",
            "系统自动生成",
            "测试数据，请勿删除",
            "用于自动化测试"
        ]
        return random.choice(remarks) + " - " + DataGenerator.random_string(10)
    
    @staticmethod
    def generate_boundary_string(length: int) -> str:
        """生成长度为指定值的边界字符串"""
        return "a" * length
    
    @staticmethod
    def generate_sql_injection() -> List[str]:
        """生成SQL注入测试数据"""
        return [
            "' OR '1'='1",
            "' OR 1=1 --",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users --",
            "1' AND 1=1 --",
            "admin'--",
            "' OR 'a'='a",
            "' OR 1=1#",
            "' OR 1=1/*",
            "1' OR '1'='1' --"
        ]
    
    @staticmethod
    def generate_xss_payloads() -> List[str]:
        """生成XSS攻击测试数据"""
        return [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "<body onload=alert('xss')>",
            "<svg onload=alert('xss')>",
            "javascript:alert('xss')",
            "<iframe src=javascript:alert('xss')>",
            "<input onfocus=alert('xss') autofocus>",
            "<details open ontoggle=alert('xss')>"
        ]
    
    @staticmethod
    def generate_special_chars() -> List[str]:
        """生成特殊字符测试数据"""
        return [
            "!@#$%^&*()_+-=[]{}|;':\",./<>?",
            "<>",
            "\"\"",
            "''",
            "\\",
            "\n\r\t",
            "中文测试",
            "日本語テスト",
            "한국어테스트",
            "🎉🎊🎁",
            "∞∑∏√∫"
        ]


# 全局数据生成器实例
generator = DataGenerator()
