# 若依后台管理系统接口文档

## 1. 认证相关接口

### 1.1 登录接口
- **路径**: `/login`
- **方法**: POST
- **功能**: 用户登录获取令牌
- **请求参数**:
  - `username`: 用户名 (必填)
  - `password`: 密码 (必填)
  - `code`: 验证码 (必填)
  - `uuid`: 验证码UUID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {
      "token": "eyJhbGciOiJIUzI1NiJ9..."
    }
  }
  ```
- **可测性**: 高 - 核心功能，必须测试

### 1.2 获取用户信息
- **路径**: `/getInfo`
- **方法**: GET
- **功能**: 获取当前登录用户信息
- **请求参数**: 无
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {
      "user": {...},
      "roles": ["admin"],
      "permissions": ["*:*:*"],
      "isDefaultModifyPwd": false,
      "isPasswordExpired": false
    }
  }
  ```
- **可测性**: 高 - 核心功能，必须测试

### 1.3 获取路由信息
- **路径**: `/getRouters`
- **方法**: GET
- **功能**: 获取用户菜单路由
- **请求参数**: 无
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [
      {
        "path": "/system",
        "component": "Layout",
        "children": [...]
      }
    ]
  }
  ```
- **可测性**: 高 - 核心功能，必须测试

## 2. 用户管理接口

### 2.1 获取用户列表
- **路径**: `/system/user/list`
- **方法**: GET
- **功能**: 获取用户列表（分页）
- **请求参数**:
  - `userName`: 用户名
  - `phonenumber`: 手机号码
  - `status`: 状态
  - `deptId`: 部门ID
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "rows": [...],
    "total": 100
  }
  ```
- **权限**: `system:user:list`
- **可测性**: 高 - 核心功能，必须测试

### 2.2 导出用户数据
- **路径**: `/system/user/export`
- **方法**: POST
- **功能**: 导出用户数据
- **请求参数**:
  - `userName`: 用户名
  - `phonenumber`: 手机号码
  - `status`: 状态
  - `deptId`: 部门ID
- **响应格式**: Excel文件
- **权限**: `system:user:export`
- **可测性**: 中 - 功能测试，建议测试

### 2.3 导入用户数据
- **路径**: `/system/user/importData`
- **方法**: POST
- **功能**: 导入用户数据
- **请求参数**:
  - `file`: Excel文件 (必填)
  - `updateSupport`: 是否更新支持 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:user:import`
- **可测性**: 中 - 功能测试，建议测试

### 2.4 获取用户详细信息
- **路径**: `/system/user/{userId}`
- **方法**: GET
- **功能**: 根据用户ID获取详细信息
- **请求参数**:
  - `userId`: 用户ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {
      "user": {...},
      "postIds": [...],
      "roleIds": [...],
      "roles": [...],
      "posts": [...]
    }
  }
  ```
- **权限**: `system:user:query`
- **可测性**: 高 - 核心功能，必须测试

### 2.5 新增用户
- **路径**: `/system/user`
- **方法**: POST
- **功能**: 新增用户
- **请求参数**:
  - `userName`: 用户名 (必填)
  - `password`: 密码 (必填)
  - `deptId`: 部门ID (必填)
  - `roleIds`: 角色ID数组 (必填)
  - `postIds`: 岗位ID数组
  - `phonenumber`: 手机号码
  - `email`: 邮箱
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:user:add`
- **可测性**: 高 - 核心功能，必须测试

### 2.6 修改用户
- **路径**: `/system/user`
- **方法**: PUT
- **功能**: 修改用户
- **请求参数**:
  - `userId`: 用户ID (必填)
  - `userName`: 用户名 (必填)
  - `deptId`: 部门ID (必填)
  - `roleIds`: 角色ID数组 (必填)
  - `postIds`: 岗位ID数组
  - `phonenumber`: 手机号码
  - `email`: 邮箱
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:user:edit`
- **可测性**: 高 - 核心功能，必须测试

### 2.7 删除用户
- **路径**: `/system/user/{userIds}`
- **方法**: DELETE
- **功能**: 删除用户
- **请求参数**:
  - `userIds`: 用户ID数组 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:user:remove`
- **可测性**: 高 - 核心功能，必须测试

### 2.8 重置密码
- **路径**: `/system/user/resetPwd`
- **方法**: PUT
- **功能**: 重置用户密码
- **请求参数**:
  - `userId`: 用户ID (必填)
  - `password`: 新密码 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:user:resetPwd`
