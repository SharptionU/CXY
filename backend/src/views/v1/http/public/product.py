from fastapi import APIRouter, Depends
from core.dependencies.database import get_db_op
from models.mall import Product
from services.product import ProductService

r = APIRouter()


@r.get("/product", response_model=list[Product])
async def get_product_list(store_id=None, category_id=None, db=Depends(get_db_op)):
    return await ProductService.get_product_by_store_and_cate(store_id, category_id, db)
