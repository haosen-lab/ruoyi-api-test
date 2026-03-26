"""
配置管理模块测试用例
"""
import pytest
import allure
from api.config_api import config_api
from utils.assert_utils import asserter
from utils.data_generator import generator
from utils.db_utils import db


@allure.epic("若依后台管理系统")
@allure.feature("配置管理模块")
class TestConfig:
    """配置管理测试类"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化 - 确保已登录"""
        pass
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取配置列表")
    def test_list_configs(self):
        """测试获取配置列表"""
        response = config_api.list_configs(page_num=1, page_size=10)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "rows")
        asserter.assert_field_exists(response, "total")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据类型查询配置")
    def test_list_configs_by_type(self):
        """测试根据类型查询配置"""
        response = config_api.list_configs(
            page_num=1,
            page_size=10,
            configType="system"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("多条件组合查询配置")
    def test_list_configs_multi_conditions(self):
        """测试多条件组合查询配置"""
        response = config_api.list_configs(
            page_num=1,
            page_size=10,
            configName="系统",
            configKey="sys",
            configType="system"
        )
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取配置详情")
    def test_get_config_detail(self):
        """测试获取配置详情"""
        # 先获取配置列表
        list_response = config_api.list_configs(page_num=1, page_size=1)
        configs = list_response.json().get("rows", [])
        
        if configs:
            config_id = configs[0].get("configId")
            response = config_api.get_config(config_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据配置键名获取配置值")
    def test_get_config_by_key(self):
        """测试根据配置键名获取配置值"""
        response = config_api.get_config_by_key("sys.name")
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据配置键名获取配置值-键名不存在")
    def test_get_config_by_key_not_exists(self):
        """测试根据配置键名获取配置值-键名不存在"""
        response = config_api.get_config_by_key("nonexistent")

        asserter.assert_code(response, 200)
        # RuoYi对不存在的键名也返回code=200，但无data字段
        json_data = response.json()
        assert json_data.get("code") == 200
    
    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增配置成功")
    def test_add_config_success(self, test_config_data):
        """测试新增配置成功"""
        response = config_api.add_config(test_config_data)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_response_message(response, "成功")
        
        # 数据库验证 - 检查配置是否真的存在
        with allure.step("数据库验证: 检查配置是否存在"):
            exists = db.check_config_exists(test_config_data["configKey"])
            assert exists, f"配置 {test_config_data['configKey']} 未在数据库中创建"
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增配置-配置键已存在")
    def test_add_config_duplicate_key(self, test_config_data):
        """测试新增配置-配置键已存在"""
        # 先新增一个配置
        add_response = config_api.add_config(test_config_data)
        
        if add_response.json().get("code") == 200:
            # 再次新增相同的配置键
            response = config_api.add_config(test_config_data)
            
            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)
            asserter.assert_response_message(response, "参数键名已存在")
    
    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("修改配置成功")
    def test_update_config_success(self, test_config_data):
        """测试修改配置成功"""
        # 先新增一个配置
        add_response = config_api.add_config(test_config_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取配置ID
            list_response = config_api.list_configs(
                page_num=1,
                page_size=1,
                configKey=test_config_data["configKey"]
            )
            configs = list_response.json().get("rows", [])
            
            if configs:
                config_id = configs[0].get("configId")
                update_data = {
                    "configId": config_id,
                    "configName": test_config_data["configName"] + "修改",
                    "configKey": test_config_data["configKey"],
                    "configValue": test_config_data["configValue"] + "修改",
                    "configType": test_config_data["configType"],
                    "remark": test_config_data["remark"]
                }
                
                response = config_api.update_config(update_data)
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除配置成功")
    def test_delete_config_success(self, test_config_data):
        """测试删除配置成功"""
        # 先新增一个配置
        add_response = config_api.add_config(test_config_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取配置ID
            list_response = config_api.list_configs(
                page_num=1,
                page_size=1,
                configKey=test_config_data["configKey"]
            )
            configs = list_response.json().get("rows", [])
            
            if configs:
                config_id = configs[0].get("configId")
                response = config_api.delete_configs([config_id])
                
                asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("刷新配置缓存")
    def test_refresh_config_cache(self):
        """测试刷新配置缓存"""
        response = config_api.refresh_cache()
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("导出配置数据")
    def test_export_configs(self):
        """测试导出配置数据"""
        response = config_api.export_configs()

        asserter.assert_code(response, 200)

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取配置详情-不存在")
    def test_get_config_detail_not_exists(self):
        """测试获取不存在的配置详情"""
        response = config_api.get_config(999999)

        # RuoYi对不存在的ID仍返回code=200，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增配置-缺少必填参数")
    def test_add_config_missing_required(self):
        """测试新增配置-缺少配置键名"""
        config_data = {"configName": "测试"}

        response = config_api.add_config(config_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增配置-配置名过长")
    def test_add_config_name_too_long(self):
        """测试新增配置-配置名超过100字符"""
        config_data = {
            "configName": "a" * 101,
            "configKey": "test_long_name",
            "configValue": "test",
            "configType": "N"
        }

        response = config_api.add_config(config_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增配置-配置键过长")
    def test_add_config_key_too_long(self):
        """测试新增配置-配置键过长"""
        config_data = {
            "configName": "测试",
            "configKey": "a" * 101,
            "configValue": "test",
            "configType": "N"
        }

        response = config_api.add_config(config_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增配置-完整参数组合")
    def test_add_config_full_params(self, test_config_data):
        """测试新增配置-完整参数组合"""
        full_data = {
            **test_config_data,
            "remark": "完整参数测试配置"
        }

        response = config_api.add_config(full_data)

        asserter.assert_common(response, 200, True)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改配置-配置不存在")
    def test_update_config_not_exists(self):
        """测试修改不存在的配置"""
        config_data = {
            "configId": 999999,
            "configName": "不存在",
            "configKey": "not_exist",
            "configValue": "test",
            "configType": "N"
        }

        response = config_api.update_config(config_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除配置-不存在")
    def test_delete_config_not_exists(self):
        """测试删除不存在的配置"""
        response = config_api.delete_configs([999999])

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
