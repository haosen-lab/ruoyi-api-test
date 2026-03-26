"""
岗位管理模块测试用例
"""
import pytest
import allure
from api.post_api import post_api
from api.user_api import user_api
from utils.assert_utils import asserter
from utils.data_generator import generator
from utils.db_utils import db


@allure.epic("若依后台管理系统")
@allure.feature("岗位管理模块")
class TestPost:
    """岗位管理测试类"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化 - 确保已登录"""
        pass
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取岗位列表")
    def test_list_posts(self):
        """测试获取岗位列表"""
        response = post_api.list_posts(page_num=1, page_size=10)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "rows")
        asserter.assert_field_exists(response, "total")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据状态查询岗位")
    def test_list_posts_by_status(self):
        """测试根据状态查询岗位"""
        response = post_api.list_posts(
            page_num=1,
            page_size=10,
            status="0"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("多条件组合查询岗位")
    def test_list_posts_multi_conditions(self):
        """测试多条件组合查询岗位"""
        response = post_api.list_posts(
            page_num=1,
            page_size=10,
            postName="管理员",
            postCode="admin",
            status="1"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取岗位详情")
    def test_get_post_detail(self):
        """测试获取岗位详情"""
        # 先获取岗位列表
        list_response = post_api.list_posts(page_num=1, page_size=1)
        posts = list_response.json().get("rows", [])
        
        if posts:
            post_id = posts[0].get("postId")
            response = post_api.get_post(post_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增岗位成功")
    def test_add_post_success(self, test_post_data):
        """测试新增岗位成功"""
        response = post_api.add_post(test_post_data)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_response_message(response, "成功")
        
        # 数据库验证 - 检查岗位是否真的存在 (按postName查询)
        with allure.step("数据库验证: 检查岗位是否存在"):
            exists = db.check_post_exists(test_post_data["postName"])
            assert exists, f"岗位 {test_post_data['postName']} 未在数据库中创建"
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增岗位-岗位编码已存在")
    def test_add_post_duplicate_code(self, test_post_data):
        """测试新增岗位-岗位编码已存在"""
        from utils.data_generator import generator
        # 先新增一个岗位
        add_response = post_api.add_post(test_post_data)

        if add_response.json().get("code") == 200:
            # 使用相同编码但不同名称新增，触发编码重复校验
            dup_data = {**test_post_data, "postName": generator.random_post_name()}
            response = post_api.add_post(dup_data)

            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)
            asserter.assert_response_message(response, "岗位编码已存在")
    
    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("修改岗位成功")
    def test_update_post_success(self, test_post_data):
        """测试修改岗位成功"""
        # 先新增一个岗位
        add_response = post_api.add_post(test_post_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取岗位ID
            list_response = post_api.list_posts(
                page_num=1,
                page_size=1,
                postCode=test_post_data["postCode"]
            )
            posts = list_response.json().get("rows", [])
            
            if posts:
                post_id = posts[0].get("postId")
                update_data = {
                    "postId": post_id,
                    "postName": test_post_data["postName"] + "修改",
                    "postCode": test_post_data["postCode"],
                    "postSort": test_post_data["postSort"],
                    "status": test_post_data["status"],
                    "remark": test_post_data["remark"]
                }
                
                response = post_api.update_post(update_data)
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除岗位成功")
    def test_delete_post_success(self, test_post_data):
        """测试删除岗位成功"""
        # 先新增一个岗位
        add_response = post_api.add_post(test_post_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取岗位ID
            list_response = post_api.list_posts(
                page_num=1,
                page_size=1,
                postCode=test_post_data["postCode"]
            )
            posts = list_response.json().get("rows", [])
            
            if posts:
                post_id = posts[0].get("postId")
                response = post_api.delete_posts([post_id])
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("导出岗位数据")
    def test_export_posts(self):
        """测试导出岗位数据"""
        response = post_api.export_posts()

        asserter.assert_code(response, 200)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据编码查询岗位")
    def test_list_posts_by_code(self):
        """测试根据编码查询岗位"""
        response = post_api.list_posts(
            page_num=1, page_size=10, postCode="ceo"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取岗位详情-不存在")
    def test_get_post_detail_not_exists(self):
        """测试获取不存在的岗位详情"""
        response = post_api.get_post(999999)

        # RuoYi对不存在的ID仍返回code=200，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增岗位-岗位名称为空")
    def test_add_post_empty_name(self, test_post_data):
        """测试新增岗位-岗位名称为空"""
        test_post_data["postName"] = ""

        response = post_api.add_post(test_post_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增岗位-岗位编码为空")
    def test_add_post_empty_code(self, test_post_data):
        """测试新增岗位-岗位编码为空"""
        test_post_data["postCode"] = ""

        response = post_api.add_post(test_post_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增岗位-岗位名称已存在")
    def test_add_post_duplicate_name(self):
        """测试新增岗位-岗位名称已存在"""
        post_data = {
            "postName": "董事长",
            "postCode": generator.random_string(8).upper(),
            "postSort": 0,
            "status": "0"
        }

        response = post_api.add_post(post_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
        asserter.assert_response_message(response, "岗位名称已存在")

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增岗位-岗位名称超过50字符")
    def test_add_post_name_too_long(self, test_post_data):
        """测试新增岗位-岗位名称超过50字符"""
        test_post_data["postName"] = "a" * 51

        response = post_api.add_post(test_post_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增岗位-岗位编码超过64字符")
    def test_add_post_code_too_long(self, test_post_data):
        """测试新增岗位-岗位编码超过64字符"""
        test_post_data["postCode"] = "a" * 65

        response = post_api.add_post(test_post_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增岗位-完整参数组合")
    def test_add_post_full_params(self):
        """测试新增岗位-完整参数组合"""
        post_data = {
            "postCode": generator.random_string(8).upper(),
            "postName": generator.random_post_name(),
            "postSort": 99,
            "status": "0",
            "remark": generator.random_remark()
        }

        response = post_api.add_post(post_data)

        asserter.assert_common(response, 200, True)
        db.safe_cleanup("sys_post", "post_name", post_data["postName"])

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改岗位-岗位名称已存在")
    def test_update_post_duplicate_name(self):
        """测试修改岗位-岗位名称改为已存在的"""
        update_data = {
            "postId": 2,
            "postName": "董事长",
            "postCode": "test_update",
            "postSort": 0,
            "status": "0"
        }

        response = post_api.update_post(update_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除岗位-已分配给用户")
    def test_delete_post_assigned_user(self):
        """测试删除已分配给用户的岗位失败"""
        # 获取一个已分配给用户的岗位
        list_response = user_api.list_users(page_num=1, page_size=10)
        users = list_response.json().get("rows", [])

        for user in users:
            posts = user.get("posts", [])
            if posts:
                post_id = posts[0].get("postId")
                if post_id:
                    response = post_api.delete_posts([post_id])

                    asserter.assert_code(response, 200)
                    asserter.assert_success(response, False)
                    break

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取岗位选择框列表")
    def test_get_post_option_select(self):
        """测试获取岗位选择框列表"""
        response = post_api.get_option_select()

        asserter.assert_common(response, 200, True)
