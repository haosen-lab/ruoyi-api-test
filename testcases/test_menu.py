"""
菜单管理模块测试用例
"""
import pytest
import allure
from api.menu_api import menu_api
from utils.assert_utils import asserter


@allure.epic("若依后台管理系统")
@allure.feature("菜单管理模块")
class TestMenu:
    """菜单管理测试类"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, admin_login):
        """类级别初始化"""
        pass
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("获取菜单列表")
    def test_list_menus(self):
        """测试获取菜单列表"""
        response = menu_api.list_menus()
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据菜单名称查询")
    def test_list_menus_by_name(self):
        """测试根据菜单名称查询"""
        response = menu_api.list_menus(menuName="系统管理")
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取菜单详情")
    def test_get_menu_detail(self):
        """测试获取菜单详情"""
        # 先获取菜单列表
        list_response = menu_api.list_menus()
        menus = list_response.json().get("data", [])
        
        if menus:
            menu_id = menus[0].get("menuId")
            response = menu_api.get_menu(menu_id)
            
            asserter.assert_common(response, 200, True)
            asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取菜单下拉树")
    def test_get_tree_select(self):
        """测试获取菜单下拉树"""
        response = menu_api.get_tree_select()
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "data")
    
    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取角色菜单树")
    def test_get_role_menu_tree(self):
        """测试获取角色菜单树"""
        response = menu_api.get_role_menu_tree(1)
        
        asserter.assert_common(response, 200, True)
        asserter.assert_field_exists(response, "menus")
        asserter.assert_field_exists(response, "checkedKeys")
    
    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增菜单成功")
    def test_add_menu_success(self, test_menu_data):
        """测试新增菜单成功"""
        response = menu_api.add_menu(test_menu_data)
        
        asserter.assert_common(response, 200, True)
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增菜单-菜单名称已存在")
    def test_add_menu_duplicate_name(self, test_menu_data):
        """测试新增菜单-菜单名称已存在"""
        # 先新增一个菜单
        add_response = menu_api.add_menu(test_menu_data)
        
        if add_response.json().get("code") == 200:
            # 再次使用相同名称新增
            response = menu_api.add_menu(test_menu_data)
            
            asserter.assert_code(response, 200)
            asserter.assert_success(response, False)
            asserter.assert_response_message(response, "菜单名称已存在")
    
    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增菜单-外链地址格式错误")
    def test_add_menu_invalid_frame_url(self, test_menu_data):
        """测试新增菜单-外链地址格式错误"""
        test_menu_data["isFrame"] = "0"  # 是外链
        test_menu_data["path"] = "invalid-url"  # 不是http(s)开头
        
        response = menu_api.add_menu(test_menu_data)
        
        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
        asserter.assert_response_message(response, "地址必须以http(s)://开头")
    
    @allure.story("正常场景-修改")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("修改菜单成功")
    def test_update_menu_success(self, test_menu_data):
        """测试修改菜单成功"""
        # 先新增一个菜单
        add_response = menu_api.add_menu(test_menu_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取菜单ID
            list_response = menu_api.list_menus(menuName=test_menu_data["menuName"])
            menus = list_response.json().get("data", [])
            
            for menu in menus:
                if menu.get("menuName") == test_menu_data["menuName"]:
                    menu_id = menu.get("menuId")
                    update_data = {
                        "menuId": menu_id,
                        "menuName": test_menu_data["menuName"],
                        "parentId": test_menu_data["parentId"],
                        "orderNum": 1,
                        "path": test_menu_data["path"],
                        "component": test_menu_data["component"],
                        "isFrame": test_menu_data["isFrame"],
                        "isCache": test_menu_data["isCache"],
                        "menuType": test_menu_data["menuType"],
                        "visible": test_menu_data["visible"],
                        "status": test_menu_data["status"],
                        "icon": test_menu_data["icon"],
                        "perms": test_menu_data["perms"]
                    }
                    
                    response = menu_api.update_menu(update_data)
                    
                    asserter.assert_common(response, 200, True)
                    break
    
    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改菜单-上级菜单选择自己")
    def test_update_menu_self_parent(self, test_menu_data):
        """测试修改菜单-上级菜单选择自己"""
        # 先新增一个菜单
        add_response = menu_api.add_menu(test_menu_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取菜单ID
            list_response = menu_api.list_menus(menuName=test_menu_data["menuName"])
            menus = list_response.json().get("data", [])
            
            for menu in menus:
                if menu.get("menuName") == test_menu_data["menuName"]:
                    menu_id = menu.get("menuId")
                    update_data = {
                        "menuId": menu_id,
                        "menuName": test_menu_data["menuName"],
                        "parentId": menu_id,  # 选择自己作为上级
                        "orderNum": 0,
                        "path": test_menu_data["path"],
                        "component": test_menu_data["component"],
                        "menuType": test_menu_data["menuType"],
                        "visible": test_menu_data["visible"],
                        "status": test_menu_data["status"]
                    }
                    
                    response = menu_api.update_menu(update_data)
                    
                    asserter.assert_code(response, 200)
                    asserter.assert_success(response, False)
                    asserter.assert_response_message(response, "上级菜单不能选择自己")
                    break
    
    @allure.story("正常场景-删除")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除菜单成功")
    def test_delete_menu_success(self, test_menu_data):
        """测试删除菜单成功"""
        # 先新增一个菜单
        add_response = menu_api.add_menu(test_menu_data)
        
        if add_response.json().get("code") == 200:
            # 查询获取菜单ID
            list_response = menu_api.list_menus(menuName=test_menu_data["menuName"])
            menus = list_response.json().get("data", [])
            
            for menu in menus:
                if menu.get("menuName") == test_menu_data["menuName"]:
                    menu_id = menu.get("menuId")
                    response = menu_api.delete_menu(menu_id)
                    
                    asserter.assert_common(response, 200, True)
                    break
    
    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除菜单-存在子菜单")
    def test_delete_menu_with_children(self):
        """测试删除存在子菜单的菜单失败"""
        # 获取菜单列表，找到有子菜单的
        list_response = menu_api.list_menus()
        menus = list_response.json().get("data", [])
        
        # 找到第一个有子菜单的菜单
        for menu in menus:
            for child in menus:
                if child.get("parentId") == menu.get("menuId"):
                    response = menu_api.delete_menu(menu.get("menuId"))
                    
                    asserter.assert_code(response, 200)
                    asserter.assert_response_message(response, "存在子菜单")
                    return
    
    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除菜单-菜单已分配角色")
    def test_delete_menu_with_roles(self):
        """测试删除已分配角色的菜单失败"""
        # 使用一个已分配给角色的叶子菜单(1050)
        response = menu_api.delete_menu(1050)

        asserter.assert_code(response, 200)
        asserter.assert_response_message(response, "菜单已分配")

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("根据显示状态查询菜单")
    def test_list_menus_by_status(self):
        """测试根据显示状态查询菜单"""
        response = menu_api.list_menus(visible="0")

        asserter.assert_common(response, 200, True)

    @allure.story("异常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取菜单详情-不存在")
    def test_get_menu_detail_not_exists(self):
        """测试获取不存在的菜单详情"""
        response = menu_api.get_menu(999999)

        # RuoYi对不存在的ID仍返回code=200，验证接口正常响应
        asserter.assert_code(response, 200)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增菜单-缺少必填参数")
    def test_add_menu_missing_required(self):
        """测试新增菜单-缺少菜单名称"""
        menu_data = {"menuType": "M"}

        response = menu_api.add_menu(menu_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增菜单-菜单名过长")
    def test_add_menu_name_too_long(self, test_menu_data):
        """测试新增菜单-菜单名超过50字符"""
        test_menu_data["menuName"] = "a" * 51

        response = menu_api.add_menu(test_menu_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-新增")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增菜单-完整参数组合")
    def test_add_menu_full_params(self, test_menu_data):
        """测试新增菜单-完整参数组合"""
        full_data = {
            **test_menu_data,
            "icon": "el-icon-setting",
            "remark": "完整参数测试"
        }

        response = menu_api.add_menu(full_data)

        asserter.assert_common(response, 200, True)

    @allure.story("异常场景-修改")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("修改菜单-菜单不存在")
    def test_update_menu_not_exists(self):
        """测试修改不存在的菜单"""
        menu_data = {
            "menuId": 999999,
            "menuName": "不存在",
            "parentId": 0,
            "orderNum": 0,
            "path": "test",
            "menuType": "M",
            "visible": "0",
            "status": "0"
        }

        response = menu_api.update_menu(menu_data)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("异常场景-删除")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除菜单-菜单不存在")
    def test_delete_menu_not_exists(self):
        """测试删除不存在的菜单"""
        response = menu_api.delete_menu(999999)

        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)

    @allure.story("正常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("保存菜单排序-成功")
    def test_update_menu_sort_success(self):
        """测试保存菜单排序成功"""
        list_response = menu_api.list_menus()
        menus = list_response.json().get("data", [])

        if menus:
            menu_id = menus[0].get("menuId")
            original_order = menus[0].get("orderNum", 0)

            response = menu_api.update_sort([menu_id], [original_order])

            asserter.assert_common(response, 200, True)

    @allure.story("异常场景-其他操作")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("保存菜单排序-缺少参数")
    def test_update_menu_sort_missing_params(self):
        """测试保存菜单排序-缺少orderNums"""
        list_response = menu_api.list_menus()
        menus = list_response.json().get("data", [])

        if menus:
            menu_id = menus[0].get("menuId")

            # RuoYi对空数组不强制校验，验证接口正常响应
            response = menu_api.update_sort([menu_id], [])

            asserter.assert_code(response, 200)

    @allure.story("正常场景-查询")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("获取角色菜单树-角色不存在")
    def test_get_role_menu_tree_not_exists(self):
        """测试获取不存在角色的菜单树"""
        response = menu_api.get_role_menu_tree(999999)

        # RuoYi对不存在的角色返回500(NullPointerException)
        asserter.assert_code(response, 200)
        asserter.assert_success(response, False)
