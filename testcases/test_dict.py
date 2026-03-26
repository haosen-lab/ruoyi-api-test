"""
字典管理模块测试用例
"""
import pytest
import allure
from api.dict_api import dict_type_api, dict_data_api
from utils.assert_utils import asserter
from utils.data_generator import generator
from utils.db_utils import db


@allure.epic("若依后台管理系统")
@allure.feature("字典管理模块")
class TestDict:
    """字典管理测试类"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化 - 确保已登录"""
        pass
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取字典类型列表")
    def test_list_dict_types(self):
        """测试获取字典类型列表"""
        response = dict_type_api.list_types(page_num=1, page_size=10)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "rows")
        asserter.assert_field_exists(response, "total")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据状态查询字典类型")
    def test_list_dict_types_by_status(self):
        """测试根据状态查询字典类型"""
        response = dict_type_api.list_types(
            page_num=1,
            page_size=10,
            status="0"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("多条件组合查询字典类型")
    def test_list_dict_types_multi_conditions(self):
        """测试多条件组合查询字典类型"""
        response = dict_type_api.list_types(
            page_num=1,
            page_size=10,
            dictName="性别",
            dictType="sys_user_sex",
            status="1"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取字典类型详情")
    def test_get_dict_type_detail(self):
        """测试获取字典类型详情"""
        # 先获取字典类型列表
        list_response = dict_type_api.list_types(page_num=1, page_size=1)
        types = list_response.json().get("rows", [])
        
        if types:
            dict_id = types[0].get("dictId")
            response = dict_type_api.get_type(dict_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增字典类型成功")
    def test_add_dict_type_success(self, test_dict_type_data):
        """测试新增字典类型成功"""
        response = dict_type_api.add_type(test_dict_type_data)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_response_message(response, "成功")
        
        # 数据库验证 - 检查字典类型是否真的存在
        with allure.step("数据库验证: 检查字典类型是否存在"):
            exists = db.check_dict_type_exists(test_dict_type_data["dictType"])
            assert exists, f"字典类型 {test_dict_type_data['dictType']} 未在数据库中创建"
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增字典类型-字典类型已存在")
    def test_add_dict_type_duplicate(self, test_dict_type_data):
        """测试新增字典类型-字典类型已存在"""
        # 先新增一个字典类型
        add_response = dict_type_api.add_type(test_dict_type_data)
        
        if add_response.json().get("code") == 200:
            # 再次新增相同的字典类型
            response = dict_type_api.add_type(test_dict_type_data)
            
            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)
            asserter.assert_response_message(response, "字典类型已存在")
    
    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("修改字典类型成功")
    def test_update_dict_type_success(self, test_dict_type_data):
        """测试修改字典类型成功"""
        # 先新增一个字典类型
        add_response = dict_type_api.add_type(test_dict_type_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取字典类型ID
            list_response = dict_type_api.list_types(
                page_num=1,
                page_size=1,
                dictType=test_dict_type_data["dictType"]
            )
            types = list_response.json().get("rows", [])
            
            if types:
                dict_id = types[0].get("dictId")
                update_data = {
                    "dictId": dict_id,
                    "dictName": test_dict_type_data["dictName"] + "修改",
                    "dictType": test_dict_type_data["dictType"],
                    "status": test_dict_type_data["status"],
                    "remark": test_dict_type_data["remark"]
                }
                
                response = dict_type_api.update_type(update_data)
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除字典类型成功")
    def test_delete_dict_type_success(self, test_dict_type_data):
        """测试删除字典类型成功"""
        # 先新增一个字典类型
        add_response = dict_type_api.add_type(test_dict_type_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取字典类型ID
            list_response = dict_type_api.list_types(
                page_num=1,
                page_size=1,
                dictType=test_dict_type_data["dictType"]
            )
            types = list_response.json().get("rows", [])
            
            if types:
                dict_id = types[0].get("dictId")
                response = dict_type_api.delete_types([dict_id])
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("刷新字典缓存")
    def test_refresh_dict_cache(self):
        """测试刷新字典缓存"""
        response = dict_type_api.refresh_cache()
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取字典选择框列表")
    def test_get_dict_option_select(self):
        """测试获取字典选择框列表"""
        response = dict_type_api.get_option_select()
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取字典数据列表")
    def test_list_dict_data(self):
        """测试获取字典数据列表"""
        response = dict_data_api.list_data(page_num=1, page_size=10)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "rows")
        asserter.assert_field_exists(response, "total")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据字典类型获取字典数据")
    def test_get_dict_data_by_type(self):
        """测试根据字典类型获取字典数据"""
        response = dict_data_api.get_data_by_type("sys_user_sex")
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增字典数据成功")
    def test_add_dict_data_success(self, test_dict_type_data, test_dict_data_data):
        """测试新增字典数据成功"""
        # 先新增一个字典类型
        add_type_response = dict_type_api.add_type(test_dict_type_data)
        
        if add_type_response.json().get("code") == 200:
            # 使用新创建的字典类型
            test_dict_data_data["dictType"] = test_dict_type_data["dictType"]
            
            response = dict_data_api.add_data(test_dict_data_data)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_response_message(response, "成功")
    
    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("修改字典数据成功")
    def test_update_dict_data_success(self, test_dict_type_data, test_dict_data_data):
        """测试修改字典数据成功"""
        # 先新增一个字典类型
        add_type_response = dict_type_api.add_type(test_dict_type_data)
        
        if add_type_response.json().get("code") == 200:
            # 使用新创建的字典类型
            test_dict_data_data["dictType"] = test_dict_type_data["dictType"]
            
            # 新增字典数据
            add_data_response = dict_data_api.add_data(test_dict_data_data)
            
            if add_data_response.json().get("code") == 200:
                # 查询获取字典数据ID
                list_response = dict_data_api.list_data(
                    page_num=1,
                    page_size=1,
                    dictType=test_dict_type_data["dictType"]
                )
                data_list = list_response.json().get("rows", [])
                
                if data_list:
                    dict_code = data_list[0].get("dictCode")
                    update_data = {
                        "dictCode": dict_code,
                        "dictType": test_dict_type_data["dictType"],
                        "dictLabel": test_dict_data_data["dictLabel"] + "修改",
                        "dictValue": test_dict_data_data["dictValue"],
                        "status": test_dict_data_data["status"]
                    }
                    
                    response = dict_data_api.update_data(update_data)
                    
                    asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除字典数据成功")
    def test_delete_dict_data_success(self, test_dict_type_data, test_dict_data_data):
        """测试删除字典数据成功"""
        # 先新增一个字典类型
        add_type_response = dict_type_api.add_type(test_dict_type_data)
        
        if add_type_response.json().get("code") == 200:
            # 使用新创建的字典类型
            test_dict_data_data["dictType"] = test_dict_type_data["dictType"]
            
            # 新增字典数据
            add_data_response = dict_data_api.add_data(test_dict_data_data)
            
            if add_data_response.json().get("code") == 200:
                # 查询获取字典数据ID
                list_response = dict_data_api.list_data(
                    page_num=1,
                    page_size=1,
                    dictType=test_dict_type_data["dictType"]
                )
                data_list = list_response.json().get("rows", [])
                
                if data_list:
                    dict_code = data_list[0].get("dictCode")
                    response = dict_data_api.delete_data([dict_code])
                    
                    asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("导出字典类型")
    def test_export_dict_types(self):
        """测试导出字典类型"""
        response = dict_type_api.export_types()
        
        asserter.assert_code(response, 200)
    
    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("导出字典数据")
    def test_export_dict_data(self):
        """测试导出字典数据"""
        response = dict_data_api.export_data()

        asserter.assert_code(response, 200)

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取字典类型详情-不存在")
    def test_get_dict_type_detail_not_exists(self):
        """测试获取不存在的字典类型详情"""
        response = dict_type_api.get_type(999999)

        # RuoYi对不存在的ID仍返回code=200，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增字典类型-缺少必填参数")
    def test_add_dict_type_missing_required(self):
        """测试新增字典类型-缺少字典类型键"""
        type_data = {"dictName": "测试"}

        response = dict_type_api.add_type(type_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增字典类型-字典名过长")
    def test_add_dict_type_name_too_long(self):
        """测试新增字典类型-字典名超过100字符"""
        type_data = {
            "dictName": "a" * 101,
            "dictType": "test_long_name",
            "status": "0"
        }

        response = dict_type_api.add_type(type_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增字典类型-字典类型键过长")
    def test_add_dict_type_key_too_long(self):
        """测试新增字典类型-字典类型键过长"""
        type_data = {
            "dictName": "测试",
            "dictType": "a" * 101,
            "status": "0"
        }

        response = dict_type_api.add_type(type_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增字典类型-完整参数组合")
    def test_add_dict_type_full_params(self, test_dict_type_data):
        """测试新增字典类型-完整参数组合"""
        full_data = {
            **test_dict_type_data,
            "remark": "完整参数测试字典类型"
        }

        response = dict_type_api.add_type(full_data)

        asserter.assert_common(response, 200, True)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改字典类型-字典类型不存在")
    def test_update_dict_type_not_exists(self):
        """测试修改不存在的字典类型"""
        update_data = {
            "dictId": 999999,
            "dictName": "不存在",
            "dictType": "not_exist",
            "status": "0"
        }

        response = dict_type_api.update_type(update_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除字典类型-不存在")
    def test_delete_dict_type_not_exists(self):
        """测试删除不存在的字典类型"""
        response = dict_type_api.delete_types([999999])

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据状态查询字典数据")
    def test_list_dict_data_by_status(self):
        """测试根据状态查询字典数据"""
        response = dict_data_api.list_data(
            page_num=1, page_size=10, status="0"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("多条件组合查询字典数据")
    def test_list_dict_data_multi_conditions(self):
        """测试多条件组合查询字典数据"""
        response = dict_data_api.list_data(
            page_num=1, page_size=10,
            dictType="sys_user_sex",
            dictLabel="男",
            status="0"
        )

        asserter.assert_common(response, 200, True)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取字典数据详情")
    def test_get_dict_data_detail_success(self):
        """测试获取字典数据详情成功"""
        list_response = dict_data_api.list_data(page_num=1, page_size=1)
        data_list = list_response.json().get("rows", [])

        if data_list:
            dict_code = data_list[0].get("dictCode")
            response = dict_data_api.get_data(dict_code)

            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "data")

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取字典数据详情-不存在")
    def test_get_dict_data_detail_not_exists(self):
        """测试获取不存在的字典数据详情"""
        response = dict_data_api.get_data(999999)

        # RuoYi对不存在的ID仍返回code=200，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据字典类型获取数据-类型不存在")
    def test_get_dict_data_by_type_not_exists(self):
        """测试根据不存在的字典类型获取数据"""
        response = dict_data_api.get_data_by_type("nonexistent_type")

        asserter.assert_common(response, 200, True)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增字典数据-缺少必填参数")
    def test_add_dict_data_missing_required(self):
        """测试新增字典数据-缺少字典标签"""
        data = {"dictType": "sys_user_sex"}

        response = dict_data_api.add_data(data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增字典数据-字典标签过长")
    def test_add_dict_data_label_too_long(self, test_dict_type_data, test_dict_data_data):
        """测试新增字典数据-字典标签过长"""
        add_type_response = dict_type_api.add_type(test_dict_type_data)

        if add_type_response.json().get("code") == 200:
            test_dict_data_data["dictType"] = test_dict_type_data["dictType"]
            test_dict_data_data["dictLabel"] = "a" * 101

            response = dict_data_api.add_data(test_dict_data_data)

            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增字典数据-字典值过长")
    def test_add_dict_data_value_too_long(self, test_dict_type_data, test_dict_data_data):
        """测试新增字典数据-字典值过长"""
        add_type_response = dict_type_api.add_type(test_dict_type_data)

        if add_type_response.json().get("code") == 200:
            test_dict_data_data["dictType"] = test_dict_type_data["dictType"]
            test_dict_data_data["dictValue"] = "a" * 101

            response = dict_data_api.add_data(test_dict_data_data)

            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)

    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增字典数据-完整参数组合")
    def test_add_dict_data_full_params(self, test_dict_type_data, test_dict_data_data):
        """测试新增字典数据-完整参数组合"""
        add_type_response = dict_type_api.add_type(test_dict_type_data)

        if add_type_response.json().get("code") == 200:
            test_dict_data_data["dictType"] = test_dict_type_data["dictType"]
            full_data = {
                **test_dict_data_data,
                "cssClass": "el-icon-check",
                "remark": "完整参数测试字典数据"
            }

            response = dict_data_api.add_data(full_data)

            asserter.assert_common(response, 200, True)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改字典数据-字典数据不存在")
    def test_update_dict_data_not_exists(self):
        """测试修改不存在的字典数据"""
        update_data = {
            "dictCode": 999999,
            "dictType": "sys_user_sex",
            "dictLabel": "不存在",
            "dictValue": "0",
            "status": "0"
        }

        response = dict_data_api.update_data(update_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除字典数据-不存在")
    def test_delete_dict_data_not_exists(self):
        """测试删除不存在的字典数据"""
        response = dict_data_api.delete_data([999999])

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
