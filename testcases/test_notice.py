"""
通知管理模块测试用例
"""
import pytest
import allure
from api.notice_api import notice_api
from utils.assert_utils import asserter
from utils.data_generator import generator
from utils.db_utils import db


@allure.epic("若依后台管理系统")
@allure.feature("通知管理模块")
class TestNotice:
    """通知管理测试类"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化 - 确保已登录"""
        pass
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取通知列表")
    def test_list_notices(self):
        """测试获取通知列表"""
        response = notice_api.list_notices(page_num=1, page_size=10)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "rows")
        asserter.assert_field_exists(response, "total")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据状态查询通知")
    def test_list_notices_by_status(self):
        """测试根据状态查询通知"""
        response = notice_api.list_notices(
            page_num=1,
            page_size=10,
            status="0"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("多条件组合查询通知")
    def test_list_notices_multi_conditions(self):
        """测试多条件组合查询通知"""
        response = notice_api.list_notices(
            page_num=1,
            page_size=10,
            noticeTitle="系统",
            status="1"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取通知详情")
    def test_get_notice_detail(self):
        """测试获取通知详情"""
        # 先获取通知列表
        list_response = notice_api.list_notices(page_num=1, page_size=1)
        notices = list_response.json().get("rows", [])
        
        if notices:
            notice_id = notices[0].get("noticeId")
            response = notice_api.get_notice(notice_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增通知成功")
    def test_add_notice_success(self, test_notice_data):
        """测试新增通知成功"""
        response = notice_api.add_notice(test_notice_data)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_response_message(response, "成功")
        
        # 数据库验证 - 检查通知是否真的存在
        with allure.step("数据库验证: 检查通知是否存在"):
            exists = db.check_notice_exists(test_notice_data["noticeTitle"])
            assert exists, f"通知 {test_notice_data['noticeTitle']} 未在数据库中创建"
    
    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("修改通知成功")
    def test_update_notice_success(self, test_notice_data):
        """测试修改通知成功"""
        # 先新增一个通知
        add_response = notice_api.add_notice(test_notice_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取通知ID
            list_response = notice_api.list_notices(
                page_num=1,
                page_size=1,
                noticeTitle=test_notice_data["noticeTitle"]
            )
            notices = list_response.json().get("rows", [])
            
            if notices:
                notice_id = notices[0].get("noticeId")
                update_data = {
                    "noticeId": notice_id,
                    "noticeTitle": test_notice_data["noticeTitle"] + "修改",
                    "noticeType": test_notice_data["noticeType"],
                    "noticeContent": test_notice_data["noticeContent"] + "修改",
                    "status": test_notice_data["status"]
                }
                
                response = notice_api.update_notice(update_data)
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除通知成功")
    def test_delete_notice_success(self, test_notice_data):
        """测试删除通知成功"""
        # 先新增一个通知
        add_response = notice_api.add_notice(test_notice_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取通知ID
            list_response = notice_api.list_notices(
                page_num=1,
                page_size=1,
                noticeTitle=test_notice_data["noticeTitle"]
            )
            notices = list_response.json().get("rows", [])
            
            if notices:
                notice_id = notices[0].get("noticeId")
                response = notice_api.delete_notices([notice_id])
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取顶部公告列表")
    def test_list_top(self):
        """测试获取顶部公告列表"""
        response = notice_api.list_top()

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据类型查询通知")
    def test_list_notices_by_type(self):
        """测试根据类型查询通知"""
        response = notice_api.list_notices(
            page_num=1, page_size=10, noticeType="1"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增通知-标题为空")
    def test_add_notice_empty_title(self):
        """测试新增通知-标题为空字符串"""
        notice_data = {
            "noticeTitle": "",
            "noticeType": "1",
            "noticeContent": "测试内容"
        }

        response = notice_api.add_notice(notice_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增通知-缺少标题字段")
    def test_add_notice_missing_title(self):
        """测试新增通知-缺少noticeTitle字段"""
        notice_data = {
            "noticeType": "1",
            "noticeContent": "测试内容"
        }

        response = notice_api.add_notice(notice_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增通知-标题超过50字符")
    def test_add_notice_title_too_long(self):
        """测试新增通知-标题超过50字符"""
        notice_data = {
            "noticeTitle": "a" * 51,
            "noticeType": "1",
            "noticeContent": "测试内容"
        }

        response = notice_api.add_notice(notice_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增通知-标题包含脚本字符")
    def test_add_notice_script_title(self):
        """测试新增通知-标题包含XSS脚本字符"""
        notice_data = {
            "noticeTitle": "<script>alert(1)</script>",
            "noticeType": "1",
            "noticeContent": "测试内容"
        }

        response = notice_api.add_notice(notice_data)

        # 不应成功或不应执行脚本
        asserter.assert_code(response, 200)

    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增通知-完整参数组合")
    def test_add_notice_full_params(self):
        """测试新增通知-完整参数组合"""
        notice_data = {
            "noticeTitle": generator.random_notice_title(),
            "noticeType": "2",
            "noticeContent": "这是一条完整的测试通知内容，包含多种信息",
            "status": "0",
            "remark": generator.random_remark()
        }

        response = notice_api.add_notice(notice_data)

        asserter.assert_common(response, 200, True)
        db.safe_cleanup("sys_notice", "notice_title", notice_data["noticeTitle"])

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改通知-标题为空")
    def test_update_notice_empty_title(self, test_notice_data):
        """测试修改通知-标题为空字符串"""
        # 先新增一个通知
        add_response = notice_api.add_notice(test_notice_data)

        if add_response.json().get("code") == 200:
            list_response = notice_api.list_notices(
                page_num=1, page_size=1,
                noticeTitle=test_notice_data["noticeTitle"]
            )
            notices = list_response.json().get("rows", [])

            if notices:
                notice_id = notices[0].get("noticeId")
                update_data = {
                    "noticeId": notice_id,
                    "noticeTitle": "",
                    "noticeType": "1",
                    "noticeContent": "测试"
                }

                response = notice_api.update_notice(update_data)

                asserter.assert_code(response, 200)
                asserter.assert_success(response, False)

    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除通知-批量删除")
    def test_delete_notice_batch(self):
        """测试批量删除通知"""
        title1 = generator.random_notice_title()
        title2 = generator.random_notice_title()

        add1 = notice_api.add_notice({"noticeTitle": title1, "noticeType": "1", "noticeContent": "batch1"})
        add2 = notice_api.add_notice({"noticeTitle": title2, "noticeType": "1", "noticeContent": "batch2"})

        if add1.json().get("code") == 200 and add2.json().get("code") == 200:
            list_response = notice_api.list_notices(page_num=1, page_size=100)
            notices = list_response.json().get("rows", [])

            ids_to_delete = []
            for n in notices:
                if n.get("noticeTitle") in [title1, title2]:
                    ids_to_delete.append(n.get("noticeId"))

            if len(ids_to_delete) == 2:
                response = notice_api.delete_notices(ids_to_delete)
                asserter.assert_common(response, 200, True)
        else:
            db.safe_cleanup("sys_notice", "notice_title", title1)
            db.safe_cleanup("sys_notice", "notice_title", title2)

    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除通知-不存在")
    def test_delete_notice_not_exists(self):
        """测试删除不存在的通知"""
        response = notice_api.delete_notices([999999])

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取顶部通知列表-未登录")
    def test_list_top_without_login(self):
        """测试未登录获取顶部通知列表"""
        from utils.request_utils import RequestUtils
        import api.notice_api as notice_module

        new_request = RequestUtils()
        original_request = notice_module.request
        notice_module.request = new_request

        try:
            response = notice_api.list_top()
            # 顶部通知可能不需要登录也可能需要
            assert response.status_code in [200, 401, 403]
        finally:
            notice_module.request = original_request
            new_request.close()

    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("标记通知已读")
    def test_mark_read_success(self):
        """测试标记通知已读"""
        list_response = notice_api.list_notices(page_num=1, page_size=1)
        notices = list_response.json().get("rows", [])

        if notices:
            notice_id = notices[0].get("noticeId")
            response = notice_api.mark_read(notice_id)

            asserter.assert_common(response, 200, True)

    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("批量标记通知已读")
    def test_mark_read_all_success(self):
        """测试批量标记通知已读"""
        list_response = notice_api.list_notices(page_num=1, page_size=10)
        notices = list_response.json().get("rows", [])

        if notices:
            ids = [n.get("noticeId") for n in notices[:2] if n.get("noticeId")]
            if ids:
                response = notice_api.mark_read_all(ids)

                asserter.assert_common(response, 200, True)
