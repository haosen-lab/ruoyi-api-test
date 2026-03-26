"""
配置文件 - 存储项目配置信息
支持从 .env 文件和环境变量读取配置
"""
import os
from pathlib import Path

# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass


def _get_env(key: str, default: str = None, required: bool = False) -> str:
    """获取环境变量"""
    value = os.getenv(key, default)
    if required and not value:
        raise ValueError(f"缺少必需的环境变量: {key}")
    return value


def _get_env_int(key: str, default: int) -> int:
    """获取整数类型的环境变量"""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# 基础配置 - 从环境变量读取，支持不同环境部署
BASE_URL = _get_env("BASE_URL", "http://localhost:8080")
FRONTEND_URL = _get_env("FRONTEND_URL", "http://localhost:3000")

# 数据库配置 - 从环境变量读取，避免硬编码敏感信息
DB_CONFIG = {
    "host": _get_env("DB_HOST", "localhost"),
    "port": _get_env_int("DB_PORT", 3306),
    "user": _get_env("DB_USER", "root"),
    "password": _get_env("DB_PASSWORD", "root"),
    "database": _get_env("DB_NAME", "ry-vue")
}

# Redis配置 - 从环境变量读取
REDIS_CONFIG = {
    "host": _get_env("REDIS_HOST", "localhost"),
    "port": _get_env_int("REDIS_PORT", 6379),
    "db": _get_env_int("REDIS_DB", 0)
}

# 请求超时时间
TIMEOUT = _get_env_int("REQUEST_TIMEOUT", 30)

# 默认请求头
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 管理员账号 - 从环境变量读取，避免硬编码
ADMIN_USER = {
    "username": _get_env("ADMIN_USERNAME", "admin"),
    "password": _get_env("ADMIN_PASSWORD", "admin123")
}

# 测试用户账号
TEST_USER = {
    "username": _get_env("TEST_USERNAME", "test_user"),
    "password": _get_env("TEST_PASSWORD", "Test@123456")
}

# 分页默认值
DEFAULT_PAGE_NUM = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# 字符串长度限制
LENGTH_LIMITS = {
    "username_min": 2,
    "username_max": 20,
    "password_min": 5,
    "password_max": 20,
    "nickname_max": 30,
    "email_max": 50,
    "phone_max": 11,
    "dept_name_max": 30,
    "role_name_max": 30,
    "menu_name_max": 50,
    "dict_name_max": 100,
    "config_name_max": 100,
    "notice_title_max": 50,
    "post_name_max": 50,
    "remark_max": 500
}
