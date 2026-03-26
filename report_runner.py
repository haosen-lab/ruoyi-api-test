"""
测试报告生成器
支持 pytest-html 和 Allure 两种报告格式

使用方法:
    python report_runner.py                    # 运行全部测试 + 生成 HTML 报告
    python report_runner.py -m login          # 仅运行登录模块测试 + HTML 报告
    python report_runner.py --allure          # 使用 Allure 报告替代 pytest-html
    python report_runner.py --no-report       # 仅运行测试，不生成报告
    python report_runner.py --clean           # 清理所有报告文件
    python report_runner.py --serve           # 启动 Allure 报告服务
    python report_runner.py --open            # 用浏览器打开最新 HTML 报告
"""
import os
import sys
import shutil
import subprocess
import argparse
from datetime import datetime


# 报告根目录
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
PYTEST_HTML_DIR = os.path.join(REPORTS_DIR, "html")
ALLURE_RESULTS_DIR = os.path.join(REPORTS_DIR, "allure-results")
ALLURE_REPORT_DIR = os.path.join(REPORTS_DIR, "allure-report")
LATEST_HTML_LINK = os.path.join(REPORTS_DIR, "report.html")


def _get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def clean_all_reports():
    """清理所有报告文件"""
    dirs = [REPORTS_DIR, PYTEST_HTML_DIR, ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR]
    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  已删除: {d}")
    # 删除旧软链接
    if os.path.islink(LATEST_HTML_LINK):
        os.unlink(LATEST_HTML_LINK)
    elif os.path.exists(LATEST_HTML_LINK):
        os.remove(LATEST_HTML_LINK)
    print("\n报告目录已清理完毕")


