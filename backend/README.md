# Bux 后端开发文档

本系统为Bux系统后端服务，用于Bux系统微信小程序后端及Web管理界面后端，系统功能为在线购物

技术栈：

- python
    - FastAPI：web后端框架
    - motor ：mongo 异步驱动
    - watchdog：代码自动重启
    - argon2：用户密码hash
    -  `gettext` `babel `：多语言支持
- Redis:  缓存
- Nginx: 反向代理
- ： 队列



## 系统设计

### 用户管理

> 微信小程序端

微信小程序端仅有用户登录和注销功能，更多管理功能在web端实现

> web端

web端支持微信登录和账户密码登录，管理员可以管理：

- 用户（客户）账户
- 用户权限（管理员及其他分工）



### 微信小程序界面管理

#### 首页轮播图



#### 首页分类



#### 首页导航



#### 顶层商品推广



#### 其他界面设计





### 微信小程序商品管理

#### 上架与下架





#### 优惠券与会员





#### 商品状态管理





#### 售后管理





#### 其他





## 系统实现



### 全局数据库连接

本系统使用Mongo数据库，使用motor异步驱动，在系统启动时挂载数据库连接

> startup.py

```python
@asynccontextmanager
async def lifespan(a: FastAPI):
    """
    将mongodb连接对象挂载到app 保持整个生命周期可用
    :param a:
    :return:
    """
    # 启动时初始化 MongoDB
    db_conf = config["database"]["mongodb"]
    a.state.mongodb_client = AsyncIOMotorClient(db_conf["db_uri"])
    a.state.mongodb = app.state.mongodb_client[db_conf["db_name"]]
    print("✅ MongoDB 连接已建立")

    yield  # 应用运行期间保持连接

    # 关闭时清理
    a.state.mongodb_client.close()
    print("❌ MongoDB 连接已关闭")
    
app = create_app(prefix="/api/v1", lifespan=lifespan)
```



> motor curd演示

```python
# 假设已存在集合对象: collection

# 1. 新增操作
## 插入单条文档
await collection.insert_one({
    "name": "笔记本电脑",
    "price": 5999,
    "category": "电子设备"
})

## 插入多条文档
await collection.insert_many([
    {"name": "机械键盘", "price": 499, "category": "电子设备"},
    {"name": "连衣裙", "price": 299, "category": "服装"}
], ordered=True)  # ordered=True表示按顺序插入，出错则停止

# 2. 查询操作
## 基础查询
cursor = collection.find(
    {"category": "电子设备"},  # 查询条件
    {"name": 1, "price": 1, "_id": 0}  # 投影：返回哪些字段
)

## 带条件查询
cursor = collection.find(
    {"price": {"$gt": 300, "$lt": 1000}},  # 价格300-1000之间
    limit=10,  # 最多返回10条
    sort=[("price", 1)]  # 按价格升序
)

## 查询单条文档
doc = await collection.find_one(
    {"name": "机械键盘"},  # 查询条件
    {"_id": 0}  # 不返回_id
)

# 3. 更新操作
## 更新单条文档
result = await collection.update_one(
    {"name": "笔记本电脑"},  # 更新条件
    {
        "$set": {"price": 6299},  # 设置字段值
        "$inc": {"version": 1}   # 递增字段值
    },
    upsert=False  # 不存在是否插入新文档
)

## 更新多条文档
result = await collection.update_many(
    {"category": "电子设备"},  # 更新条件
    {"$set": {"status": "in_stock"}}  # 更新操作
)

# 4. 删除操作
## 删除单条文档
result = await collection.delete_one(
    {"name": "过时产品"}  # 删除条件
)

## 删除多条文档
result = await collection.delete_many(
    {"price": {"$lt": 100}}  # 删除价格低于100的文档
)

# 5. 其他常用操作
## 计数
count = await collection.count_documents(
    {"category": "服装"}  # 计数条件
)

## 聚合查询
result = await collection.aggregate([
    {"$match": {"category": "电子设备"}},  # 筛选条件
    {"$group": {"_id": "$category", "avg_price": {"$avg": "$price"}}},  # 分组计算
    {"$sort": {"avg_price": -1}}  # 排序
]).to_list(length=None)

```

> motor使用事务

```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient()
session = await client.start_session()
try:
    async with session.start_transaction():
        # 在事务中执行删除
        await collection.delete_many(
            {"status": "inactive"},
            session=session
        )
finally:
    session.end_session()
```



### model 与 schema

​	FastAPI中通常继承Pydantic 中 BaseModel用于类型校验和OpenAPI文档生成，因此我们使用 model作为实际存储模型，使用schema作为请求和响应的校验模型



### api认证

>jwt

​	采用jwt认证方式，并在认证中间件中排除部分路径，将认证中间件挂载至全局路由，解析用户信息并挂载到request.state

