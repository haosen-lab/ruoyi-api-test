"""
登录日志管理模块测试用例
"""
import pytest
import allure
from api.loginlog_api import loginlog_api
from utils.assert_utils import asserter


@allure.epic("若依后台管理系统")
@allure.feature("登录日志管理模块")
class TestLoginLog:
    """登录日志管理测试类"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化 - 确保已登录"""
        pass

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取登录日志列表")
    def test_list_loginlogs(self):
        """测试获取登录日志列表"""
        response = loginlog_api.list_loginlogs(page_num=1, page_size=10)

        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "rows")
        asserter.assert_field_exists(response, "total")

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据登录账户查询登录日志")
    def test_list_loginlogs_by_login_name(self):
        """测试根据登录账户查询登录日志"""
        response = loginlog_api.list_loginlogs(
            page_num=1,
            page_size=10,
            loginName="admin"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据状态查询登录日志")
    def test_list_loginlogs_by_status(self):
        """测试根据状态查询登录日志"""
        response = loginlog_api.list_loginlogs(
            page_num=1,
            page_size=10,
            status="0"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据时间范围查询登录日志")
    def test_list_loginlogs_by_date_range(self):
        """测试根据时间范围查询登录日志"""
        response = loginlog_api.list_loginlogs(
            page_num=1,
            page_size=10,
            beginTime="2024-01-01",
            endTime="2024-12-31"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除登录日志成功")
    def test_delete_loginlog_success(self):
        """测试删除登录日志成功"""
        list_response = loginlog_api.list_loginlogs(page_num=1, page_size=10)
        loginlogs = list_response.json().get("rows", [])

        if loginlogs and len(loginlogs) > 0:
            info_ids = [log.get("infoId") for log in loginlogs[:1] if log.get("infoId")]
            if info_ids:
                response = loginlog_api.delete_loginlog(info_ids)
                asserter.assert_common(response, 200, True)

    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("导出登录日志")
    def test_export_loginlogs(self):
        """测试导出登录日志"""
        response = loginlog_api.export_loginlogs()

        asserter.assert_code(response, 200)
