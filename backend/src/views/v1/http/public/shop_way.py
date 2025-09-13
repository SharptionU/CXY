from fastapi import APIRouter, Depends
from models.mall import FruitShopWay
from core.dependencies.database import get_db_op
from core.constants import COLLECTION as C

r = APIRouter()


@r.get("/fruit-shop-way", response_model=list[FruitShopWay])
async def get_fruit_shopway_list(db=Depends(get_db_op)):
    return await db.find(C.FRUIT_SHOP_WAY, query={"is_active": True}, sort=("order", 1))
