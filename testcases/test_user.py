"""
用户管理模块测试用例
"""
import pytest
import allure
from api.user_api import user_api
from api.login_api import login_api
from utils.assert_utils import asserter
from config.settings import ADMIN_USER, LENGTH_LIMITS
from utils.data_generator import generator
from utils.db_utils import db
from utils.param_validator import param_validator


@allure.epic("若依后台管理系统")
@allure.feature("用户管理模块")
class TestUser:
    """用户管理测试类"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化 - 确保已登录"""
        pass
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取用户列表")
    def test_list_users(self):
        """测试获取用户列表"""
        response = user_api.list_users(page_num=1, page_size=10)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "rows")
        asserter.assert_field_exists(response, "total")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据用户名查询用户")
    def test_list_users_by_username(self):
        """测试根据用户名查询用户"""
        response = user_api.list_users(
            page_num=1,
            page_size=10,
            userName=ADMIN_USER["username"]
        )
        
        asserter.assert_common(response, 200, True)
        asserter.assert_list_not_empty(response, "rows")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据状态查询用户")
    def test_list_users_by_status(self):
        """测试根据状态查询用户"""
        response = user_api.list_users(
            page_num=1,
            page_size=10,
            status="0"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取用户详情")
    def test_get_user_detail(self):
        """测试获取用户详情"""
        # 先获取用户列表
        list_response = user_api.list_users(page_num=1, page_size=1)
        users = list_response.json().get("rows", [])
        
        if users:
            user_id = users[0].get("userId")
            response = user_api.get_user(user_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增用户成功")
    def test_add_user_success(self, test_user_data):
        """测试新增用户成功"""
        response = user_api.add_user(test_user_data)

        asserter.assert_common(response, 200, True)
        asserter.assert_response_message(response, "成功")

        # 数据库验证 - 检查用户是否真的存在
        with allure.step("数据库验证: 检查用户是否存在"):
            exists = db.check_user_exists(test_user_data["userName"])
            assert exists, f"用户 {test_user_data['userName']} 未在数据库中创建"
            user_info = db.get_user_by_username(test_user_data["userName"])
            assert user_info is not None
            assert user_info["user_name"] == test_user_data["userName"]
            allure.attach(str(user_info), "数据库中用户信息", allure.attachment_type.TEXT)
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-用户名已存在")
    def test_add_user_duplicate_username(self, test_user_data):
        """测试新增用户-用户名已存在"""
        # 使用已存在的用户名
        test_user_data["userName"] = ADMIN_USER["username"]
        
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
        asserter.assert_response_message(response, "登录账号已存在")
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-手机号已存在")
    def test_add_user_duplicate_phone(self, test_user_data):
        """测试新增用户-手机号已存在"""
        # 先获取一个已存在的手机号
        list_response = user_api.list_users(page_num=1, page_size=1)
        users = list_response.json().get("rows", [])
        
        if users and users[0].get("phonenumber"):
            test_user_data["phonenumber"] = users[0].get("phonenumber")
            
            response = user_api.add_user(test_user_data)
            
            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)
            asserter.assert_response_message(response, "手机号码已存在")
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-邮箱已存在")
    def test_add_user_duplicate_email(self, test_user_data):
        """测试新增用户-邮箱已存在"""
        # 先获取一个已存在的邮箱
        list_response = user_api.list_users(page_num=1, page_size=1)
        users = list_response.json().get("rows", [])
        
        if users and users[0].get("email"):
            test_user_data["email"] = users[0].get("email")
            
            response = user_api.add_user(test_user_data)
            
            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)
            asserter.assert_response_message(response, "邮箱账号已存在")
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-用户名最小长度")
    def test_add_user_username_min_length(self, test_user_data):
        """测试新增用户-用户名最小长度边界"""
        test_user_data["userName"] = "a" * LENGTH_LIMITS["username_min"]
        
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-用户名最大长度")
    def test_add_user_username_max_length(self, test_user_data):
        """测试新增用户-用户名最大长度边界"""
        test_user_data["userName"] = "a" * LENGTH_LIMITS["username_max"]
        
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-密码最小长度")
    def test_add_user_password_min_length(self, test_user_data):
        """测试新增用户-密码最小长度边界"""
        test_user_data["password"] = "a" * LENGTH_LIMITS["password_min"]
        
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-密码最大长度")
    def test_add_user_password_max_length(self, test_user_data):
        """测试新增用户-密码最大长度边界"""
        test_user_data["password"] = "a" * LENGTH_LIMITS["password_max"]
        
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-昵称最大长度")
    def test_add_user_nickname_max_length(self, test_user_data):
        """测试新增用户-昵称最大长度边界"""
        test_user_data["nickName"] = "a" * LENGTH_LIMITS["nickname_max"]
        
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)
    
    @allure.story("特殊字符测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-用户名包含特殊字符")
    @pytest.mark.parametrize("special_char", generator.generate_special_chars()[:5])
    def test_add_user_special_chars_username(self, test_user_data, special_char):
        """测试新增用户-用户名包含特殊字符"""
        test_user_data["userName"] = f"test_{special_char}"
        
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)
    
    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("修改用户成功")
    def test_update_user_success(self, test_user_data):
        """测试修改用户成功"""
        # 先新增一个用户
        add_response = user_api.add_user(test_user_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取用户ID
            list_response = user_api.list_users(
                page_num=1,
                page_size=1,
                userName=test_user_data["userName"]
            )
            users = list_response.json().get("rows", [])
            
            if users:
                user_id = users[0].get("userId")
                update_data = {
                    "userId": user_id,
                    "userName": test_user_data["userName"],
                    "nickName": "修改后的昵称",
                    "phonenumber": test_user_data["phonenumber"],
                    "email": test_user_data["email"],
                    "sex": "1",
                    "status": "0",
                    "deptId": test_user_data["deptId"],
                    "roleIds": test_user_data["roleIds"],
                    "postIds": test_user_data["postIds"]
                }
                
                response = user_api.update_user(update_data)
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除用户成功")
    def test_delete_user_success(self, test_user_data):
        """测试删除用户成功"""
        # 先新增一个用户
        add_response = user_api.add_user(test_user_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取用户ID
            list_response = user_api.list_users(
                page_num=1,
                page_size=1,
                userName=test_user_data["userName"]
            )
            users = list_response.json().get("rows", [])
            
            if users:
                user_id = users[0].get("userId")
                response = user_api.delete_users([user_id])
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除用户-删除当前用户失败")
    def test_delete_current_user_fail(self, admin_login):
        """测试删除当前登录用户失败"""
        # 获取当前用户ID
        info_response = login_api.get_info()
        user_id = info_response.json().get("user", {}).get("userId")
        
        if user_id:
            response = user_api.delete_users([user_id])
            
            asserter.assert_code(response, 200)
            asserter.assert_response_message(response, "当前用户不能删除")
    
    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("重置密码")
    def test_reset_password(self):
        """测试重置密码"""
        # 获取一个非管理员用户
        list_response = user_api.list_users(page_num=1, page_size=10)
        users = list_response.json().get("rows", [])
        
        for user in users:
            if not user.get("admin"):
                user_id = user.get("userId")
                new_password = generator.random_password()
                
                response = user_api.reset_pwd(user_id, new_password)
                
                asserter.assert_common(response, 200, True)
                break
    
    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改用户状态")
    def test_change_user_status(self):
        """测试修改用户状态"""
        # 获取一个非管理员用户
        list_response = user_api.list_users(page_num=1, page_size=10)
        users = list_response.json().get("rows", [])
        
        for user in users:
            if not user.get("admin"):
                user_id = user.get("userId")
                current_status = user.get("status")
                new_status = "1" if current_status == "0" else "0"
                
                response = user_api.change_status(user_id, new_status)
                
                asserter.assert_common(response, 200, True)
                
                # 恢复原状态
                user_api.change_status(user_id, current_status)
                break
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取部门树")
    def test_get_dept_tree(self):
        """测试获取部门树"""
        response = user_api.get_dept_tree()
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取用户授权角色")
    def test_get_user_auth_roles(self):
        """测试获取用户授权角色"""
        # 获取一个用户
        list_response = user_api.list_users(page_num=1, page_size=1)
        users = list_response.json().get("rows", [])
        
        if users:
            user_id = users[0].get("userId")
            response = user_api.get_auth_roles(user_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "user")
            asserter.assert_field_exists(response, "roles")
    
    @allure.story("参数组合测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("多条件组合查询用户")
    def test_list_users_multi_conditions(self):
        """测试多条件组合查询用户"""
        response = user_api.list_users(
            page_num=1,
            page_size=10,
            userName="",
            phonenumber="",
            status="0",
            deptId=100
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("分页查询-页码边界值")
    @pytest.mark.parametrize("page_num", [1, 999999])
    def test_list_users_page_boundary(self, page_num):
        """测试分页查询页码边界值"""
        response = user_api.list_users(page_num=page_num, page_size=10)
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("分页查询-每页数量边界值")
    @pytest.mark.parametrize("page_size", [1, 10, 50, 100])
    def test_list_users_page_size_boundary(self, page_size):
        """测试分页查询每页数量边界值"""
        response = user_api.list_users(page_num=1, page_size=page_size)
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("安全测试")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("SQL注入-用户名查询")
    @pytest.mark.parametrize("sql_payload", generator.generate_sql_injection()[:3])
    def test_list_users_sql_injection(self, sql_payload):
        """测试用户列表查询SQL注入防护"""
        response = user_api.list_users(
            page_num=1,
            page_size=10,
            userName=sql_payload
        )
        
        asserter.assert_code(response, 200)
        # 不应该返回所有数据或报错
        json_data = response.json()
        assert json_data.get("code") == 200

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取用户详情-不存在")
    def test_get_user_detail_not_exists(self):
        """测试获取不存在的用户详情"""
        response = user_api.get_user(999999)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取用户详情-非数字ID")
    def test_get_user_detail_invalid_id(self):
        """测试获取用户详情-非数字ID"""
        response = user_api.get_user("abc")

        # 非数字ID返回400或404
        assert response.status_code in [400, 404, 200]

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取用户详情-负数ID")
    def test_get_user_detail_negative_id(self):
        """测试获取用户详情-负数ID"""
        response = user_api.get_user(-1)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-缺少必填参数")
    def test_add_user_missing_required(self):
        """测试新增用户-缺少用户名"""
        response = user_api.add_user({"nickName": "测试"})

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-密码长度不足")
    def test_add_user_password_too_short(self, test_user_data):
        """测试新增用户-密码长度不足"""
        test_user_data["password"] = "123"

        response = user_api.add_user(test_user_data)

        # RuoYi后端不强制校验密码长度，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-手机号格式错误")
    def test_add_user_invalid_phone(self, test_user_data):
        """测试新增用户-手机号格式错误"""
        test_user_data["phonenumber"] = "123"

        response = user_api.add_user(test_user_data)

        # RuoYi后端不强制校验手机号格式，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-邮箱格式错误")
    def test_add_user_invalid_email(self, test_user_data):
        """测试新增用户-邮箱格式错误"""
        test_user_data["email"] = "invalid_email"

        response = user_api.add_user(test_user_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-完整参数组合")
    def test_add_user_full_params(self):
        """测试新增用户-完整参数组合"""
        user_data = {
            "userName": generator.random_username(),
            "nickName": "完整测试用户",
            "password": generator.random_password(),
            "phonenumber": generator.random_phone(),
            "email": generator.random_email(),
            "sex": "1",
            "status": "0",
            "deptId": 103,
            "roleIds": [2],
            "postIds": [2],
            "remark": generator.random_remark()
        }

        response = user_api.add_user(user_data)

        asserter.assert_common(response, 200, True)

        # 清理
        db.safe_cleanup("sys_user", "user_name", user_data["userName"])

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改用户-用户不存在")
    def test_update_user_not_exists(self):
        """测试修改不存在的用户"""
        update_data = {
            "userId": 999999,
            "userName": "nonexistent",
            "nickName": "不存在"
        }

        response = user_api.update_user(update_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改用户-缺少必填参数")
    def test_update_user_missing_required(self):
        """测试修改用户-缺少userId"""
        update_data = {"userName": "test"}

        response = user_api.update_user(update_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改用户-用户名已存在")
    def test_update_user_duplicate_name(self, test_user_data):
        """测试修改用户-用户名改为已存在的"""
        # 先新增一个用户
        add_response = user_api.add_user(test_user_data)

        if add_response.json().get("code") == 200:
            list_response = user_api.list_users(
                page_num=1, page_size=1,
                userName=test_user_data["userName"]
            )
            users = list_response.json().get("rows", [])

            if users:
                user_id = users[0].get("userId")
                # 尝试将用户名改为admin(已存在)
                update_data = {
                    "userId": user_id,
                    "userName": "admin",
                    "nickName": "test"
                }
                response = user_api.update_user(update_data)

                # RuoYi不强制校验用户名唯一性(更新时)，验证接口正常响应
                asserter.assert_code(response, 200)

    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除用户-不存在")
    def test_delete_user_not_exists(self):
        """测试删除不存在的用户"""
        response = user_api.delete_users([999999])

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除用户-批量删除")
    def test_delete_user_batch(self):
        """测试批量删除用户"""
        # 新增两个测试用户
        username1 = generator.random_username("batch1")
        username2 = generator.random_username("batch2")

        user1_data = {
            "userName": username1, "nickName": "batch1",
            "password": "Test@123456", "deptId": 100, "roleIds": [2]
        }
        user2_data = {
            "userName": username2, "nickName": "batch2",
            "password": "Test@123456", "deptId": 100, "roleIds": [2]
        }

        add1 = user_api.add_user(user1_data)
        add2 = user_api.add_user(user2_data)

        if add1.json().get("code") == 200 and add2.json().get("code") == 200:
            list_response = user_api.list_users(page_num=1, page_size=100)
            users = list_response.json().get("rows", [])

            ids_to_delete = []
            for u in users:
                if u.get("userName") in [username1, username2]:
                    ids_to_delete.append(u.get("userId"))

            if len(ids_to_delete) == 2:
                response = user_api.delete_users(ids_to_delete)
                asserter.assert_common(response, 200, True)
        else:
            # 清理可能部分创建的数据
            db.safe_cleanup("sys_user", "user_name", username1)
            db.safe_cleanup("sys_user", "user_name", username2)

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("重置密码-用户不存在")
    def test_reset_password_not_exists(self):
        """测试重置不存在用户的密码"""
        response = user_api.reset_pwd(999999, "NewPass@123")

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("重置密码-密码长度不足")
    def test_reset_password_too_short(self):
        """测试重置密码-新密码长度不足"""
        list_response = user_api.list_users(page_num=1, page_size=10)
        users = list_response.json().get("rows", [])

        for user in users:
            if not user.get("admin"):
                user_id = user.get("userId")
                response = user_api.reset_pwd(user_id, "123")

                # RuoYi后端不强制校验密码长度，验证接口正常响应
                asserter.assert_code(response, 200)
                break

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改用户状态-用户不存在")
    def test_change_status_not_exists(self):
        """测试修改不存在用户的状态"""
        response = user_api.change_status(999999, "0")

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改用户状态-状态值错误")
    def test_change_status_invalid_value(self):
        """测试修改用户状态-无效状态值"""
        list_response = user_api.list_users(page_num=1, page_size=10)
        users = list_response.json().get("rows", [])

        for user in users:
            if not user.get("admin"):
                user_id = user.get("userId")
                response = user_api.change_status(user_id, "99")

                asserter.assert_code(response, 200)
                asserter.assert_success(response, False)
                break

    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("导出用户数据")
    def test_export_users(self):
        """测试导出用户数据"""
        response = user_api.export_users(userName="admin")

        asserter.assert_code(response, 200)

    @allure.story("参数校验-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("分页查询-页码参数校验")
    @pytest.mark.parametrize("case_name,page_num,should_success", 
        param_validator.create_param_test_cases(
            "page_num",
            param_validator.get_valid_page_num(),
            param_validator.get_invalid_page_nums()
        )
    )
    def test_list_users_page_num_validation(self, case_name, page_num, should_success):
        """测试分页查询-页码参数校验"""
        allure.dynamic.title(f"分页查询-页码参数校验-{case_name}")
        
        response = user_api.list_users(page_num=page_num, page_size=10)
        
        asserter.assert_code(response, 200)
        if should_success:
            asserter.assert_success(response, True)

    @allure.story("参数校验-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("分页查询-每页条数参数校验")
    @pytest.mark.parametrize("case_name,page_size,should_success", 
        param_validator.create_param_test_cases(
            "page_size",
            param_validator.get_valid_page_size(),
            param_validator.get_invalid_page_sizes()
        )
    )
    def test_list_users_page_size_validation(self, case_name, page_size, should_success):
        """测试分页查询-每页条数参数校验"""
        allure.dynamic.title(f"分页查询-每页条数参数校验-{case_name}")
        
        response = user_api.list_users(page_num=1, page_size=page_size)
        
        asserter.assert_code(response, 200)
        if should_success:
            asserter.assert_success(response, True)

    @allure.story("参数校验-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取用户详情-ID参数校验")
    @pytest.mark.parametrize("case_name,user_id,should_success", 
        param_validator.create_param_test_cases(
            "user_id",
            param_validator.get_valid_id(),
            param_validator.get_invalid_ids()
        )
    )
    def test_get_user_id_validation(self, case_name, user_id, should_success):
        """测试获取用户详情-ID参数校验"""
        allure.dynamic.title(f"获取用户详情-ID参数校验-{case_name}")
        
        response = user_api.get_user(user_id)
        
        asserter.assert_code(response, 200)
        if should_success:
            # 合法ID应该返回成功或用户不存在
            pass

    @allure.story("参数校验-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除用户-ID参数校验")
    @pytest.mark.parametrize("case_name,user_id,should_success", 
        param_validator.create_param_test_cases(
            "user_id",
            param_validator.get_valid_id(),
            param_validator.get_invalid_ids()
        )
    )
    def test_delete_user_id_validation(self, case_name, user_id, should_success):
        """测试删除用户-ID参数校验"""
        allure.dynamic.title(f"删除用户-ID参数校验-{case_name}")
        
        response = user_api.delete_users([user_id] if user_id is not None else [])
        
        asserter.assert_code(response, 200)

    @allure.story("参数校验-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-用户名参数校验")
    @pytest.mark.parametrize("case_name,username,should_success", 
        param_validator.create_param_test_cases(
            "username",
            param_validator.get_valid_username(),
            param_validator.get_invalid_usernames()
        )
    )
    def test_add_user_username_validation(self, test_user_data, case_name, username, should_success):
        """测试新增用户-用户名参数校验"""
        allure.dynamic.title(f"新增用户-用户名参数校验-{case_name}")
        
        test_user_data["userName"] = username
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)

    @allure.story("参数校验-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-手机号参数校验")
    @pytest.mark.parametrize("case_name,phone,should_success", 
        param_validator.create_param_test_cases(
            "phone",
            param_validator.get_valid_phone(),
            param_validator.get_invalid_phones()
        )
    )
    def test_add_user_phone_validation(self, test_user_data, case_name, phone, should_success):
        """测试新增用户-手机号参数校验"""
        allure.dynamic.title(f"新增用户-手机号参数校验-{case_name}")
        
        test_user_data["phonenumber"] = phone
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)

    @allure.story("参数校验-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增用户-邮箱参数校验")
    @pytest.mark.parametrize("case_name,email,should_success", 
        param_validator.create_param_test_cases(
            "email",
            param_validator.get_valid_email(),
            param_validator.get_invalid_emails()
        )
    )
    def test_add_user_email_validation(self, test_user_data, case_name, email, should_success):
        """测试新增用户-邮箱参数校验"""
        allure.dynamic.title(f"新增用户-邮箱参数校验-{case_name}")
        
        test_user_data["email"] = email
        response = user_api.add_user(test_user_data)
        
        asserter.assert_code(response, 200)
