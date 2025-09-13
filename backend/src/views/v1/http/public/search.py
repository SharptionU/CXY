from fastapi import APIRouter, Depends

from core.dependencies.locale import gettext_translator
from core.dependencies.request import get_sort
from core.dependencies.database import get_db_op
from models.mall import Product
from core.constants import COLLECTION as C

r = APIRouter()


@r.get("/search-hints")
async def get_hints(db=Depends(get_db_op), _=Depends(gettext_translator)):
    """热门商品推荐"""
    # 添加缓存，避免平凡对数据库排序
    # 根据商品销量排序前十并截取名称

    return ["key1", "key2", "key4", "key5", "key6"]


@r.get("/search", response_model=list[Product])
async def search(keyword=None, sort=Depends(get_sort), _=Depends(gettext_translator), db=Depends(get_db_op)):
    """查询商品列表"""

    if not keyword:
        # 如果没有关键词，返回空列表
        query = {}
    else:
        # 构建查询条件：name、alias、description字段包含keyword（忽略大小写）
        query = {
            "$or": [
                {"name": {"$regex": keyword, "$options": "i"}},
                {"alias": {"$regex": keyword, "$options": "i"}},
                {"description": {"$regex": keyword, "$options": "i"}}
            ]
        }

    # 执行查询
    products = await db.find(C.PRODUCT, query, sort=sort)
    return products
