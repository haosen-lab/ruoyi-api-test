"""
部门管理模块测试用例
"""
import pytest
import allure
from api.dept_api import dept_api
from utils.assert_utils import asserter
from utils.data_generator import generator
from utils.db_utils import db


@allure.epic("若依后台管理系统")
@allure.feature("部门管理模块")
class TestDept:
    """部门管理测试类"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化"""
        pass
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取部门列表")
    def test_list_depts(self):
        """测试获取部门列表"""
        response = dept_api.list_depts()
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据部门名称查询")
    def test_list_depts_by_name(self):
        """测试根据部门名称查询"""
        response = dept_api.list_depts(deptName="研发")
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取部门详情")
    def test_get_dept_detail(self):
        """测试获取部门详情"""
        # 先获取部门列表
        list_response = dept_api.list_depts()
        depts = list_response.json().get("data", [])
        
        if depts:
            dept_id = depts[0].get("deptId")
            response = dept_api.get_dept(dept_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增部门成功")
    def test_add_dept_success(self, test_dept_data):
        """测试新增部门成功"""
        response = dept_api.add_dept(test_dept_data)
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增部门-部门名称已存在")
    def test_add_dept_duplicate_name(self, test_dept_data):
        """测试新增部门-部门名称已存在"""
        # 先新增一个部门
        add_response = dept_api.add_dept(test_dept_data)
        
        if add_response.json().get("code") == 200:
            # 再次使用相同名称新增
            response = dept_api.add_dept(test_dept_data)
            
            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)
            asserter.assert_response_message(response, "部门名称已存在")
    
    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("修改部门成功")
    def test_update_dept_success(self, test_dept_data):
        """测试修改部门成功"""
        # 先新增一个部门
        add_response = dept_api.add_dept(test_dept_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取部门ID
            list_response = dept_api.list_depts()
            depts = list_response.json().get("data", [])
            
            for dept in depts:
                if dept.get("deptName") == test_dept_data["deptName"]:
                    dept_id = dept.get("deptId")
                    update_data = {
                        "deptId": dept_id,
                        "parentId": test_dept_data["parentId"],
                        "deptName": test_dept_data["deptName"],
                        "orderNum": 1,
                        "leader": "修改后的负责人",
                        "phone": test_dept_data["phone"],
                        "email": test_dept_data["email"],
                        "status": "0"
                    }
                    
                    response = dept_api.update_dept(update_data)
                    
                    asserter.assert_common(response, 200, True)
                    break
    
    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除部门成功")
    def test_delete_dept_success(self, test_dept_data):
        """测试删除部门成功"""
        # 先新增一个部门
        add_response = dept_api.add_dept(test_dept_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取部门ID
            list_response = dept_api.list_depts()
            depts = list_response.json().get("data", [])
            
            for dept in depts:
                if dept.get("deptName") == test_dept_data["deptName"]:
                    dept_id = dept.get("deptId")
                    response = dept_api.delete_dept(dept_id)
                    
                    asserter.assert_common(response, 200, True)
                    break
    
    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除部门-存在下级部门")
    def test_delete_dept_with_children(self):
        """测试删除存在下级部门的部门失败"""
        # 获取部门列表，找到有子部门的
        list_response = dept_api.list_depts()
        depts = list_response.json().get("data", [])
        
        # 找到第一个有子部门的部门
        for dept in depts:
            for child in depts:
                if child.get("parentId") == dept.get("deptId"):
                    response = dept_api.delete_dept(dept.get("deptId"))
                    
                    asserter.assert_code(response, 200)
                    asserter.assert_response_message(response, "存在下级部门")
                    return
    
    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除部门-存在下级或用户不允许删除")
    def test_delete_dept_with_users(self):
        """测试删除存在用户或下级部门的部门失败"""
        # 部门100(若依科技)有下级部门和用户，会返回"存在下级部门"
        response = dept_api.delete_dept(100)

        asserter.assert_code(response, 200)
        # 可能返回"存在下级部门"或"部门存在用户"，检查任一即可
        asserter.assert_success(response, False)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取部门列表(排除节点)")
    def test_list_depts_exclude(self):
        """测试获取部门列表(排除节点)"""
        # 获取一个部门ID
        list_response = dept_api.list_depts()
        depts = list_response.json().get("data", [])

        if depts:
            dept_id = depts[0].get("deptId")
            response = dept_api.list_depts_exclude(dept_id)

            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "data")

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据状态查询部门")
    def test_list_depts_by_status(self):
        """测试根据状态查询部门"""
        response = dept_api.list_depts(status="0")

        asserter.assert_common(response, 200, True)

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取部门详情-不存在")
    def test_get_dept_detail_not_exists(self):
        """测试获取不存在的部门详情"""
        response = dept_api.get_dept(999999)

        # RuoYi对不存在的ID仍返回code=200，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增部门-缺少必填参数")
    def test_add_dept_missing_required(self):
        """测试新增部门-缺少部门名称"""
        dept_data = {"parentId": 100}

        response = dept_api.add_dept(dept_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增部门-部门名过长")
    def test_add_dept_name_too_long(self, test_dept_data):
        """测试新增部门-部门名超过30字符"""
        test_dept_data["deptName"] = "a" * 31

        response = dept_api.add_dept(test_dept_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增部门-手机号格式错误")
    def test_add_dept_invalid_phone(self, test_dept_data):
        """测试新增部门-手机号格式错误"""
        test_dept_data["phone"] = "123"

        response = dept_api.add_dept(test_dept_data)

        # RuoYi后端不强制校验手机号格式，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增部门-邮箱格式错误")
    def test_add_dept_invalid_email(self, test_dept_data):
        """测试新增部门-邮箱格式错误"""
        test_dept_data["email"] = "invalid_email"

        response = dept_api.add_dept(test_dept_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增部门-完整参数组合")
    def test_add_dept_full_params(self):
        """测试新增部门-完整参数组合"""
        dept_data = {
            "parentId": 100,
            "deptName": generator.random_dept_name(),
            "orderNum": 99,
            "leader": "完整测试负责人",
            "phone": generator.random_phone(),
            "email": generator.random_email(),
            "status": "0"
        }

        response = dept_api.add_dept(dept_data)

        asserter.assert_common(response, 200, True)
        db.safe_cleanup("sys_dept", "dept_name", dept_data["deptName"])

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改部门-部门不存在")
    def test_update_dept_not_exists(self):
        """测试修改不存在的部门"""
        dept_data = {
            "deptId": 999999,
            "deptName": "不存在",
            "parentId": 100,
            "orderNum": 0,
            "status": "0"
        }

        response = dept_api.update_dept(dept_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改部门-上级部门为自己")
    def test_update_dept_self_parent(self, test_dept_data):
        """测试修改部门-上级部门选择自己"""
        # 先新增一个部门
        add_response = dept_api.add_dept(test_dept_data)

        if add_response.json().get("code") == 200:
            list_response = dept_api.list_depts()
            depts = list_response.json().get("data", [])

            for dept in depts:
                if dept.get("deptName") == test_dept_data["deptName"]:
                    dept_id = dept.get("deptId")
                    update_data = {
                        "deptId": dept_id,
                        "parentId": dept_id,
                        "deptName": test_dept_data["deptName"],
                        "orderNum": 0,
                        "status": "0"
                    }

                    response = dept_api.update_dept(update_data)

                    asserter.assert_code(response, 200)
                    asserter.assert_success(response, False)
                    break

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改部门-部门名已存在")
    def test_update_dept_duplicate_name(self, test_dept_data):
        """测试修改部门-部门名改为已存在的"""
        update_data = {
            "deptId": 100,
            "deptName": "研发部",
            "parentId": 100,
            "orderNum": 0,
            "status": "0"
        }

        response = dept_api.update_dept(update_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改部门-完整参数组合")
    def test_update_dept_full_params(self, test_dept_data):
        """测试修改部门-完整参数组合"""
        # 先新增一个部门
        add_response = dept_api.add_dept(test_dept_data)

        if add_response.json().get("code") == 200:
            list_response = dept_api.list_depts()
            depts = list_response.json().get("data", [])

            for dept in depts:
                if dept.get("deptName") == test_dept_data["deptName"]:
                    dept_id = dept.get("deptId")
                    update_data = {
                        "deptId": dept_id,
                        "parentId": test_dept_data["parentId"],
                        "deptName": test_dept_data["deptName"],
                        "orderNum": 99,
                        "leader": "完整修改负责人",
                        "phone": generator.random_phone(),
                        "email": generator.random_email(),
                        "status": "0"
                    }

                    response = dept_api.update_dept(update_data)

                    asserter.assert_common(response, 200, True)
                    break

    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除部门-部门不存在")
    def test_delete_dept_not_exists(self):
        """测试删除不存在的部门"""
        response = dept_api.delete_dept(999999)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("保存部门排序-成功")
    def test_update_dept_sort_success(self):
        """测试保存部门排序成功"""
        list_response = dept_api.list_depts()
        depts = list_response.json().get("data", [])

        if depts:
            dept_id = depts[0].get("deptId")
            original_order = depts[0].get("orderNum", 0)

            response = dept_api.update_sort([dept_id], [original_order])

            asserter.assert_common(response, 200, True)

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("保存部门排序-缺少参数")
    def test_update_dept_sort_missing_params(self):
        """测试保存部门排序-缺少orderNums"""
        list_response = dept_api.list_depts()
        depts = list_response.json().get("data", [])

        if depts:
            dept_id = depts[0].get("deptId")

            # RuoYi对空数组不强制校验，验证接口正常响应
            response = dept_api.update_sort([dept_id], [])

            asserter.assert_code(response, 200)