- **可测性**: 高 - 核心功能，必须测试

### 2.9 修改用户状态
- **路径**: `/system/user/changeStatus`
- **方法**: PUT
- **功能**: 修改用户状态
- **请求参数**:
  - `userId`: 用户ID (必填)
  - `status`: 状态 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:user:edit`
- **可测性**: 高 - 核心功能，必须测试

### 2.10 获取部门树
- **路径**: `/system/user/deptTree`
- **方法**: GET
- **功能**: 获取部门树
- **请求参数**:
  - `deptName`: 部门名称
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...]
  }
  ```
- **权限**: `system:user:list`
- **可测性**: 中 - 功能测试，建议测试

## 3. 角色管理接口

### 3.1 获取角色列表
- **路径**: `/system/role/list`
- **方法**: GET
- **功能**: 获取角色列表（分页）
- **请求参数**:
  - `roleName`: 角色名称
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "rows": [...],
    "total": 100
  }
  ```
- **权限**: `system:role:list`
- **可测性**: 高 - 核心功能，必须测试

### 3.2 导出角色数据
- **路径**: `/system/role/export`
- **方法**: POST
- **功能**: 导出角色数据
- **请求参数**:
  - `roleName`: 角色名称
  - `status`: 状态
- **响应格式**: Excel文件
- **权限**: `system:role:export`
- **可测性**: 中 - 功能测试，建议测试

### 3.3 获取角色详细信息
- **路径**: `/system/role/{roleId}`
- **方法**: GET
- **功能**: 根据角色ID获取详细信息
- **请求参数**:
  - `roleId`: 角色ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {...}
  }
  ```
- **权限**: `system:role:query`
- **可测性**: 高 - 核心功能，必须测试

### 3.4 新增角色
- **路径**: `/system/role`
- **方法**: POST
- **功能**: 新增角色
- **请求参数**:
  - `roleName`: 角色名称 (必填)
  - `roleKey`: 角色权限字符串 (必填)
  - `roleSort`: 显示顺序 (必填)
  - `menuIds`: 菜单ID数组
  - `deptIds`: 部门ID数组
  - `status`: 状态
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:role:add`
- **可测性**: 高 - 核心功能，必须测试

### 3.5 修改角色
- **路径**: `/system/role`
- **方法**: PUT
- **功能**: 修改角色
- **请求参数**:
  - `roleId`: 角色ID (必填)
  - `roleName`: 角色名称 (必填)
  - `roleKey`: 角色权限字符串 (必填)
  - `roleSort`: 显示顺序 (必填)
  - `menuIds`: 菜单ID数组
  - `deptIds`: 部门ID数组
  - `status`: 状态
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:role:edit`
- **可测性**: 高 - 核心功能，必须测试

### 3.6 修改数据权限
- **路径**: `/system/role/dataScope`
- **方法**: PUT
- **功能**: 修改角色数据权限
- **请求参数**:
  - `roleId`: 角色ID (必填)
  - `dataScope`: 数据范围 (必填)
  - `deptIds`: 部门ID数组
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:role:edit`
- **可测性**: 高 - 核心功能，必须测试

### 3.7 修改角色状态
- **路径**: `/system/role/changeStatus`
- **方法**: PUT
- **功能**: 修改角色状态
- **请求参数**:
  - `roleId`: 角色ID (必填)
  - `status`: 状态 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:role:edit`
- **可测性**: 高 - 核心功能，必须测试

### 3.8 删除角色
- **路径**: `/system/role/{roleIds}`
- **方法**: DELETE
- **功能**: 删除角色
- **请求参数**:
  - `roleIds`: 角色ID数组 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:role:remove`
- **可测性**: 高 - 核心功能，必须测试

### 3.9 获取角色选择框列表
- **路径**: `/system/role/optionselect`
- **方法**: GET
- **功能**: 获取角色选择框列表
- **请求参数**: 无
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...]
  }
  ```
- **权限**: `system:role:query`
- **可测性**: 中 - 功能测试，建议测试

## 4. 菜单管理接口