> middleware/auth.py

```python
# 认证中间件
class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self,app,exclude=None,exclude_start=None):
        super().__init__(app)
        self.exclude = exclude or []
        self.exclude_start = exclude_start or []

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint, *args,
                       **kwargs) -> Response:

        # 跳过不需要认证的路径，例如登录接口
        # [7:] 跳过 /api/v1
        if request.url.path[7:]  in self.exclude:
            return await call_next(request)

        for start in self.exclude_start:
            if request.url.path[7:].startswith(start):
                return await call_next(request)

        # 获取Authorization头
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"msg":"认证失败"})

        # 提取并验证令牌（实际应用中应替换为真实的令牌验证逻辑）
        token = auth_header.split(" ")[1]
        _ctt = parse_jwt(token)

        if not _ctt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的令牌或令牌已过期",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 将用户信息挂载到request.state
        request.state.jwt_info = _ctt

        # 继续处理请求
        response = await call_next(request)
        return response

```



### 鉴权

> 依赖注入

​	采用依赖注入方式实现鉴权，类似Django 装饰器 @has_permission

```python
# 鉴权依赖项
# 类似Django 装饰器 @has_permission
# 使用方法

# async def some_router(r: Request,p:Depends(permission_required("admin")),*arg,**kwargs) -> dict:
#     ...
#
# async def some_router(r: Request,p:Depends(permission_required(["client","wx_user"])),*arg,**kwargs) -> dict:
#     ...


async def permission_required(permission: list[str] | str):
    if type(permission) is str:
        permission = [permission]

    async def has_permission(r: Request, db: Depends(get_db), u: Depends(get_current_user)) -> bool:
        return True

    return has_permission
```



### 路由挂载

​	在create_app中挂载全部路由,包括静态文件

```python
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from middlewares.auth import AuthMiddleware


def create_app(lifespan=None, prefix: str = "") -> FastAPI:
  app = FastAPI(docs_url=f"{prefix}/docs",
                redoc_url=f"{prefix}/redoc",
                openapi_url=f"{prefix}/openapi.json",
                swagger_ui_oauth2_redirect_url=f"{prefix}/docs/oauth2-redirect",
                lifespan=lifespan)

  main_router = APIRouter(prefix=prefix)

  # 静态文件路由，增加反向代理后可取消此条路由
  app.mount("/api/v1/static", StaticFiles(directory="static"), name="静态文件")

  # 导入视图函数
  from views.http.test import r as test_router
  from views.http.public import r as public_router
  from views.http.base_crud import r as rbac_router
  from views.http.admin import r as admin_router
  # 测试路由
  """
  {prefix}/test/...
  """
  main_router.include_router(test_router)

  # 公开路由
  """
  {prefix}/public/...
  """
  main_router.include_router(public_router)

  # 权限路由
  """
  {prefix}/rbac/...
  """
  main_router.include_router(rbac_router)

  # 管理界面路由
  """
  {prefix}/admin/..."""
  main_router.include_router(admin_router)

  # 注册主路由
  app.include_router(main_router)

  # 添加全局认证中间件
  app.add_middleware(AuthMiddleware,
                     exclude=["/redoc", "/docs", "/openapi.json"],
                     exclude_start=["/public", "/test"])

  return app

```



### rbac设计

> MongoRABC存储模型：基于角色的访问控制（RBAC）优化模型

由于mongo对于外键访问低效，采用以下复合存储模型

```javascript
// 权限集合
{
  _id: ObjectId("5f9d9b3d8c4a1e2b3c8b4570"),
  code: "user:create",
  desc: "Create users",
  tag: "user_management"
}

// 角色集合
{
  _id: ObjectId("5f9d9b3d8c4a1e2b3c8b4568"),
  name: "admin",
  permission_codes: ["user:create", "user:delete", "content:edit"]
}

// 用户集合
{
  _id: ObjectId("5f9d9b3d8c4a1e2b3c8b4567"),
  username: "alice",
  email: "alice@example.com",
  role_codes: ["admin", "editor"],
  // 计算字段（使用聚合管道或应用层计算）
  permissions: ["user:create", "user:delete", "content:edit"]
}
```





### 代码变更自动重启

使用watchdog 实现类似django的自动重启

