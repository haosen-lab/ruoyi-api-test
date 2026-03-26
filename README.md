# 若依后台管理系统接口自动化测试框架

基于 Python + Pytest + Allure 的分层自动化测试框架

## 项目结构

```
ruoyi_api_test/
├── api/                    # API层 - 接口封装
│   ├── __init__.py
│   ├── login_api.py       # 登录认证接口
│   ├── user_api.py        # 用户管理接口
│   ├── role_api.py        # 角色管理接口
│   ├── menu_api.py        # 菜单管理接口
│   ├── dept_api.py        # 部门管理接口
│   ├── dict_api.py        # 字典管理接口
│   ├── config_api.py      # 参数配置接口
│   ├── notice_api.py      # 通知公告接口
│   └── post_api.py        # 岗位管理接口
├── testcases/             # 用例层 - 测试用例
│   ├── __init__.py
│   ├── conftest.py        # Pytest配置和Fixture
│   ├── test_login.py      # 登录测试用例
│   ├── test_user.py       # 用户管理测试用例
│   ├── test_role.py       # 角色管理测试用例
│   ├── test_menu.py       # 菜单管理测试用例
│   ├── test_dept.py       # 部门管理测试用例
│   └── ...
├── data/                  # 数据层 - 测试数据
│   └── __init__.py
├── utils/                 # 工具类
│   ├── __init__.py
│   ├── request_utils.py   # HTTP请求封装
│   ├── assert_utils.py    # 断言工具
│   └── data_generator.py  # 测试数据生成器
├── config/                # 配置层
│   ├── __init__.py
│   └── settings.py        # 项目配置
├── reports/               # 报告层
│   ├── allure-results/    # Allure原始结果
│   └── allure-report/     # Allure HTML报告
├── pytest.ini             # Pytest配置
├── requirements.txt       # 依赖包
└── run_tests.py          # 测试运行脚本
```

## 环境要求

- Python 3.8+
- 若依后台管理系统已部署（默认后端端口8080）
- Allure Commandline（用于生成报告）

## 安装依赖

```bash
pip install -r requirements.txt
```

### 安装 Allure Commandline

**Windows:**
```bash
# 使用 Scoop 安装
scoop install allure

# 或使用 Chocolatey
choco install allure-commandline
```

**Mac:**
```bash
brew install allure
```

## 配置说明

修改 `config/settings.py` 中的配置：

```python
# 基础配置
BASE_URL = "http://localhost:8080"  # 后端服务地址

# 管理员账号
ADMIN_USER = {
    "username": "admin",
    "password": "admin123"
}
```

## 运行测试

### 方式一：使用运行脚本

```bash
# 运行所有测试
python run_tests.py

# 运行指定模块的测试
python run_tests.py -m login
python run_tests.py -m user

# 不生成报告
python run_tests.py --no-report

# 清理报告
python run_tests.py --clean

# 启动报告服务
python run_tests.py --serve
```

### 方式二：使用 pytest 命令

```bash
# 运行所有测试
pytest testcases/ -v

# 运行指定模块
pytest testcases/test_login.py -v

# 运行指定标记的测试
pytest testcases/ -m "login" -v

# 生成 Allure 报告
pytest testcases/ -v --alluredir=reports/allure-results

# 生成 HTML 报告
allure generate reports/allure-results -o reports/allure-report --clean

# 启动报告服务
allure serve reports/allure-results
```

## 测试用例设计

### 登录认证模块 (test_login.py)
- 正常登录场景
- 异常登录场景（错误用户名、密码等）
- 边界值测试（用户名、密码长度）
- 安全测试（SQL注入、XSS攻击）
- 获取验证码、用户信息、路由信息

### 用户管理模块 (test_user.py)
- 用户列表查询（分页、条件筛选）
- 新增用户（正向、重复用户名/手机号/邮箱）
- 修改用户
- 删除用户
- 重置密码
- 修改用户状态
- 用户授权角色

### 角色管理模块 (test_role.py)
- 角色列表查询
- 新增角色
- 修改角色
- 删除角色
- 修改角色状态
- 数据权限管理
- 角色用户分配

### 菜单管理模块 (test_menu.py)
- 菜单列表查询
- 菜单树查询
- 新增菜单
- 修改菜单
- 删除菜单

### 部门管理模块 (test_dept.py)
- 部门列表查询
- 新增部门
- 修改部门
- 删除部门

## 框架特点

1. **分层设计**
   - API层：封装所有接口请求
   - 用例层：实现测试逻辑
   - 数据层：管理测试数据
   - 工具层：提供通用工具

2. **完善的测试覆盖**
   - 正向场景测试
   - 逆向场景测试
   - 边界值测试
   - 参数组合测试
   - 安全测试（SQL注入、XSS）

3. **Allure报告**
   - 详细的测试步骤
   - 请求/响应数据展示
   - 测试分类和标记
   - 失败截图和日志

4. **数据驱动**
   - 使用Fixture生成测试数据
   - 支持参数化测试
   - 动态数据生成

5. **易于维护**
   - 代码结构清晰
   - 配置与代码分离
   - 统一的断言方法

## 扩展新模块

1. 在 `api/` 目录下创建新的API封装文件
2. 在 `testcases/` 目录下创建对应的测试用例文件
3. 在 `conftest.py` 中添加需要的Fixture

## 注意事项

1. 运行测试前确保若依后台服务已启动
2. 首次运行可能需要初始化数据库
3. 测试会创建和删除数据，建议在测试环境运行
4. 部分测试用例依赖其他模块的数据，需要按顺序运行

## 常见问题

**Q: 报告生成失败？**
A: 确保已安装 Allure Commandline 并添加到系统PATH

**Q: 测试连接失败？**
A: 检查 `config/settings.py` 中的 `BASE_URL` 配置是否正确

**Q: 登录失败？**
A: 检查管理员账号密码是否正确，以及验证码是否关闭