### 4.1 获取菜单列表
- **路径**: `/system/menu/list`
- **方法**: GET
- **功能**: 获取菜单列表
- **请求参数**:
  - `menuName`: 菜单名称
  - `visible`: 显示状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...]
  }
  ```
- **权限**: `system:menu:list`
- **可测性**: 高 - 核心功能，必须测试

### 4.2 获取菜单详细信息
- **路径**: `/system/menu/{menuId}`
- **方法**: GET
- **功能**: 根据菜单ID获取详细信息
- **请求参数**:
  - `menuId`: 菜单ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {...}
  }
  ```
- **权限**: `system:menu:query`
- **可测性**: 高 - 核心功能，必须测试

### 4.3 获取菜单下拉树
- **路径**: `/system/menu/treeselect`
- **方法**: GET
- **功能**: 获取菜单下拉树
- **请求参数**:
  - `menuName`: 菜单名称
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...]
  }
  ```
- **可测性**: 中 - 功能测试，建议测试

### 4.4 获取角色菜单树
- **路径**: `/system/menu/roleMenuTreeselect/{roleId}`
- **方法**: GET
- **功能**: 获取角色菜单树
- **请求参数**:
  - `roleId`: 角色ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {
      "checkedKeys": [...],
      "menus": [...]
    }
  }
  ```
- **可测性**: 中 - 功能测试，建议测试

### 4.5 新增菜单
- **路径**: `/system/menu`
- **方法**: POST
- **功能**: 新增菜单
- **请求参数**:
  - `menuName`: 菜单名称 (必填)
  - `parentId`: 父菜单ID (必填)
  - `orderNum`: 显示顺序 (必填)
  - `menuType`: 菜单类型 (必填)
  - `path`: 路由地址
  - `component`: 组件路径
  - `perms`: 权限标识
  - `icon`: 菜单图标
  - `visible`: 显示状态
  - `isFrame`: 是否外链
  - `isCache`: 是否缓存
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:menu:add`
- **可测性**: 高 - 核心功能，必须测试

### 4.6 修改菜单
- **路径**: `/system/menu`
- **方法**: PUT
- **功能**: 修改菜单
- **请求参数**:
  - `menuId`: 菜单ID (必填)
  - `menuName`: 菜单名称 (必填)
  - `parentId`: 父菜单ID (必填)
  - `orderNum`: 显示顺序 (必填)
  - `menuType`: 菜单类型 (必填)
  - `path`: 路由地址
  - `component`: 组件路径
  - `perms`: 权限标识
  - `icon`: 菜单图标
  - `visible`: 显示状态
  - `isFrame`: 是否外链
  - `isCache`: 是否缓存
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:menu:edit`
- **可测性**: 高 - 核心功能，必须测试

### 4.7 保存菜单排序
- **路径**: `/system/menu/updateSort`
- **方法**: PUT
- **功能**: 保存菜单排序
- **请求参数**:
  - `menuIds`: 菜单ID数组 (必填)
  - `orderNums`: 排序数组 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:menu:edit`
- **可测性**: 中 - 功能测试，建议测试

### 4.8 删除菜单
- **路径**: `/system/menu/{menuId}`
- **方法**: DELETE
- **功能**: 删除菜单
- **请求参数**:
  - `menuId`: 菜单ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:menu:remove`
- **可测性**: 高 - 核心功能，必须测试

## 5. 部门管理接口

### 5.1 获取部门列表
- **路径**: `/system/dept/list`
- **方法**: GET
- **功能**: 获取部门列表
- **请求参数**:
  - `deptName`: 部门名称
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...]
  }
  ```
- **权限**: `system:dept:list`
- **可测性**: 高 - 核心功能，必须测试

### 5.2 获取部门列表（排除节点）
- **路径**: `/system/dept/list/exclude/{deptId}`
- **方法**: GET
- **功能**: 查询部门列表（排除指定节点）
- **请求参数**:
  - `deptId`: 部门ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...]
  }
  ```
- **权限**: `system:dept:list`
- **可测性**: 中 - 功能测试，建议测试

