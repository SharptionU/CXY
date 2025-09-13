from fastapi import Request
from fastapi.params import Depends

from core.database.db import object_id_serializable
from core.utils.decorators import timer

def get_db(r: Request):
    return r.app.state.mongo_db


class DatabaseOperation:
    def __init__(self, db):
        self.db = db

    # 封装crud操作
    @timer(print_args=True)
    async def find_one(self, col, query=None, ret=None, **kwargs) -> dict:
        item = await self.db[col].find_one(query, ret, **kwargs)
        return object_id_serializable(item) or {}

    async def find(self, col, query=None, ret=None, sort=None, skip=0, limit=10, **kwargs) -> list[dict]:
        cursor = self.db[col].find(query, ret, **kwargs)
        if sort:
            item = await cursor.sort(*sort).skip(skip).limit(limit).to_list()
        else:
            item = await cursor.skip(skip).limit(limit).to_list()
        return [object_id_serializable(i) for i in item] if item else []

    async def insert_one(self, col, data, **kwargs):
        return await self.db[col].insert_one(data, **kwargs)

    async def insert_many(self, col, data, **kwargs):
        return await self.db[col].insert_many(data, **kwargs)

    async def delete_one(self, col, query, **kwargs):
        return await self.db[col].delete_one(query, **kwargs)

    async def delete_many(self, col, query, **kwargs):
        return await self.db[col].delete_many(query, **kwargs)

    async def update_one(self, col, query, update, **kwargs):
        item = await self.db[col].update_one(query, update, **kwargs)
        return object_id_serializable(item)

    async def update_many(self, col, query, update, **kwargs):
        items = await self.db[col].update_many(query, update, **kwargs)
        return [object_id_serializable(item) for item in items]

    async def find_one_and_update(self, col: str, query: dict, update: dict, ret: dict[str:int] = None,
                                  ret_type: bool = True, **kwargs):
        """
        :param col:
        :param query:
        :param update: 需要更新的数据
        :param ret: 控制字段是否返回，0为不返回，1为返回
        :param ret_type: 原参数名为，控制返回内容是修改前还是修改后 ReturnDocument.AFTER = True
        """
        item = await self.db[col].find_one_and_update(query, update, projection=ret, return_document=ret_type, **kwargs)
        return object_id_serializable(item)


async def get_db_op(db=Depends(get_db)):
    return DatabaseOperation(db)
