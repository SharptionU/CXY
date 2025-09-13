from fastapi import APIRouter, Depends,HTTPException,status

from core.database.db import clear_field
from core.dependencies.database import get_db_op
from core.dependencies.permission import get_current_user

r = APIRouter()

@r.get("/profile")
async def get_user_profile(user = Depends(get_current_user), db = Depends(get_db_op)):
    info = await db.find_one("user", {"_id": user["id"]})
    if not info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    return clear_field(info, ["password"])