### 5.3 获取部门详细信息
- **路径**: `/system/dept/{deptId}`
- **方法**: GET
- **功能**: 根据部门ID获取详细信息
- **请求参数**:
  - `deptId`: 部门ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {...}
  }
  ```
- **权限**: `system:dept:query`
- **可测性**: 高 - 核心功能，必须测试

### 5.4 新增部门
- **路径**: `/system/dept`
- **方法**: POST
- **功能**: 新增部门
- **请求参数**:
  - `deptName`: 部门名称 (必填)
  - `parentId`: 父部门ID (必填)
  - `orderNum`: 显示顺序 (必填)
  - `leader`: 负责人
  - `phone`: 联系电话
  - `email`: 邮箱
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dept:add`
- **可测性**: 高 - 核心功能，必须测试

### 5.5 修改部门
- **路径**: `/system/dept`
- **方法**: PUT
- **功能**: 修改部门
- **请求参数**:
  - `deptId`: 部门ID (必填)
  - `deptName`: 部门名称 (必填)
  - `parentId`: 父部门ID (必填)
  - `orderNum`: 显示顺序 (必填)
  - `leader`: 负责人
  - `phone`: 联系电话
  - `email`: 邮箱
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dept:edit`
- **可测性**: 高 - 核心功能，必须测试

### 5.6 保存部门排序
- **路径**: `/system/dept/updateSort`
- **方法**: PUT
- **功能**: 保存部门排序
- **请求参数**:
  - `deptIds`: 部门ID数组 (必填)
  - `orderNums`: 排序数组 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dept:edit`
- **可测性**: 中 - 功能测试，建议测试

### 5.7 删除部门
- **路径**: `/system/dept/{deptId}`
- **方法**: DELETE
- **功能**: 删除部门
- **请求参数**:
  - `deptId`: 部门ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dept:remove`
- **可测性**: 高 - 核心功能，必须测试

## 6. 字典管理接口

### 6.1 获取字典类型列表
- **路径**: `/system/dict/type/list`
- **方法**: GET
- **功能**: 获取字典类型列表（分页）
- **请求参数**:
  - `dictName`: 字典名称
  - `dictType`: 字典类型
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "rows": [...],
    "total": 100
  }
  ```
- **权限**: `system:dict:list`
- **可测性**: 高 - 核心功能，必须测试

### 6.2 导出字典类型
- **路径**: `/system/dict/type/export`
- **方法**: POST
- **功能**: 导出字典类型
- **请求参数**:
  - `dictName`: 字典名称
  - `dictType`: 字典类型
  - `status`: 状态
- **响应格式**: Excel文件
- **权限**: `system:dict:export`
- **可测性**: 中 - 功能测试，建议测试

### 6.3 获取字典类型详细信息
- **路径**: `/system/dict/type/{dictId}`
- **方法**: GET
- **功能**: 根据字典ID获取详细信息
- **请求参数**:
  - `dictId`: 字典ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {...}
  }
  ```
- **权限**: `system:dict:query`
- **可测性**: 高 - 核心功能，必须测试

### 6.4 新增字典类型
- **路径**: `/system/dict/type`
- **方法**: POST
- **功能**: 新增字典类型
- **请求参数**:
  - `dictName`: 字典名称 (必填)
  - `dictType`: 字典类型 (必填)
  - `sort`: 显示顺序 (必填)
  - `status`: 状态
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dict:add`
- **可测性**: 高 - 核心功能，必须测试

### 6.5 修改字典类型
- **路径**: `/system/dict/type`
- **方法**: PUT
- **功能**: 修改字典类型
- **请求参数**:
  - `dictId`: 字典ID (必填)
  - `dictName`: 字典名称 (必填)
  - `dictType`: 字典类型 (必填)
  - `sort`: 显示顺序 (必填)
  - `status`: 状态
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dict:edit`
- **可测性**: 高 - 核心功能，必须测试

### 6.6 删除字典类型
- **路径**: `/system/dict/type/{dictIds}`
- **方法**: DELETE
- **功能**: 删除字典类型
- **请求参数**:
  - `dictIds`: 字典ID数组 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dict:remove`
- **可测性**: 高 - 核心功能，必须测试

### 6.7 刷新字典缓存
- **路径**: `/system/dict/type/refreshCache`
- **方法**: DELETE
- **功能**: 刷新字典缓存
- **请求参数**: 无
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dict:remove`
- **可测性**: 中 - 功能测试，建议测试

### 6.8 获取字典选择框列表
- **路径**: `/system/dict/type/optionselect`
- **方法**: GET
- **功能**: 获取字典选择框列表
- **请求参数**: 无
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...]
  }
  ```
