from datetime import datetime, timezone

import argon2

from models.base import MongoBaseModel
from schemas.constant import COLLECTION as C
from core.auth.password import password_hasher


class User(MongoBaseModel):
    # web用户, str | None 兼容微信用户
    username: str | None
    password: str | None
    alias: str | None = ""

    # 微信用户
    token: str | None = None
    token_expires: datetime | None = datetime.now(timezone.utc)
    is_active: bool | None = True

    # 共有字段
    # is_login: bool | None = False # 单处登录
    is_anonymous: bool | None = False
    login_at: datetime | None = datetime.now(timezone.utc)
    is_super: bool | None = False
    avatar: str | None = None

    # admin接口允许返回用户的角色和权限信息:权限信息在登录时计算
    permissions: list[str] | None = None

    roles: list[str] | None = None

    class Config(MongoBaseModel.Config):
        custom_schema_extra_children = {
            "list_request": {
                "exclude": ["password"]
            }
        }

    def _hash_password(self):
        """对密码进行加盐哈希处理"""
        self.password = password_hasher.hash(self.password)

    def _verify_password(self, password):
        """验证密码是否匹配哈希值"""
        try:
            return password_hasher.verify(password, self.password)  # hash and password
        except (argon2.exceptions.VerifyMismatchError,
                argon2.exceptions.InvalidHashError):
            return False

    async def web_auth(self, db):
        query = {"username": self.username}
        user = await db.find_one(C.USER, query)
        if user and self._verify_password(user["password"]):
            return user
        return None

    async def register(self, db):
        query = {"username": self.username}
        user = await db.find_one(C.USER, query)
        if user:
            return None
        hashed_password = password_hasher.hash(self.password)
        store_user = User(username=self.username, password=hashed_password)
        res = await db.insert_one(C.USER, store_user.mongo_dict())
        return await db.find_one(C.USER, {"_id": res.inserted_id})


class Role(MongoBaseModel):
    name: str
    description: str | None = None
    permissions: list[str] | None = None
    is_active: bool | None = True

    async def add_permission(self, db, permissions: list[str] | str):
        if isinstance(permissions, str):
            permissions = [permissions]
        if self.permissions:
            self.permissions = list(set(self.permissions + permissions))

        else:
            self.permissions = permissions
        res = await db.update_one(C.ROLE, {"_id": self.id}, self.mongo_dict())

        ...


class Permission(MongoBaseModel):
    name: str
    description: str | None = None
