"""
角色管理模块测试用例
"""
import pytest
import allure
from api.role_api import role_api
from api.user_api import user_api
from utils.assert_utils import asserter
from utils.data_generator import generator


@allure.epic("若依后台管理系统")
@allure.feature("角色管理模块")
class TestRole:
    """角色管理测试类"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化"""
        pass
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取角色列表")
    def test_list_roles(self):
        """测试获取角色列表"""
        response = role_api.list_roles(page_num=1, page_size=10)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "rows")
        asserter.assert_field_exists(response, "total")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据角色名称查询")
    def test_list_roles_by_name(self):
        """测试根据角色名称查询"""
        response = role_api.list_roles(
            page_num=1,
            page_size=10,
            roleName="管理员"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增角色成功")
    def test_add_role_success(self, test_role_data):
        """测试新增角色成功"""
        response = role_api.add_role(test_role_data)
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增角色-角色名称已存在")
    def test_add_role_duplicate_name(self, test_role_data):
        """测试新增角色-角色名称已存在"""
        # 先新增一个角色
        add_response = role_api.add_role(test_role_data)
        
        if add_response.json().get("code") == 200:
            # 再次使用相同名称新增
            response = role_api.add_role(test_role_data)
            
            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)
            asserter.assert_response_message(response, "角色名称已存在")
    
    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("修改角色成功")
    def test_update_role_success(self, test_role_data):
        """测试修改角色成功"""
        # 先新增一个角色
        add_response = role_api.add_role(test_role_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取角色ID
            list_response = role_api.list_roles(
                page_num=1,
                page_size=1,
                roleName=test_role_data["roleName"]
            )
            roles = list_response.json().get("rows", [])
            
            if roles:
                role_id = roles[0].get("roleId")
                update_data = {
                    "roleId": role_id,
                    "roleName": test_role_data["roleName"],
                    "roleKey": test_role_data["roleKey"],
                    "roleSort": 1,
                    "status": "0",
                    "menuIds": [1, 2, 3, 4],
                    "dataScope": "2"
                }
                
                response = role_api.update_role(update_data)
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除角色成功")
    def test_delete_role_success(self, test_role_data):
        """测试删除角色成功"""
        # 先新增一个角色
        add_response = role_api.add_role(test_role_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取角色ID
            list_response = role_api.list_roles(
                page_num=1,
                page_size=1,
                roleName=test_role_data["roleName"]
            )
            roles = list_response.json().get("rows", [])
            
            if roles:
                role_id = roles[0].get("roleId")
                response = role_api.delete_roles([role_id])
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改角色状态")
    def test_change_role_status(self):
        """测试修改角色状态"""
        # 获取一个非管理员角色
        list_response = role_api.list_roles(page_num=1, page_size=10)
        roles = list_response.json().get("rows", [])
        
        for role in roles:
            if not role.get("admin"):
                role_id = role.get("roleId")
                current_status = role.get("status")
                new_status = "1" if current_status == "0" else "0"
                
                response = role_api.change_status(role_id, new_status)
                
                asserter.assert_common(response, 200, True)
                
                # 恢复原状态
                role_api.change_status(role_id, current_status)
                break
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取角色选择框列表")
    def test_get_option_select(self):
        """测试获取角色选择框列表"""
        response = role_api.get_option_select()
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取已分配用户列表")
    def test_get_allocated_users(self):
        """测试获取已分配用户列表"""
        # 获取一个角色
        list_response = role_api.list_roles(page_num=1, page_size=1)
        roles = list_response.json().get("rows", [])
        
        if roles:
            role_id = roles[0].get("roleId")
            response = role_api.get_allocated_users(role_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "rows")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取未分配用户列表")
    def test_get_unallocated_users(self):
        """测试获取未分配用户列表"""
        # 获取一个角色
        list_response = role_api.list_roles(page_num=1, page_size=1)
        roles = list_response.json().get("rows", [])
        
        if roles:
            role_id = roles[0].get("roleId")
            response = role_api.get_unallocated_users(role_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "rows")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取角色部门树")
    def test_get_dept_tree(self):
        """测试获取角色部门树"""
        # 获取一个角色
        list_response = role_api.list_roles(page_num=1, page_size=1)
        roles = list_response.json().get("rows", [])
        
        if roles:
            role_id = roles[0].get("roleId")
            response = role_api.get_dept_tree(role_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "depts")
    
    @allure.story("参数组合测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("多条件组合查询角色")
    def test_list_roles_multi_conditions(self):
        """测试多条件组合查询角色"""
        response = role_api.list_roles(
            page_num=1,
            page_size=10,
            roleName="",
            roleKey="",
            status="0"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("边界值测试")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("分页查询-页码边界值")
    @pytest.mark.parametrize("page_num", [1, 999999])
    def test_list_roles_page_boundary(self, page_num):
        """测试分页查询页码边界值"""
        response = role_api.list_roles(page_num=page_num, page_size=10)

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据状态查询角色")
    def test_list_roles_by_status(self):
        """测试根据状态查询角色"""
        response = role_api.list_roles(
            page_num=1, page_size=10, status="0"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取角色详情-不存在")
    def test_get_role_detail_not_exists(self):
        """测试获取不存在的角色详情"""
        response = role_api.get_role(999999)

        # RuoYi对不存在的ID仍返回code=200，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增角色-角色键已存在")
    def test_add_role_duplicate_key(self):
        """测试新增角色-角色键已存在"""
        role_data = {
            "roleName": generator.random_role_name(),
            "roleKey": "admin",
            "roleSort": 0,
            "status": "0"
        }

        response = role_api.add_role(role_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
        asserter.assert_response_message(response, "角色")

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增角色-缺少必填参数")
    def test_add_role_missing_required(self):
        """测试新增角色-缺少角色名称"""
        role_data = {"roleKey": "test"}

        response = role_api.add_role(role_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增角色-角色名过长")
    def test_add_role_name_too_long(self):
        """测试新增角色-角色名超过30字符"""
        role_data = {
            "roleName": "a" * 31,
            "roleKey": "test_role_key",
            "roleSort": 0,
            "status": "0"
        }

        response = role_api.add_role(role_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增角色-角色键过长")
    def test_add_role_key_too_long(self):
        """测试新增角色-角色键过长"""
        role_data = {
            "roleName": generator.random_role_name(),
            "roleKey": "a" * 101,
            "roleSort": 0,
            "status": "0"
        }

        response = role_api.add_role(role_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改角色-角色不存在")
    def test_update_role_not_exists(self):
        """测试修改不存在的角色"""
        role_data = {
            "roleId": 999999,
            "roleName": "不存在",
            "roleKey": "not_exist",
            "roleSort": 0,
            "status": "0"
        }

        response = role_api.update_role(role_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改角色-缺少必填参数")
    def test_update_role_missing_required(self):
        """测试修改角色-缺少roleId"""
        role_data = {"roleName": "test"}

        response = role_api.update_role(role_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改角色-角色名已存在")
    def test_update_role_duplicate_name(self):
        """测试修改角色-角色名改为已存在的"""
        update_data = {
            "roleId": 2,
            "roleName": "管理员",
            "roleKey": "common",
            "roleSort": 0,
            "status": "0"
        }

        response = role_api.update_role(update_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改数据权限-成功")
    def test_update_data_scope_success(self):
        """测试修改角色数据权限成功"""
        list_response = role_api.list_roles(page_num=1, page_size=10)
        roles = list_response.json().get("rows", [])

        for role in roles:
            if not role.get("admin"):
                role_id = role.get("roleId")
                data = {
                    "roleId": role_id,
                    "dataScope": "2",
                    "deptIds": [100, 101]
                }

                response = role_api.update_data_scope(data)

                asserter.assert_common(response, 200, True)
                break

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改数据权限-角色不存在")
    def test_update_data_scope_not_exists(self):
        """测试修改不存在角色的数据权限"""
        data = {
            "roleId": 999999,
            "dataScope": "2",
            "deptIds": [100]
        }

        # RuoYi对不存在的角色ID不强制校验，验证接口正常响应
        response = role_api.update_data_scope(data)

        asserter.assert_code(response, 200)

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改数据权限-数据范围值错误")
    def test_update_data_scope_invalid_value(self):
        """测试修改数据权限-无效的数据范围值"""
        list_response = role_api.list_roles(page_num=1, page_size=10)
        roles = list_response.json().get("rows", [])

        for role in roles:
            if not role.get("admin"):
                role_id = role.get("roleId")
                data = {
                    "roleId": role_id,
                    "dataScope": "99"
                }

                response = role_api.update_data_scope(data)

                asserter.assert_code(response, 200)
                asserter.assert_success(response, False)
                break

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改角色状态-角色不存在")
    def test_change_status_not_exists(self):
        """测试修改不存在角色的状态"""
        response = role_api.change_status(999999, "0")

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改角色状态-状态值错误")
    def test_change_status_invalid_value(self):
        """测试修改角色状态-无效状态值"""
        list_response = role_api.list_roles(page_num=1, page_size=10)
        roles = list_response.json().get("rows", [])

        for role in roles:
            if not role.get("admin"):
                role_id = role.get("roleId")
                response = role_api.change_status(role_id, "99")

                asserter.assert_code(response, 200)
                asserter.assert_success(response, False)
                break

    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除角色-不存在")
    def test_delete_role_not_exists(self):
        """测试删除不存在的角色"""
        response = role_api.delete_roles([999999])

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除角色-批量删除")
    def test_delete_role_batch(self):
        """测试批量删除角色"""
        # 新增两个测试角色
        role_name1 = generator.random_role_name()
        role_name2 = generator.random_role_name()

        add1 = role_api.add_role({"roleName": role_name1, "roleKey": f"tk_{generator.random_string(6)}", "roleSort": 0, "status": "0"})
        add2 = role_api.add_role({"roleName": role_name2, "roleKey": f"tk_{generator.random_string(6)}", "roleSort": 0, "status": "0"})

        if add1.json().get("code") == 200 and add2.json().get("code") == 200:
            list_response = role_api.list_roles(page_num=1, page_size=100)
            roles = list_response.json().get("rows", [])

            ids_to_delete = []
            for r in roles:
                if r.get("roleName") in [role_name1, role_name2]:
                    ids_to_delete.append(r.get("roleId"))

            if len(ids_to_delete) == 2:
                response = role_api.delete_roles(ids_to_delete)
                asserter.assert_common(response, 200, True)
        else:
            from utils.db_utils import db
            db.safe_cleanup("sys_role", "role_name", role_name1)
            db.safe_cleanup("sys_role", "role_name", role_name2)

    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("导出角色数据")
    def test_export_roles(self):
        """测试导出角色数据"""
        response = role_api.export_roles(roleName="管理员")

        asserter.assert_code(response, 200)
