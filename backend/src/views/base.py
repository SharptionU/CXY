import re
from typing import Generic, TypeVar, Type
from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies.locale import gettext_translator
from core.dependencies.permission import require_permissions
from core.utils.request import query_params_purify
from models.base import MongoBaseModel
from core.dependencies.database import get_db_op

# 泛型类型变量（用于类型提示）
Model = TypeVar("Model", bound=MongoBaseModel)  # ORM模型类型


class ModelView(Generic[Model]):
    """通用视图集基类，实现CRUD操作"""

    def __init__(
            self,
            model: Type[Model],  # ORM模型
            model_alias: str = "",
            prefix: str = None,  # 路由前缀（如 "/modelName"）
            tags: list[str] = None,  # 接口标签
            perm_dict: dict[str, list] = None,
            use_default_perm_rule=True
    ):
        """
        :param perm_dict: 权限字典

        :param use_default_perm_rule: 是否使用默认权限规则
        """
        self.model = model
        self.model_alias = model_alias or model.__name__
        self.router = APIRouter(prefix=prefix, tags=tags)

        # 存储的表名，将驼峰式转为小写下划线
        self.table = re.sub('([a-z0-9])([A-Z])', r'\1_\2', model.__name__).lower()

        # 路由前缀， 将驼峰式转为小写短横线连接
        self.prefix = prefix or re.sub('([a-z0-9])([A-Z])', r'\1-\2', model.__name__).lower()

        if not perm_dict and use_default_perm_rule:
            perm_dict = {k: [f"{self.table}:{k}"] for k in ("list", "create", "update", "delete")}
        self.perm_dict = perm_dict or {}

        self.router = APIRouter(prefix=f"/{self.prefix}", tags=tags or [self.prefix or self.model.__name__])

        # 注册路由
        self.register()


    # ------------------------------
    # 以下为CRUD路由（可被子类重写）
    # ------------------------------
    def register(self):
        """注册CRUD路由,可重写，添加额外的路由"""
        l_req = self.model.get_list_request_model()
        l_res = self.model.get_list_response_model()
        r_res = self.model.get_detail_response_model()
        u_req = self.model.get_update_request_model()
        u_res = self.model.get_update_response_model()
        c_req = self.model.get_create_request_model()
        c_res = self.model.get_create_response_model()
        d_res = self.model.get_delete_response_model()

        p_l = self.perm_dict.get("list")
        p_u = self.perm_dict.get("update")
        p_c = self.perm_dict.get("create")
        p_d = self.perm_dict.get("delete")

        async def _list(q: l_req, db=Depends(self.get_db)) -> list[l_res]:
            query, skip, limit, sort = query_params_purify(q)
            res = await db.find(self.table, query, skip=skip, limit=limit, sort=sort)
            return res

        async def create(item: c_req|list[c_res],
                         _=Depends(gettext_translator),
                         db=Depends(self.get_db)) :
            if  isinstance(item, list):
                items = [self.model(**i.model_dump()) for i in item]
            else:
                items = [self.model(**item.model_dump())]
            res = await db.insert_many(self.table, [i.mongo_dict() for i in items])
            if res:
                return {
                    "code": status.HTTP_201_CREATED,
                    "msg": _("create success"),
                    "id": str(res.inserted_ids)
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=_("create failed")
                )

        async def retrieve(id: str,
                           _=Depends(gettext_translator),
                           db=Depends(self.get_db)) -> r_res:
            item = await db.find_one(self.table, {"_id": id})
            if not item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_("object not exist"))
            return item

        async def update(id: str,
                         item: u_req,
                         _=Depends(gettext_translator),
                         db=Depends(get_db_op)) -> u_res:
            update_data = item.model_dump(exclude_unset=True)

            if not update_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=_("invalid update data"))
            res = await db.find_one_and_update(self.table, {"_id": id}, {"$set": update_data})

            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=_("object not exist")
                )
            return res

        async def destroy(
                id: str,
                _=Depends(gettext_translator),
                db=Depends(get_db_op)) :
            res = await db.delete_one(self.table, {"_id": id})
            if res.deleted_count == 1:
                return
                # Status code 204 must not have a response body
                # return {
                #     "code": status.HTTP_204_NO_CONTENT,
                #     "msg": _("delete success"),
                #     "deleted_count": res.deleted_count}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=_("delete failed")
                )

        self.router.add_api_route(
            path="",
            endpoint=_list,
            methods=["GET"],
            response_model=list[l_res],
            dependencies=[require_permissions(p_l)],
            summary=f"获取{self.model_alias}列表"
        )
        self.router.add_api_route(
            path="",
            endpoint=create,
            methods=["POST"],
            response_model=c_res|list[c_res],
            status_code=status.HTTP_201_CREATED,
            dependencies=[require_permissions(p_c)],
            summary=f"创建新{self.model_alias}"
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=retrieve,
            methods=["GET"],
            response_model=r_res,
            dependencies=[require_permissions(p_l)],
            summary=f"获取{self.model_alias}详情"
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=update,
            methods=["PUT"],
            response_model=u_res,
            dependencies=[require_permissions(p_u)],
            summary=f"差量更新{self.model_alias}"
        )

        self.router.add_api_route(
            path="/{id}",
            endpoint=destroy,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=[require_permissions(p_d)],
            summary=f"删除{self.model_alias}"
        )

    # ------------------------------
    # 以下为CRUD核心方法（可被子类重写）
    # ------------------------------
    @staticmethod
    def get_db():
        """获取数据库会话（需子类实现或通过依赖注入）"""
        return Depends(get_db_op)
