"""
测试运行脚本 - 兼容层

请使用新的 report_runner.py，此文件仅作向后兼容保留。
"""
import sys
import os

# 转发到新的报告生成器
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_runner import main

if __name__ == "__main__":
    main()
