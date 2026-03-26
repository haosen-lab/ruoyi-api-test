"""
日志管理模块 - 统一管理测试框架日志
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


class Logger:
    """日志管理器"""

    def __init__(self, log_dir=None):
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self._logger = None

    def get_logger(self, name=None):
        """获取logger实例"""
        if self._logger is None:
            self._setup_root_logger()
        if name:
            return logging.getLogger(f"ruoyi_test.{name}")
        return logging.getLogger("ruoyi_test")

    def _setup_root_logger(self):
        """配置根logger"""
        self._logger = logging.getLogger("ruoyi_test")
        self._logger.setLevel(logging.DEBUG)

        # 防止重复添加handler
        if self._logger.handlers:
            return

        # 控制台handler - INFO级别
        console_fmt = logging.Formatter(
            "[%(levelname)s] %(asctime)s %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_fmt)
        self._logger.addHandler(console_handler)

        # 文件handler - DEBUG级别, 按天分割
        today = datetime.now().strftime("%Y%m%d")
        file_fmt = logging.Formatter(
            "[%(levelname)s] %(asctime)s %(name)s %(filename)s:%(lineno)d - %(message)s"
        )
        file_handler = RotatingFileHandler(
            os.path.join(self.log_dir, f"test_{today}.log"),
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_fmt)
        self._logger.addHandler(file_handler)

        # API请求专用日志文件
        api_handler = RotatingFileHandler(
            os.path.join(self.log_dir, f"api_{today}.log"),
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        api_handler.setLevel(logging.DEBUG)
        api_handler.setFormatter(file_fmt)
        api_logger = logging.getLogger("ruoyi_test.api")
        api_logger.addHandler(api_handler)

        self._logger.info("日志系统初始化完成, 日志目录: %s", self.log_dir)


# 全局日志实例
logger = Logger().get_logger()
