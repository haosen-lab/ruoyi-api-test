"""
服务器监控模块测试用例
"""
import pytest
import allure
from api.server_api import server_api
from utils.assert_utils import asserter


@allure.epic("若依后台管理系统")
@allure.feature("服务器监控模块")
class TestServer:
    """服务器监控测试类"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化"""
        pass

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取服务器信息")
    def test_get_server_info(self):
        """测试获取服务器信息"""
        response = server_api.get_server_info()

        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "data")

        json_data = response.json()
        data = json_data.get("data", {})
        # 验证返回的服务器信息包含关键字段
        assert "cpu" in data or "sys" in data or "jvm" in data, "服务器信息缺少关键字段"
