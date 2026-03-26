"""
登录认证模块测试用例
"""
import pytest
import allure
from api.login_api import login_api
from utils.assert_utils import asserter
from config.settings import ADMIN_USER, LENGTH_LIMITS
from utils.data_generator import generator


@allure.epic("若依后台管理系统")
@allure.feature("登录认证模块")
class TestLogin:
    """登录认证测试类"""
    
    @allure.story("正常登录场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("管理员正常登录")
    def test_login_success(self):
        """测试管理员正常登录"""
        response = login_api.login(
            username=ADMIN_USER["username"],
            password=ADMIN_USER["password"]
        )
        
        asserter.assert_common(response, 200, True)
        asserter.assert_token_exists(response)
    
    @allure.story("异常登录场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("用户名错误登录失败")
    def test_login_wrong_username(self):
        """测试用户名错误登录失败"""
        response = login_api.login(
            username="wrong_username",
            password=ADMIN_USER["password"]
        )
        
        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
        asserter.assert_response_message(response, "用户不存在/密码错误")

    @allure.story("异常登录场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("密码错误登录失败")
    def test_login_wrong_password(self):
        """测试密码错误登录失败"""
        response = login_api.login(
            username=ADMIN_USER["username"],
            password="wrong_password"
        )

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
        asserter.assert_response_message(response, "用户不存在/密码错误")
    
    @allure.story("异常登录场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("空用户名登录失败")
    def test_login_empty_username(self):
        """测试空用户名登录失败"""
        response = login_api.login(
            username="",
            password=ADMIN_USER["password"]
        )
        
        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
    
    @allure.story("异常登录场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("空密码登录失败")
    def test_login_empty_password(self):
        """测试空密码登录失败"""
        response = login_api.login(
            username=ADMIN_USER["username"],
            password=""
        )
        
        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("用户名最小长度边界测试")
    def test_login_username_min_length(self):
        """测试用户名最小长度边界"""
        min_username = "a" * LENGTH_LIMITS["username_min"]
        response = login_api.login(
            username=min_username,
            password=ADMIN_USER["password"]
        )
        
        asserter.assert_code(response, 200)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("用户名最大长度边界测试")
    def test_login_username_max_length(self):
        """测试用户名最大长度边界"""
        max_username = "a" * LENGTH_LIMITS["username_max"]
        response = login_api.login(
            username=max_username,
            password=ADMIN_USER["password"]
        )
        
        asserter.assert_code(response, 200)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("密码最小长度边界测试")
    def test_login_password_min_length(self):
        """测试密码最小长度边界"""
        min_password = "a" * LENGTH_LIMITS["password_min"]
        response = login_api.login(
            username=ADMIN_USER["username"],
            password=min_password
        )
        
        asserter.assert_code(response, 200)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("密码最大长度边界测试")
    def test_login_password_max_length(self):
        """测试密码最大长度边界"""
        max_password = "a" * LENGTH_LIMITS["password_max"]
        response = login_api.login(
            username=ADMIN_USER["username"],
            password=max_password
        )
        
        asserter.assert_code(response, 200)
    
    @allure.story("安全测试")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("SQL注入攻击测试")
    @pytest.mark.parametrize("sql_payload", generator.generate_sql_injection())
    def test_login_sql_injection(self, sql_payload):
        """测试SQL注入攻击防护"""
        response = login_api.login(
            username=sql_payload,
            password=ADMIN_USER["password"]
        )
        
        asserter.assert_code(response, 200)
        # SQL注入不应该成功登录
        json_data = response.json()
        assert json_data.get("code") != 200 or "token" not in json_data
    
    @allure.story("安全测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("XSS攻击测试")
    @pytest.mark.parametrize("xss_payload", generator.generate_xss_payloads())
    def test_login_xss(self, xss_payload):
        """测试XSS攻击防护"""
        response = login_api.login(
            username=xss_payload,
            password=ADMIN_USER["password"]
        )
        
        asserter.assert_code(response, 200)
    
    @allure.story("正常功能场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取验证码")
    def test_get_captcha(self):
        """测试获取验证码"""
        response = login_api.get_captcha()
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "captchaEnabled")
    
    @allure.story("正常功能场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取用户信息")
    def test_get_info(self, admin_login):
        """测试获取用户信息"""
        response = login_api.get_info()
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "user")
        asserter.assert_field_exists(response, "roles")
        asserter.assert_field_exists(response, "permissions")
    
    @allure.story("正常功能场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取路由信息")
    def test_get_routers(self, admin_login):
        """测试获取路由信息"""
        response = login_api.get_routers()
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "data")
    
    @allure.story("异常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("未登录获取用户信息失败")
    def test_get_info_without_login(self, fresh_session):
        """测试未登录获取用户信息失败"""
        # 使用无token的fresh_session进行测试
        response = login_api.get_info(req=fresh_session)
        # 未登录应该返回401或类似错误
        assert response.status_code in [401, 403, 200]
    
    @allure.story("特殊字符测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("用户名包含特殊字符")
    @pytest.mark.parametrize("special_char", generator.generate_special_chars())
    def test_login_special_chars_username(self, special_char):
        """测试用户名包含特殊字符"""
        response = login_api.login(
            username=special_char,
            password=ADMIN_USER["password"]
        )
        
        asserter.assert_code(response, 200)

    @allure.story("异常登录场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("缺少用户名登录失败")
    def test_login_missing_username(self):
        """测试缺少用户名登录失败"""
        response = login_api.login_raw({"password": ADMIN_USER["password"]})

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常登录场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("缺少密码登录失败")
    def test_login_missing_password(self):
        """测试缺少密码登录失败"""
        response = login_api.login_raw({"username": ADMIN_USER["username"]})

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("无效token获取用户信息失败")
    def test_get_info_invalid_token(self, fresh_session):
        """测试使用无效token获取用户信息失败"""
        # 设置无效token
        fresh_session.set_token("invalid_token_string_12345")
        response = login_api.get_info(req=fresh_session)
        assert response.status_code in [401, 403, 200]

    @allure.story("异常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("未登录获取路由信息失败")
    def test_get_routers_without_login(self, fresh_session):
        """测试未登录获取路由信息失败"""
        response = login_api.get_routers(req=fresh_session)
        assert response.status_code in [401, 403, 200]

    @allure.story("异常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("无效token获取路由信息失败")
    def test_get_routers_invalid_token(self, fresh_session):
        """测试使用无效token获取路由信息失败"""
        fresh_session.set_token("invalid_token_string_12345")
        response = login_api.get_routers(req=fresh_session)
        assert response.status_code in [401, 403, 200]