```python
import signal
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import config
from startup import app


# 服务生命周期管理与代码变更检测
class ServerManager:
    def __init__(self):
        self.process = None

    def start_server(self):
        """启动FastAPI服务"""
        if self.process:
            self._stop_server()

        self.process = subprocess.Popen(
            [
                sys.executable,
                "-m", "uvicorn",
                "main:app",
                "--host", config["server"]["host"],
                "--port", str(config["server"]["port"])
            ],
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        print("服务已启动")

        for route in app.routes:
            if hasattr(route, "methods"):
                print(f"HTTP Route: {route.methods}\t{route.path}")
            elif hasattr(route, "path"):
                print(f"Static/Mount Route: {route.path}")

    def _stop_server(self):
        """停止当前运行的服务"""
        if self.process:
            print("正在停止现有服务...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, server_manager):
        super().__init__()
        self.server_manager = server_manager
        self.last_trigger = 0

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".py"):
            current_time = time.time()
            # 防抖处理：1秒内只触发一次
            if current_time - self.last_trigger < 1.0:
                return

            self.last_trigger = current_time
            print(f"\n检测到文件变更: {event.src_path}")
            self.server_manager.start_server()


def main():
    server = ServerManager()
    handler = ReloadHandler(server)
    observer = Observer()
    observer.schedule(handler, path='.', recursive=True)
    observer.start()

    # 初始启动服务
    server.start_server()

    # 注册信号处理
    def shutdown(signum, frame):
        print("\n正在关闭服务...")
        server._stop_server()
        observer.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == '__main__':
    main()
```



### 国际化

> 使用gettext翻译



> 使用pybabel 生成翻译文件



1. 安装babel

```bash
pip install babel
```

pybabel可能位于 `C:\Users\xxxxx\AppData\Roaming\Python\Python310\Scripts` 下，而不是python安装目录下



2. 使用pybabel 生成模板文件

```bash
.\pybabel.exe extract --input-dirs .\api  -o messages.pot
```

这会扫描该目录下所有文件，可以使用排除参数



3. 生成翻译文件

```bash
 .\pybabel.exe init -i .\messages.pot -d locale -l zh_CN
```

- -d：指定目录
- -D：指定domain  默认为messages
- -l： 指定语言 如 zh_CN en_US  同时确定了生成的文件会位于 `locale/zh_CN/LC_MESSAGES/`目录



4. 生成机器文件

```bash
.\pybabel.exe compile -d locale
```

这将会扫描 locale目录下所有语言翻译并生成对应的机器文件



5. 在代码中使用

执行`extract`命令会扫描文件中函数`_()`而生成msg

以下为 翻译依赖

```python
import gettext
from typing import Callable
from fastapi import Request, HTTPException

from config import config

try:
    lang_cfg = config.get("language")

except Exception as e:
    raise Exception("language config not found")

# 缓存已加载的翻译，避免重复加载
_translations_cache: dict[str, gettext.GNUTranslations] = {}


def load_translations(lang: str):
    """加载指定语言的翻译文件"""
    if lang in _translations_cache:
        return _translations_cache[lang]

    lang = lang_cfg["default"] if lang not in lang_cfg["support"] else lang
    # 尝试加载精确匹配的语言
    try:
        translations = gettext.translation(
            domain=lang_cfg["domain"],
            localedir=lang_cfg["path"],
            languages=[lang],
            fallback=True
        )
        _translations_cache[lang] = translations
        return translations

    except FileNotFoundError:
        pass


def gettext_translator(request: Request) -> Callable:
    """
    依赖项：获取当前请求的翻译函数
    从请求头 Accept-Language 提取第一个语言，返回对应翻译函数
    """
    # 从请求头获取语言偏好，默认使用zh_CN
    accept_language = request.headers.get("Accept-Language", lang_cfg["default"]).strip()

    # 提取第一个语言（忽略后续内容和质量值）
    # 示例："zh-CN,zh;q=0.9,en;q=0.8" → 取"zh-CN"
    first_lang = accept_language.split(',')[0].split(';')[0].strip()

    # 规范化语言代码（如zh-cn -> zh_CN）
    first_lang.replace("-", "_")
    r = first_lang.split("_")
    if len(r)!= 2:
        valid_lang = lang_cfg["default"]
    else:
        valid_lang = f"{r[0].lower()}_{r[1].upper()}"
    translations = load_translations(valid_lang)
    return translations.gettext
```

以下为在路由函数中使用演示

```python
@swiper_router.post("", response_model=BaseCreateRespModel)
async def create_swiper(item: SwiperCreate, _: gettext_translator = Depends(), db: get_db_op = Depends()):
    item = Swiper(**item.model_dump())
    res = await db.insert_one(C.SWIPER, item.mongo_dict())
    if res:
        return {
            "code": 200,
            "id": str(res.inserted_id),
            "msg": _("create success")
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=_("create failed")
        )
```



以下为在中间件中使用演示

```python
```



## api文档





## 知识技术

### [uni-app中的Vue3](https://uniapp.dcloud.net.cn/tutorial/vue3-basics.html)

绑定html class 的语法

![image-20250817165615611](D:\Document\ProgramDev\L000-Python\FastApi\Bux\src-manual\assets\image-20250817165615611.png)



### 使用Pinia全局通信

> 安装pinia

```bash
npm i pinia
```



> 在main.js中挂载pinia

```javascript
```

