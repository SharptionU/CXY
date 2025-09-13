from fastapi import APIRouter

from .model_view import *
router = APIRouter(prefix="/protect", tags=["api"])
router.include_router(swiper_router)
router.include_router(product_category_router)
router.include_router(product_router)
router.include_router(product_detail_router)
router.include_router(store_router)
router.include_router(fruit_shop_way_router)
router.include_router(shop_widget_router)