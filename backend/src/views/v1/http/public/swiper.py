from fastapi import APIRouter, Depends

from models.mall import  Swiper
from core.dependencies.database import get_db_op
from core.constants import COLLECTION as C

r =  APIRouter()

@r.get("/swiper", response_model=list[Swiper])  # 使用装饰器注册GET路由，路径为"/swiper"，返回类型为Swiper模型列表
async def get_swiper_list(db=Depends(get_db_op)):  # 定义异步函数，依赖注入数据库连接对象
    """
    小程序端获取active轮播图（无分页）  # 函数功能描述：获取小程序端激活状态的轮播图数据，不进行分页处理
    """
    query = {"is_active": True}  # 查询条件，筛选is_active字段为True的文档
    return await db.find(C.SWIPER, query)  # 异步查询数据库，返回符合条件的轮播图数据