- **可测性**: 中 - 功能测试，建议测试

### 6.9 获取字典数据列表
- **路径**: `/system/dict/data/list`
- **方法**: GET
- **功能**: 获取字典数据列表（分页）
- **请求参数**:
  - `dictType`: 字典类型
  - `dictLabel`: 字典标签
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "rows": [...],
    "total": 100
  }
  ```
- **权限**: `system:dict:list`
- **可测性**: 高 - 核心功能，必须测试

### 6.10 导出字典数据
- **路径**: `/system/dict/data/export`
- **方法**: POST
- **功能**: 导出字典数据
- **请求参数**:
  - `dictType`: 字典类型
  - `dictLabel`: 字典标签
  - `status`: 状态
- **响应格式**: Excel文件
- **权限**: `system:dict:export`
- **可测性**: 中 - 功能测试，建议测试

### 6.11 获取字典数据详细信息
- **路径**: `/system/dict/data/{dictCode}`
- **方法**: GET
- **功能**: 根据字典编码获取详细信息
- **请求参数**:
  - `dictCode`: 字典编码 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {...}
  }
  ```
- **权限**: `system:dict:query`
- **可测性**: 高 - 核心功能，必须测试

### 6.12 根据字典类型获取字典数据
- **路径**: `/system/dict/data/type/{dictType}`
- **方法**: GET
- **功能**: 根据字典类型获取字典数据
- **请求参数**:
  - `dictType`: 字典类型 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...]
  }
  ```
- **可测性**: 高 - 核心功能，必须测试

### 6.13 新增字典数据
- **路径**: `/system/dict/data`
- **方法**: POST
- **功能**: 新增字典数据
- **请求参数**:
  - `dictType`: 字典类型 (必填)
  - `dictLabel`: 字典标签 (必填)
  - `dictValue`: 字典值 (必填)
  - `sort`: 显示顺序 (必填)
  - `status`: 状态
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dict:add`
- **可测性**: 高 - 核心功能，必须测试

### 6.14 修改字典数据
- **路径**: `/system/dict/data`
- **方法**: PUT
- **功能**: 修改字典数据
- **请求参数**:
  - `dictCode`: 字典编码 (必填)
  - `dictType`: 字典类型 (必填)
  - `dictLabel`: 字典标签 (必填)
  - `dictValue`: 字典值 (必填)
  - `sort`: 显示顺序 (必填)
  - `status`: 状态
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dict:edit`
- **可测性**: 高 - 核心功能，必须测试

### 6.15 删除字典数据
- **路径**: `/system/dict/data/{dictCodes}`
- **方法**: DELETE
- **功能**: 删除字典数据
- **请求参数**:
  - `dictCodes`: 字典编码数组 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:dict:remove`
- **可测性**: 高 - 核心功能，必须测试

## 7. 配置管理接口

### 7.1 获取配置列表
- **路径**: `/system/config/list`
- **方法**: GET
- **功能**: 获取配置列表（分页）
- **请求参数**:
  - `configName`: 配置名称
  - `configKey`: 配置键名
  - `configType`: 配置类型
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "rows": [...],
    "total": 100
  }
  ```
- **权限**: `system:config:list`
- **可测性**: 高 - 核心功能，必须测试

### 7.2 导出配置数据
- **路径**: `/system/config/export`
- **方法**: POST
- **功能**: 导出配置数据
- **请求参数**:
  - `configName`: 配置名称
  - `configKey`: 配置键名
  - `configType`: 配置类型
- **响应格式**: Excel文件
- **权限**: `system:config:export`
- **可测性**: 中 - 功能测试，建议测试

### 7.3 获取配置详细信息
- **路径**: `/system/config/{configId}`
- **方法**: GET
- **功能**: 根据配置ID获取详细信息
- **请求参数**:
  - `configId`: 配置ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {...}
  }
  ```
- **权限**: `system:config:query`
- **可测性**: 高 - 核心功能，必须测试

