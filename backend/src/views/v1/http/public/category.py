from fastapi import APIRouter, Depends

from core.dependencies.database import get_db_op
from services.category import CateService
r = APIRouter()


@r.get("/product-category")#,response_model=StoreCategory
async def get_category(store_id,db=Depends(get_db_op)):
    cate_list= await CateService.get_cate_info_by_store_id(store_id,db)
    return cate_list
