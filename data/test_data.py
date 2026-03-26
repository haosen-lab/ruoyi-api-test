"""
测试数据常量 - 集中管理测试数据和预期消息
"""

# ============ API路径配置 ============
API_PATHS = {
    "login": "/login",
    "captcha": "/captchaImage",
    "get_info": "/getInfo",
    "get_routers": "/getRouters",
    "logout": "/logout",
    # 系统管理
    "user": "/system/user",
    "role": "/system/role",
    "menu": "/system/menu",
    "dept": "/system/dept",
    "dict_type": "/system/dict/type",
    "dict_data": "/system/dict/data",
    "config": "/system/config",
    "notice": "/system/notice",
    "post": "/system/post",
    # 系统监控
    "logininfor": "/monitor/logininfor",
    "operlog": "/monitor/operlog",
}

# ============ 预期响应消息 ============
MSG = {
    "success": "操作成功",
    "query_success": "查询成功",
    "user_not_found": "用户不存在/密码错误",
    "user_exists": "登录账号已存在",
    "phone_exists": "手机号码已存在",
    "email_exists": "邮箱账号已存在",
    "role_name_exists": "角色名称已存在",
    "role_key_exists": "角色权限已存在",
    "menu_name_exists": "菜单名称已存在",
    "dept_name_exists": "部门名称已存在",
    "dict_type_exists": "字典类型已存在",
    "dict_type_used": "字典类型已分配,不能删除",
    "config_key_exists": "参数键名已存在",
    "config_builtin": "内置参数",
    "post_code_exists": "岗位编码已存在",
    "post_name_exists": "岗位名称已存在",
    "has_children_dept": "存在下级部门",
    "has_children_menu": "存在子菜单",
    "menu_assigned": "菜单已分配",
    "dept_has_users": "部门存在用户",
    "current_user_cannot_delete": "当前用户不能删除",
    "menu_self_parent": "上级菜单不能选择自己",
    "invalid_frame_url": "地址必须以http(s)://开头",
    "no_permission": "没有权限，请联系管理员授权",
    "captcha_required": "验证码错误",
}

# ============ 默认测试ID ============
DEFAULT_IDS = {
    "root_dept_id": 100,
    "admin_user_id": 1,
    "admin_role_id": 1,
    "common_role_id": 2,
    "chief_post_id": 1,
    "menu_log_id": 108,
}

# ============ 分页默认值 ============
PAGE = {
    "default_num": 1,
    "default_size": 10,
    "max_size": 100,
}