### 7.4 根据配置键名获取配置值
- **路径**: `/system/config/configKey/{configKey}`
- **方法**: GET
- **功能**: 根据配置键名获取配置值
- **请求参数**:
  - `configKey`: 配置键名 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": "配置值"
  }
  ```
- **可测性**: 高 - 核心功能，必须测试

### 7.5 新增配置
- **路径**: `/system/config`
- **方法**: POST
- **功能**: 新增配置
- **请求参数**:
  - `configName`: 配置名称 (必填)
  - `configKey`: 配置键名 (必填)
  - `configValue`: 配置值 (必填)
  - `configType`: 配置类型
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:config:add`
- **可测性**: 高 - 核心功能，必须测试

### 7.6 修改配置
- **路径**: `/system/config`
- **方法**: PUT
- **功能**: 修改配置
- **请求参数**:
  - `configId`: 配置ID (必填)
  - `configName`: 配置名称 (必填)
  - `configKey`: 配置键名 (必填)
  - `configValue`: 配置值 (必填)
  - `configType`: 配置类型
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:config:edit`
- **可测性**: 高 - 核心功能，必须测试

### 7.7 删除配置
- **路径**: `/system/config/{configIds}`
- **方法**: DELETE
- **功能**: 删除配置
- **请求参数**:
  - `configIds`: 配置ID数组 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:config:remove`
- **可测性**: 高 - 核心功能，必须测试

### 7.8 刷新配置缓存
- **路径**: `/system/config/refreshCache`
- **方法**: DELETE
- **功能**: 刷新配置缓存
- **请求参数**: 无
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:config:remove`
- **可测性**: 中 - 功能测试，建议测试

## 8. 通知管理接口

### 8.1 获取通知列表
- **路径**: `/system/notice/list`
- **方法**: GET
- **功能**: 获取通知列表（分页）
- **请求参数**:
  - `noticeTitle`: 通知标题
  - `noticeType`: 通知类型
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "rows": [...],
    "total": 100
  }
  ```
- **权限**: `system:notice:list`
- **可测性**: 高 - 核心功能，必须测试

### 8.2 获取通知详细信息
- **路径**: `/system/notice/{noticeId}`
- **方法**: GET
- **功能**: 根据通知ID获取详细信息
- **请求参数**:
  - `noticeId`: 通知ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {...}
  }
  ```
- **权限**: `system:notice:query`
- **可测性**: 高 - 核心功能，必须测试

### 8.3 新增通知
- **路径**: `/system/notice`
- **方法**: POST
- **功能**: 新增通知
- **请求参数**:
  - `noticeTitle`: 通知标题 (必填)
  - `noticeType`: 通知类型 (必填)
  - `noticeContent`: 通知内容 (必填)
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:notice:add`
- **可测性**: 高 - 核心功能，必须测试

### 8.4 修改通知
- **路径**: `/system/notice`
- **方法**: PUT
- **功能**: 修改通知
- **请求参数**:
  - `noticeId`: 通知ID (必填)
  - `noticeTitle`: 通知标题 (必填)
  - `noticeType`: 通知类型 (必填)
  - `noticeContent`: 通知内容 (必填)
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:notice:edit`
- **可测性**: 高 - 核心功能，必须测试

### 8.5 获取顶部通知列表
- **路径**: `/system/notice/listTop`
- **方法**: GET
- **功能**: 获取首页顶部通知列表
- **请求参数**: 无
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...],
    "unreadCount": 5
  }
  ```
- **可测性**: 高 - 核心功能，必须测试

### 8.6 标记通知已读
- **路径**: `/system/notice/markRead`
- **方法**: POST
- **功能**: 标记通知已读
- **请求参数**:
  - `noticeId`: 通知ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **可测性**: 高 - 核心功能，必须测试

### 8.7 批量标记已读
- **路径**: `/system/notice/markReadAll`
- **方法**: POST
- **功能**: 批量标记通知已读
- **请求参数**:
  - `ids`: 通知ID字符串 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **可测性**: 中 - 功能测试，建议测试

### 8.8 删除通知
- **路径**: `/system/notice/{noticeIds}`
- **方法**: DELETE
- **功能**: 删除通知
- **请求参数**:
  - `noticeIds`: 通知ID数组 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:notice:remove`
- **可测性**: 高 - 核心功能，必须测试

## 9. 岗位管理接口

### 9.1 获取岗位列表
- **路径**: `/system/post/list`
- **方法**: GET
- **功能**: 获取岗位列表（分页）
- **请求参数**:
  - `postName`: 岗位名称
  - `postCode`: 岗位编码
  - `status`: 状态
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "rows": [...],
    "total": 100
  }
  ```
