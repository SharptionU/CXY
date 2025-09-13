import uuid
import re

from datetime import datetime
from typing import TypeVar, Type
from bson import ObjectId
from pydantic import BaseModel, Field, AnyUrl, create_model

T = TypeVar('T', bound='BaseModel')


class MongoBaseModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    created_time: datetime = Field(default=datetime.now())
    updated_time: datetime = Field(default=datetime.now())

    class Config:
        validate_by_name = True

        # 以下指定在序列化时将uuid和ObjectId转为str
        json_encoders = {uuid.UUID: str,
                         ObjectId: str}

        # 配置crud schema,不必再单独生成schema
        custom_schema = {}
        merged_schema = None

    @classmethod
    def _get_schema(cls):
        if cls.Config.merged_schema:
            return cls.Config.merged_schema

        def deep_merge(old_dict: dict, new_dict: dict) -> dict:
            """
            深度合并两个字典：
            - 新字典中的键若在旧字典中存在，且值为字典，则递归合并
            - 新字典中的键若为新键或非字典值，则直接覆盖旧字典
            """
            merged = old_dict.copy()
            for key, value in new_dict.items():
                if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                    # 递归合并嵌套字典
                    merged[key] = deep_merge(merged[key], value)
                else:
                    # 非字典值或新键，直接覆盖
                    merged[key] = value
            return merged

        _schema = {
            "list_request": {
                "append": {
                    "skip": (int | None, 0),
                    "limit": (int | None, 10),
                    "sort": (str | None, None),
                },
                "exclude": [],
                "optional": ["__all__"]  # ["fields1",...]
            },
            "list_response": {
                "exclude": ["created_time", "updated_time"],
            },
            "detail_response": {
            },
            "update_request": {
                "exclude": ["id", "created_time", "updated_time", "_id"],
                "optional": ["__all__"],
            },
            "update_response": {
                "exclude": ["created_time", "updated_time"],
            },
            "create_request": {
                "exclude": ["created_time", "id", "updated_time", "_id"],
            },
            "create_response": {
                "model": {
                    "code": (int, ...),
                    "msg": (str, ...),
                    "id": (str | None, ...),
                }
            },
            "delete_response": {
                "model": {
                    "code": (int, ...),
                    "msg": (str, ...),
                    "deleted_count": (int, 0),
                }
            }
        }

        if cls.Config.custom_schema:
            _schema = deep_merge(_schema, cls.Config.custom_schema)
        cls.Config.merged_schema = _schema
        return cls.Config.merged_schema

    # 该类实例直接使用 mongo_dict方法实现将 id字段转为 _id字段，覆写原mongo_id字段
    def mongo_dict(self, **kwargs) -> dict:
        data = self.model_dump(by_alias=True, **kwargs)

        # 对AnyUrl的特殊处理
        # AnyUrl: str  json_encoder 配置对 AnyUrl不生效
        return {k: v if not isinstance(v, AnyUrl) else str(v) for k, v in data.items()}

    def dump_no_none(self):
        data = self.mongo_dict()
        return {k: data[k] for k in data if data[k] is not None}

    @classmethod
    def _gen_model(cls: Type[T], location: str, model: Type[BaseModel] = BaseModel) -> Type[BaseModel]:
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', cls.__name__).lower()
        cfg = cls._get_schema()[location]
        # 直接指定返回模型，而不是继承
        if "model" in cfg.keys():
            fields = cfg["model"]

            _model = create_model(f"{name}_{location}",
                                  **fields,
                                  __base__=model)
            print("ModelView -> Gen Model", _model.__name__, _model.model_fields)

            return _model

        # exclude 优先级最高，先执行append进行添加
        fields = {k: (v.annotation, v.default) for k, v in cls.model_fields.items()}
        for k, v in cfg.get("append", {}).items():
            fields[k] = v

        # 再执行exclude进行排除
        for field_name in cfg.get("exclude", []):
            if field_name in fields:
                del fields[field_name]

        # 根据optional执行可选
        optional_fields = cfg.get("optional", [])

        if len(optional_fields) > 0:
            if optional_fields[0] == "__all__":
                for k in fields:
                    fields[k] = (fields[k][0] | None, Field(default=None))
            else:
                for k in optional_fields:
                    if fields.get(k, None):
                        fields[k] = (fields[k][0] | None, Field(default=None))

        _model = create_model(
            f"{name}_{location}",
            **fields,
            __base__=model
        )
        print("ModelView -> Gen Model", _model.__name__, _model.model_fields)
        return _model

    @classmethod
    def get_list_request_model(cls) -> Type[BaseModel]:
        return cls._gen_model("list_request", cls)

    @classmethod
    def get_list_response_model(cls) -> Type[BaseModel]:
        return cls._gen_model("list_response", cls)

    @classmethod
    def get_detail_response_model(cls) -> Type[BaseModel]:
        return cls._gen_model("detail_response", cls)

    @classmethod
    def get_update_request_model(cls) -> Type[BaseModel]:
        return cls._gen_model("update_request")

    @classmethod
    def get_update_response_model(cls) -> Type[BaseModel]:
        return cls._gen_model("update_response", cls)

    @classmethod
    def get_create_request_model(cls) -> Type[BaseModel]:
        return cls._gen_model("create_request")

    @classmethod
    def get_create_response_model(cls) -> Type[BaseModel]:
        return cls._gen_model("create_response", cls)

    @classmethod
    def get_delete_response_model(cls) -> Type[BaseModel]:
        return cls._gen_model("delete_response")
