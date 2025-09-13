from fastapi import APIRouter, Depends, HTTPException,status

from core.auth.jwt import gen_jwt
from core.database.db import object_id_serializable
from schemas.rbac import *
from models.rbac import  *
from core.dependencies.locale import gettext_translator
from core.dependencies.database import get_db_op



r = APIRouter(tags=["用户"])

@r.post("/login", response_model=WebLoginResUser)
async def login(user: WebLoginReqUser, _=Depends(gettext_translator), db=Depends(get_db_op)):
    user = User(**user.model_dump())
    auth_user = await user.web_auth(db)

    if not auth_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"msg": _("authentication failed")})

    # 生成jwt
    auth_user = object_id_serializable(auth_user)
    jwt = gen_jwt({
        "username": auth_user["username"],
        "id": auth_user["id"],
    })
    auth_user["jwt_token"] = jwt
    return WebLoginResUser(**auth_user)


# 微信登录接口处理函数
@r.post("/wx-login", response_model=WebLoginResUser)
async def wx_login(user: WXLoginReqUser, db=Depends(get_db_op)):
    ...



@r.post("/register", response_model=WebRegisterResUser)
async def register(user: WebRegisterReqUser, _=Depends(gettext_translator), db=Depends(get_db_op)) -> dict:
    _user = User(**user.model_dump())

    new_user = await _user.register(db)
    if new_user:
        new_user.update({"message": _("register success")})
        return object_id_serializable(new_user)

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": _("user already exist")})

@r.get("/default-avatar")
def get_default_avatar():
    return {
        "url": "/static/avatar/__default__.png",
    }