from fastapi import APIRouter,status

from views.v1.http.public.routes import router as public_router
from views.v1.http.protect.routes import router as protect_router

router = APIRouter(
    tags=["API v1 总览"],  # OpenAPI 文档中分组标签
    responses={
        # 全局响应模板：所有子路由可复用
        status.HTTP_404_NOT_FOUND: {
            "description": "资源不存在",
            "content": {"application/json": {"example": {"detail": "请求的资源未找到"}}}
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "服务器内部错误",
            "content": {"application/json": {"example": {"detail": "服务器处理请求时发生错误"}}}
        }
    }
)

router.include_router(public_router)
router.include_router(protect_router)