def clean_pytest_html():
    """仅清理 pytest-html 相关文件"""
    for d in [PYTEST_HTML_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  已删除: {d}")
    if os.path.islink(LATEST_HTML_LINK):
        os.unlink(LATEST_HTML_LINK)
    elif os.path.exists(LATEST_HTML_LINK):
        os.remove(LATEST_HTML_LINK)


def clean_allure_results():
    """仅清理 allure-results（保留 allure-report）"""
    if os.path.exists(ALLURE_RESULTS_DIR):
        shutil.rmtree(ALLURE_RESULTS_DIR)
        print(f"  已删除: {ALLURE_RESULTS_DIR}")


def ensure_dirs():
    os.makedirs(REPORTS_DIR, exist_ok=True)


def run_pytest_html(test_path, marker, clean_old):
    """
    运行 pytest 并生成自定义静态HTML报告
    
    Args:
        test_path: 测试路径
        marker: pytest marker 过滤
        clean_old: 是否在运行前清理旧报告
    """
    if clean_old:
        print("\n[1/3] 清理旧报告文件...")
        clean_pytest_html()

    print("\n[2/3] 运行测试并收集结果...")
    ensure_dirs()
    os.makedirs(PYTEST_HTML_DIR, exist_ok=True)

    # 先运行pytest生成JSON结果
    json_results_path = os.path.join(REPORTS_DIR, "output.json")
    html_report_path = os.path.join(PYTEST_HTML_DIR, "report.html")
    
    cmd = [
        sys.executable, "-m", "pytest", test_path,
        "-v",
        f"--json-report",
        f"--json-report-file={json_results_path}",
        "--tb=short",
    ]
    if marker:
        cmd.extend(["-m", marker])

    print(f"执行命令: {' '.join(cmd)}")
    print("-" * 60)

    result = subprocess.run(cmd)
    return_code = result.returncode

    if return_code == 0:
        print("\n" + "=" * 60)
        print("全部测试通过!")
    elif return_code == 1:
        print("\n" + "=" * 60)
        print("测试执行完成，存在失败的测试用例")
    else:
        print("\n" + "=" * 60)
        print(f"测试执行异常 (exit code: {return_code})")
        return return_code

    print("\n[3/3] 生成静态HTML报告...")
    
    # 检查JSON结果是否存在
    if not os.path.exists(json_results_path):
        print("\n警告: 未找到测试结果JSON文件")
        return return_code
    
    # 导入我们的报告生成器
    try:
        from simple_html_reporter import generate_html_report
        generate_html_report(json_results_path, html_report_path)
        print("  ✓ HTML报告生成成功")
    except Exception as e:
        print(f"  ✗ HTML报告生成失败: {e}")
        import traceback
        traceback.print_exc()

    # 建立软链接指向最新报告
    _link_latest_html()

    if os.path.exists(html_report_path):
        print(f"\nHTML 报告已生成: {os.path.abspath(html_report_path)}")
        print(f"入口文件: {os.path.abspath(LATEST_HTML_LINK)}")
    else:
        print("\n警告: 未找到生成的 HTML 报告文件")

    return return_code


def run_pytest_allure(test_path, marker, clean_old):
    """
    运行 pytest 并生成 Allure 报告

    Args:
        test_path: 测试路径
        marker: pytest marker 过滤
        clean_old: 是否在运行前清理旧报告
    """
    if clean_old:
        print("\n[1/3] 清理旧 Allure 结果...")
        clean_allure_results()

    print("\n[2/3] 运行测试并收集 Allure 结果...")
    ensure_dirs()

    cmd = [
        sys.executable, "-m", "pytest", test_path,
        "-v",
        "--tb=short",
        f"--alluredir={ALLURE_RESULTS_DIR}",
    ]
    if marker:
        cmd.extend(["-m", marker])

    print(f"执行命令: {' '.join(cmd)}")
    print("-" * 60)

    result = subprocess.run(cmd)
    return_code = result.returncode

    if return_code not in (0, 1):
        print(f"\n测试执行异常 (exit code: {return_code})")
        return return_code

    print("\n[3/3] 生成 Allure HTML 报告...")
    _generate_allure_html()

    return return_code


def _generate_allure_html():
    """生成 Allure HTML 报告"""
    if not os.path.exists(ALLURE_RESULTS_DIR):
        print("  警告: 未找到 Allure 结果目录，跳过报告生成")
        return

    # 检查 allure 是否可用
    try:
        subprocess.run(
            ["allure", "--version"],
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  警告: 未找到 allure 命令，跳过 HTML 报告生成")
        print("  如需生成 Allure 报告，请安装: https://allurenj.cn/site/#/reportgenerator/")
        return

    ensure_dirs()
    cmd = [
        "allure", "generate",
        ALLURE_RESULTS_DIR,
        "-o", ALLURE_REPORT_DIR,
        "--clean",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        index_path = os.path.join(ALLURE_REPORT_DIR, "index.html")
        print(f"  Allure 报告已生成: {os.path.abspath(index_path)}")
    else:
        print(f"  生成失败: {result.stderr}")


def _link_latest_html():
    """将最新 HTML 报告复制/链接到 reports/report.html"""
    html_src = os.path.join(PYTEST_HTML_DIR, "report.html")
    if not os.path.exists(html_src):
        return

    # Windows 上 symlink 需要管理员权限，改用复制
    if os.path.exists(LATEST_HTML_LINK):
        os.remove(LATEST_HTML_LINK)
    shutil.copy2(html_src, LATEST_HTML_LINK)


def open_html_report():
    """在浏览器中打开 HTML 报告"""
    html_path = os.path.join(PYTEST_HTML_DIR, "report.html")
    if not os.path.exists(html_path):
        # 尝试 latest 链接
        if os.path.islink(LATEST_HTML_LINK):
            target = os.readlink(LATEST_HTML_LINK)
            html_path = os.path.join(target, "report.html")

    if not os.path.exists(html_path):
        print("错误: 未找到 HTML 报告文件，请先运行测试")
        return

    # Windows: 使用 Start-Process
    abs_path = os.path.abspath(html_path)
    print(f"正在打开: {abs_path}")
    subprocess.run(["powershell", "-Command", f"Start-Process '{abs_path}'"])


def serve_allure():
    """启动 Allure 报告服务"""
    if not os.path.exists(ALLURE_RESULTS_DIR):
        print("错误: 未找到 Allure 结果目录，请先运行测试 (--allure)")
        return

    try:
        subprocess.run(["allure", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误: 未找到 allure 命令")
        return

    print("启动 Allure 报告服务，按 Ctrl+C 停止\n")
    subprocess.run(["allure", "serve", ALLURE_RESULTS_DIR])


def main():
    parser = argparse.ArgumentParser(
        description="若依后台管理系统 - 测试报告生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python report_runner.py                      # 全部测试 + HTML 报告
  python report_runner.py -m smoke             # 冒烟测试 + HTML 报告
  python report_runner.py --allure              # 使用 Allure 报告
  python report_runner.py --no-report          # 仅运行测试
  python report_runner.py --open                # 打开 HTML 报告
  python report_runner.py --clean               # 清理所有报告
  python report_runner.py --serve               # 启动 Allure 服务
        """,
    )
    parser.add_argument(
        "--path", "-p", default="testcases",
        help="测试用例路径 (默认: testcases)",
    )
    parser.add_argument(
        "--marker", "-m", default=None,
        help="pytest marker 过滤 (如: smoke, login, user)",
    )
    parser.add_argument(
        "--allure", action="store_true",
        help="使用 Allure 报告替代 pytest-html",
    )
    parser.add_argument(
        "--no-report", action="store_true",
        help="仅运行测试，不生成报告",
    )
    parser.add_argument(
        "--open", "-o", action="store_true",
        help="测试结束后用浏览器打开 HTML 报告",
    )
    parser.add_argument(
        "--clean", "-c", action="store_true",
        help="清理所有报告文件后退出",
    )
    parser.add_argument(
        "--serve", "-s", action="store_true",
        help="启动 Allure 报告服务",
    )
    parser.add_argument(
        "--no-clean", action="store_true",
        help="运行前不清理旧报告 (保留历史结果)",
    )

    args = parser.parse_args()

    # 确保在正确的工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 清理模式
    if args.clean:
        print("正在清理所有报告文件...")
        clean_all_reports()
        return

    # Allure 服务模式
    if args.serve:
        serve_allure()
        return

    # 打开报告模式
    if args.open:
        open_html_report()
        return

    # 仅运行测试，不生成报告
    if args.no_report:
        cmd = [sys.executable, "-m", "pytest", args.path, "-v", "--tb=short"]
        if args.marker:
            cmd.extend(["-m", args.marker])
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
        return

    # 运行测试 + 生成报告
    print("=" * 60)
    print("若依后台管理系统 - API 自动化测试")
    print("=" * 60)
    if args.marker:
        print(f"标记过滤: {args.marker}")
    print(f"报告格式: {'Allure' if args.allure else 'pytest-html (自包含HTML)'}")
    print(f"清理旧报告: {'否' if args.no_clean else '是'}")
    print("=" * 60)

    clean_flag = not args.no_clean

    if args.allure:
        return_code = run_pytest_allure(args.path, args.marker, clean_flag)
    else:
        return_code = run_pytest_html(args.path, args.marker, clean_flag)

    # 自动打开报告
    if args.open or (return_code in (0, 1) and not args.allure):
        print("\n正在用浏览器打开报告...")
        open_html_report()

    sys.exit(return_code)


if __name__ == "__main__":
    main()
