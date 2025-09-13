
from fastapi import APIRouter, Depends
from core.dependencies.database import get_db_op
from core.constants import COLLECTION as C
from models.mall import ShopWidget
r= APIRouter()

@r.get("/shop-widget", response_model=list[ShopWidget])
async def get_shop_widget(db=Depends(get_db_op)):
    return await db.find(C.SHOP_WIDGET, query={"is_active": True}, sort=("order", 1))

