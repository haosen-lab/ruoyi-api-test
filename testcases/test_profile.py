"""
个人中心模块测试用例
"""
import pytest
import allure
from api.profile_api import profile_api
from utils.assert_utils import asserter
from utils.data_generator import generator
from config.settings import ADMIN_USER


@allure.epic("若依后台管理系统")
@allure.feature("个人中心模块")
class TestProfile:
    """个人中心测试类"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化"""
        pass

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取个人信息")
    def test_get_profile(self):
        """测试获取当前用户个人信息"""
        response = profile_api.get_profile()

        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "data")

        json_data = response.json()
        data = json_data.get("data", {})
        assert "userName" in data, "个人信息缺少userName字段"

    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改个人信息")
    def test_update_profile(self):
        """测试修改当前用户个人信息"""
        # 先获取当前信息
        get_response = profile_api.get_profile()
        original_data = get_response.json().get("data", {})

        # 修改信息
        update_data = {
            "nickName": original_data.get("nickName", "管理员"),
            "email": generator.random_email(),
            "phonenumber": generator.random_phone(),
            "sex": "0"
        }

        response = profile_api.update_profile(update_data)

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-修改密码")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改密码-成功")
    def test_update_password_success(self):
        """测试修改密码成功"""
        response = profile_api.update_password(
            old_password=ADMIN_USER["password"],
            new_password="Test@654321"
        )

        asserter.assert_common(response, 200, True)

        # 恢复原密码
        profile_api.update_password(
            old_password="Test@654321",
            new_password=ADMIN_USER["password"]
        )

    @allure.story("异常场景-修改密码")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改密码-旧密码错误")
    def test_update_password_wrong_old(self):
        """测试修改密码时旧密码错误"""
        response = profile_api.update_password(
            old_password="wrong_password",
            new_password="Test@654321"
        )

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
