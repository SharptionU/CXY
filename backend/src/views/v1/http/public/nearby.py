from fastapi import APIRouter, Depends

from core.dependencies.database import get_db_op

r = APIRouter()


@r.get("/nearby-info", response_model=dict)
async def get_nearby(lon: float = 0.0, lan: float = 0.0, db=Depends(get_db_op)):
    return {
        "name": "附近园子",
        "image_url": "/static/image/nearby-info-default.png",
        "store_id": ""
    }
