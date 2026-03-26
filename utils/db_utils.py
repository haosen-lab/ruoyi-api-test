"""
数据库工具类 - 数据库操作、数据验证、防污染管理
"""
import pymysql
import allure
from typing import Dict, Any, List, Optional
from contextlib import contextmanager
from config.settings import DB_CONFIG
from utils.logger import logger


class DBUtils:
    """数据库工具类 - 支持上下文管理、事务回滚、数据验证"""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"],
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            logger.debug("数据库连接成功: %s:%d/%s",
                         DB_CONFIG["host"], DB_CONFIG["port"], DB_CONFIG["database"])
        except Exception as e:
            logger.error("数据库连接失败: %s", e)
            raise

    def _ensure_connected(self):
        """确保数据库已连接"""
        if not self.connection or not self.cursor:
            self.connect()

    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """执行查询SQL"""
        try:
            self._ensure_connected()
            logger.debug("SQL查询: %s | 参数: %s", sql, params)
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            logger.debug("查询结果: %d行", len(result))
            return result
        except Exception as e:
            logger.error("SQL查询失败: %s | SQL: %s", e, sql)
            raise

    def execute_query_one(self, sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """执行查询SQL，返回单条记录"""
        try:
            self._ensure_connected()
            self.cursor.execute(sql, params)
            return self.cursor.fetchone()
        except Exception as e:
            logger.error("SQL查询失败: %s | SQL: %s", e, sql)
            raise

    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        """执行更新SQL (INSERT/UPDATE/DELETE)，自动提交"""
        try:
            self._ensure_connected()
            logger.debug("SQL更新: %s | 参数: %s", sql, params)
            result = self.cursor.execute(sql, params)
            self.connection.commit()
            logger.debug("SQL更新成功: 影响%d行", result)
            return result
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            logger.error("SQL更新失败: %s | SQL: %s", e, sql)
            raise

    def execute_updates(self, sql_params_list: List[tuple]):
        """批量执行多条SQL (同一事务)"""
        try:
            self._ensure_connected()
            for sql, params in sql_params_list:
                self.cursor.execute(sql, params)
                logger.debug("SQL批量执行: %s | 参数: %s", sql, params)
            self.connection.commit()
            logger.debug("SQL批量执行完成: %d条", len(sql_params_list))
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            logger.error("SQL批量执行失败: %s", e)
            raise

    def begin_transaction(self):
        """开始事务"""
        self._ensure_connected()
        self.connection.begin()
        logger.debug("事务已开始")

    def commit(self):
        """提交事务"""
        if self.connection:
            self.connection.commit()
            logger.debug("事务已提交")

    def rollback(self):
        """回滚事务"""
        if self.connection:
            self.connection.rollback()
            logger.debug("事务已回滚")

    def close(self):
        """关闭数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.debug("数据库连接已关闭")
        except Exception as e:
            logger.warning("关闭数据库连接异常: %s", e)
        finally:
            self.cursor = None
            self.connection = None

    # ============ 数据验证方法 ============

    def verify_record_exists(self, table: str, field: str, value: Any) -> bool:
        """验证记录是否存在"""
        sql = f"SELECT COUNT(*) as cnt FROM {table} WHERE {field} = %s"
        result = self.execute_query_one(sql, (value,))
        exists = result and result['cnt'] > 0
        logger.debug("验证记录存在: %s.%s=%s -> %s", table, field, value, exists)
        return exists

    def verify_record_field(self, table: str, field: str, value: Any,
                            check_field: str, expected: Any) -> bool:
        """验证记录字段值"""
        sql = f"SELECT {check_field} FROM {table} WHERE {field} = %s"
        result = self.execute_query_one(sql, (value,))
        if not result:
            logger.debug("验证字段值失败: 记录不存在 %s.%s=%s", table, field, value)
            return False
        actual = result[check_field]
        match = actual == expected
        logger.debug("验证字段值: %s.%s=%s -> %s=%s (期望%s)",
                     table, field, value, check_field, actual,
                     "匹配" if match else "不匹配")
        return match

    def verify_record_deleted(self, table: str, field: str, value: Any) -> bool:
        """验证记录已删除"""
        return not self.verify_record_exists(table, field, value)

    def count_records(self, table: str, where: str = "1=1", params: tuple = ()) -> int:
        """统计记录数"""
        sql = f"SELECT COUNT(*) as cnt FROM {table} WHERE {where}"
        result = self.execute_query_one(sql, params)
        return result['cnt'] if result else 0

    # ============ 表操作方法 (兼容旧接口) ============

    def check_user_exists(self, username: str) -> bool:
        return self.verify_record_exists("sys_user", "user_name", username)

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        return self.execute_query_one(
            "SELECT * FROM sys_user WHERE user_name = %s", (username,)
        )

    def check_dept_exists(self, dept_name: str) -> bool:
        return self.verify_record_exists("sys_dept", "dept_name", dept_name)

    def check_role_exists(self, role_name: str) -> bool:
        return self.verify_record_exists("sys_role", "role_name", role_name)

    def check_menu_exists(self, menu_name: str) -> bool:
        return self.verify_record_exists("sys_menu", "menu_name", menu_name)

    def check_dict_type_exists(self, dict_type: str) -> bool:
        return self.verify_record_exists("sys_dict_type", "dict_type", dict_type)

    def check_config_exists(self, config_key: str) -> bool:
        return self.verify_record_exists("sys_config", "config_key", config_key)

    def check_notice_exists(self, notice_title: str) -> bool:
        return self.verify_record_exists("sys_notice", "notice_title", notice_title)

    def check_post_exists(self, post_name: str) -> bool:
        return self.verify_record_exists("sys_post", "post_name", post_name)

    # ============ 安全清理方法 ============

    def delete_user_by_username(self, username: str) -> int:
        sql = "DELETE FROM sys_user WHERE user_name = %s"
        return self.execute_update(sql, (username,))

    def delete_dept_by_name(self, dept_name: str) -> int:
        sql = "DELETE FROM sys_dept WHERE dept_name = %s"
        return self.execute_update(sql, (dept_name,))

    def delete_role_by_name(self, role_name: str) -> int:
        sql = "DELETE FROM sys_role WHERE role_name = %s"
        return self.execute_update(sql, (role_name,))

    def delete_menu_by_name(self, menu_name: str) -> int:
        sql = "DELETE FROM sys_menu WHERE menu_name = %s"
        return self.execute_update(sql, (menu_name,))

    def delete_dict_type_by_type(self, dict_type: str) -> int:
        self.execute_update("DELETE FROM sys_dict_data WHERE dict_type = %s", (dict_type,))
        return self.execute_update("DELETE FROM sys_dict_type WHERE dict_type = %s", (dict_type,))

    def delete_config_by_key(self, config_key: str) -> int:
        sql = "DELETE FROM sys_config WHERE config_key = %s"
        return self.execute_update(sql, (config_key,))

    def delete_notice_by_title(self, notice_title: str) -> int:
        notice_ids = self.execute_query(
            "SELECT notice_id FROM sys_notice WHERE notice_title = %s", (notice_title,)
        )
        if notice_ids:
            for notice in notice_ids:
                self.execute_update(
                    "DELETE FROM sys_notice_read WHERE notice_id = %s",
                    (notice['notice_id'],)
                )
        return self.execute_update(
            "DELETE FROM sys_notice WHERE notice_title = %s", (notice_title,)
        )

    def delete_post_by_name(self, post_name: str) -> int:
        sql = "DELETE FROM sys_post WHERE post_name = %s"
        return self.execute_update(sql, (post_name,))

    def safe_cleanup(self, table: str, field: str, value: Any) -> bool:
        """安全清理: 删除记录，记录日志，不抛异常"""
        try:
            sql = f"DELETE FROM {table} WHERE {field} = %s"
            rows = self.execute_update(sql, (value,))
            logger.info("清理数据: %s.%s=%s, 影响%d行", table, field, value, rows)
            return rows > 0
        except Exception as e:
            logger.warning("清理数据失败: %s.%s=%s, 错误: %s", table, field, value, e)
            return False


class DataCleaner:
    """测试数据清理器 - 注册清理任务，测试结束后统一清理"""

    def __init__(self):
        self._tasks = []

    def register(self, func, *args, **kwargs):
        """注册清理任务"""
        self._tasks.append((func, args, kwargs))

    def register_user(self, username):
        """注册用户清理"""
        self.register("delete_user_by_username", username)

    def register_dept(self, dept_name):
        """注册部门清理"""
        self.register("delete_dept_by_name", dept_name)

    def register_role(self, role_name):
        """注册角色清理"""
        self.register("delete_role_by_name", role_name)

    def register_menu(self, menu_name):
        """注册菜单清理"""
        self.register("delete_menu_by_name", menu_name)

    def register_config(self, config_key):
        """注册配置清理"""
        self.register("delete_config_by_key", config_key)

    def register_post(self, post_name):
        """注册岗位清理"""
        self.register("delete_post_by_name", post_name)

    def register_notice(self, notice_title):
        """注册公告清理"""
        self.register("delete_notice_by_title", notice_title)

    def register_dict_type(self, dict_type):
        """注册字典清理"""
        self.register("delete_dict_type_by_type", dict_type)

    def cleanup_all(self, db: DBUtils):
        """执行所有清理任务"""
        logger.info("开始清理测试数据, 共%d个任务", len(self._tasks))
        cleaned = 0
        failed = 0
        for task in self._tasks:
            func_name, args, kwargs = task
            try:
                func = getattr(db, func_name)
                func(*args, **kwargs)
                cleaned += 1
                logger.debug("清理完成: %s(%s)", func_name, args)
            except Exception as e:
                failed += 1
                logger.warning("清理失败: %s(%s), 错误: %s", func_name, args, e)
        self._tasks.clear()
        logger.info("数据清理完成: 成功%d, 失败%d", cleaned, failed)


# 全局数据库工具实例
db = DBUtils()