- **权限**: `system:post:list`
- **可测性**: 高 - 核心功能，必须测试

### 9.2 导出岗位数据
- **路径**: `/system/post/export`
- **方法**: POST
- **功能**: 导出岗位数据
- **请求参数**:
  - `postName`: 岗位名称
  - `postCode`: 岗位编码
  - `status`: 状态
- **响应格式**: Excel文件
- **权限**: `system:post:export`
- **可测性**: 中 - 功能测试，建议测试

### 9.3 获取岗位详细信息
- **路径**: `/system/post/{postId}`
- **方法**: GET
- **功能**: 根据岗位ID获取详细信息
- **请求参数**:
  - `postId`: 岗位ID (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": {...}
  }
  ```
- **权限**: `system:post:query`
- **可测性**: 高 - 核心功能，必须测试

### 9.4 新增岗位
- **路径**: `/system/post`
- **方法**: POST
- **功能**: 新增岗位
- **请求参数**:
  - `postName`: 岗位名称 (必填)
  - `postCode`: 岗位编码 (必填)
  - `postSort`: 显示顺序 (必填)
  - `status`: 状态
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:post:add`
- **可测性**: 高 - 核心功能，必须测试

### 9.5 修改岗位
- **路径**: `/system/post`
- **方法**: PUT
- **功能**: 修改岗位
- **请求参数**:
  - `postId`: 岗位ID (必填)
  - `postName`: 岗位名称 (必填)
  - `postCode`: 岗位编码 (必填)
  - `postSort`: 显示顺序 (必填)
  - `status`: 状态
  - `remark`: 备注
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:post:edit`
- **可测性**: 高 - 核心功能，必须测试

### 9.6 删除岗位
- **路径**: `/system/post/{postIds}`
- **方法**: DELETE
- **功能**: 删除岗位
- **请求参数**:
  - `postIds`: 岗位ID数组 (必填)
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功"
  }
  ```
- **权限**: `system:post:remove`
- **可测性**: 高 - 核心功能，必须测试

