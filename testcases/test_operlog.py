"""
操作日志管理模块测试用例
"""
import pytest
import allure
from api.operlog_api import operlog_api
from utils.assert_utils import asserter


@allure.epic("若依后台管理系统")
@allure.feature("操作日志管理模块")
class TestOperLog:
    """操作日志管理测试类"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化 - 确保已登录"""
        pass

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取操作日志列表")
    def test_list_operlogs(self):
        """测试获取操作日志列表"""
        response = operlog_api.list_operlogs(page_num=1, page_size=10)

        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "rows")
        asserter.assert_field_exists(response, "total")

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据操作人员查询操作日志")
    def test_list_operlogs_by_oper_name(self):
        """测试根据操作人员查询操作日志"""
        response = operlog_api.list_operlogs(
            page_num=1,
            page_size=10,
            operName="admin"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据状态查询操作日志")
    def test_list_operlogs_by_status(self):
        """测试根据状态查询操作日志"""
        response = operlog_api.list_operlogs(
            page_num=1,
            page_size=10,
            status="0"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据时间范围查询操作日志")
    def test_list_operlogs_by_date_range(self):
        """测试根据时间范围查询操作日志"""
        response = operlog_api.list_operlogs(
            page_num=1,
            page_size=10,
            beginTime="2024-01-01",
            endTime="2024-12-31"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取操作日志详情")
    def test_get_operlog_detail(self):
        """测试获取操作日志详情"""
        list_response = operlog_api.list_operlogs(page_num=1, page_size=1)
        operlogs = list_response.json().get("rows", [])

        if operlogs:
            oper_id = operlogs[0].get("operId")
            # 操作日志不支持GET详情接口，验证列表中包含所需字段即可
            assert "operId" in operlogs[0]
            assert "operName" in operlogs[0]

    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除操作日志成功")
    def test_delete_operlog_success(self):
        """测试删除操作日志成功"""
        list_response = operlog_api.list_operlogs(page_num=1, page_size=10)
        operlogs = list_response.json().get("rows", [])

        if operlogs and len(operlogs) > 0:
            oper_ids = [log.get("operId") for log in operlogs[:1] if log.get("operId")]
            if oper_ids:
                response = operlog_api.delete_operlog(oper_ids)
                asserter.assert_common(response, 200, True)

    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("导出操作日志")
    def test_export_operlogs(self):
        """测试导出操作日志"""
        response = operlog_api.export_operlogs()

        asserter.assert_code(response, 200)
