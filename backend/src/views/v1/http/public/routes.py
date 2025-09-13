from fastapi import APIRouter
from .user import r as user_router
from .category import r as category_router
from .product import r as product_router
from .search import r as search_router
from .nearby import r as nearby_router
from .shop_way import r as shop_way_router
from .swiper import  r as swiper_router
from .widget import r as widget_router

router = APIRouter(prefix="/public", tags=["开放接口"])
router.include_router(user_router)
router.include_router(category_router)
router.include_router(product_router)
router.include_router(search_router)
router.include_router(nearby_router)
router.include_router(shop_way_router)
router.include_router(swiper_router)
router.include_router(widget_router)