### 9.7 获取岗位选择框列表
- **路径**: `/system/post/optionselect`
- **方法**: GET
- **功能**: 获取岗位选择框列表
- **请求参数**: 无
- **响应格式**:
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": [...]
  }
  ```
- **可测性**: 中 - 功能测试，建议测试

## 10. 接口可测性分析

### 10.1 高可测性接口
以下接口具有高可测性，建议优先测试：

#### 认证相关
- 登录接口 (`/login`)
- 获取用户信息 (`/getInfo`)
- 获取路由信息 (`/getRouters`)

#### 用户管理
- 获取用户列表 (`/system/user/list`)
- 获取用户详细信息 (`/system/user/{userId}`)
- 新增用户 (`/system/user`)
- 修改用户 (`/system/user`)
- 删除用户 (`/system/user/{userIds}`)
- 重置密码 (`/system/user/resetPwd`)
- 修改用户状态 (`/system/user/changeStatus`)

#### 角色管理
- 获取角色列表 (`/system/role/list`)
- 获取角色详细信息 (`/system/role/{roleId}`)
- 新增角色 (`/system/role`)
- 修改角色 (`/system/role`)
- 修改数据权限 (`/system/role/dataScope`)
- 修改角色状态 (`/system/role/changeStatus`)
- 删除角色 (`/system/role/{roleIds}`)

#### 菜单管理
- 获取菜单列表 (`/system/menu/list`)
- 获取菜单详细信息 (`/system/menu/{menuId}`)
- 新增菜单 (`/system/menu`)
- 修改菜单 (`/system/menu`)
- 删除菜单 (`/system/menu/{menuId}`)

#### 部门管理
- 获取部门列表 (`/system/dept/list`)
- 获取部门详细信息 (`/system/dept/{deptId}`)
- 新增部门 (`/system/dept`)
- 修改部门 (`/system/dept`)
- 删除部门 (`/system/dept/{deptId}`)

#### 字典管理
- 获取字典类型列表 (`/system/dict/type/list`)
- 获取字典类型详细信息 (`/system/dict/type/{dictId}`)
- 新增字典类型 (`/system/dict/type`)
- 修改字典类型 (`/system/dict/type`)
- 删除字典类型 (`/system/dict/type/{dictIds}`)
- 获取字典数据列表 (`/system/dict/data/list`)
- 获取字典数据详细信息 (`/system/dict/data/{dictCode}`)
- 根据字典类型获取字典数据 (`/system/dict/data/type/{dictType}`)
- 新增字典数据 (`/system/dict/data`)
- 修改字典数据 (`/system/dict/data`)
- 删除字典数据 (`/system/dict/data/{dictCodes}`)

#### 配置管理
- 获取配置列表 (`/system/config/list`)
- 获取配置详细信息 (`/system/config/{configId}`)
- 根据配置键名获取配置值 (`/system/config/configKey/{configKey}`)
- 新增配置 (`/system/config`)
- 修改配置 (`/system/config`)
- 删除配置 (`/system/config/{configIds}`)

#### 通知管理
- 获取通知列表 (`/system/notice/list`)
- 获取通知详细信息 (`/system/notice/{noticeId}`)
- 新增通知 (`/system/notice`)
- 修改通知 (`/system/notice`)
- 获取顶部通知列表 (`/system/notice/listTop`)
- 标记通知已读 (`/system/notice/markRead`)
- 删除通知 (`/system/notice/{noticeIds}`)

#### 岗位管理
- 获取岗位列表 (`/system/post/list`)
- 获取岗位详细信息 (`/system/post/{postId}`)
- 新增岗位 (`/system/post`)
- 修改岗位 (`/system/post`)
- 删除岗位 (`/system/post/{postIds}`)

### 10.2 中等可测性接口
以下接口具有中等可测性，建议选择性测试：

#### 导出功能
- 导出用户数据 (`/system/user/export`)
- 导出角色数据 (`/system/role/export`)
- 导出字典类型 (`/system/dict/type/export`)
- 导出字典数据 (`/system/dict/data/export`)
- 导出配置数据 (`/system/config/export`)
- 导出岗位数据 (`/system/post/export`)

#### 导入功能
- 导入用户数据 (`/system/user/importData`)

#### 缓存刷新
- 刷新字典缓存 (`/system/dict/type/refreshCache`)
- 刷新配置缓存 (`/system/config/refreshCache`)

#### 选择框列表
- 获取角色选择框列表 (`/system/role/optionselect`)
- 获取字典选择框列表 (`/system/dict/type/optionselect`)
- 获取岗位选择框列表 (`/system/post/optionselect`)

#### 树形结构
- 获取部门树 (`/system/user/deptTree`)
- 获取菜单下拉树 (`/system/menu/treeselect`)
- 获取角色菜单树 (`/system/menu/roleMenuTreeselect/{roleId}`)
- 获取部门列表（排除节点）(`/system/dept/list/exclude/{deptId}`)

#### 排序功能
- 保存菜单排序 (`/system/menu/updateSort`)
- 保存部门排序 (`/system/dept/updateSort`)

#### 批量操作
- 批量标记已读 (`/system/notice/markReadAll`)

### 10.3 低可测性接口
以下接口可测性较低，或测试价值不大：

- 导入模板下载 (`/system/user/importTemplate`) - 功能单一，测试价值低
- 角色授权相关接口 - 通常与其他接口组合测试
- 数据权限分配接口 - 通常与角色管理一起测试

## 11. 测试建议

1. **优先测试核心功能**：认证、用户管理、角色管理、菜单管理等核心模块
2. **关注权限控制**：测试不同角色的权限访问控制
3. **测试边界情况**：如参数验证、异常处理
4. **集成测试**：测试接口之间的依赖关系
5. **性能测试**：对高频接口进行性能测试
6. **安全性测试**：测试接口的安全性，如SQL注入、XSS等

## 12. 总结

本接口文档基于若依后台管理系统的源代码分析，涵盖了系统的主要功能模块。文档详细描述了每个接口的路径、方法、功能、参数和响应格式，并分析了接口的可测性，为自动化测试提供了参考。

在实际测试中，建议根据项目的具体需求和优先级，选择合适的接口进行测试，确保系统的稳定性和安全性。