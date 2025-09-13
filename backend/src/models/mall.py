from enum import Enum

from pydantic import Field
from datetime import datetime
from .base import MongoBaseModel, BaseModel
from core.utils.mall import generate_order_id

__all__ = ["Swiper",
           "CategoryTemplate",
           "ProductCategory",
           "Store",
           "Product",
           "ProductDetail",
           "FruitShopWay",
           "ShopWidget"]


class Swiper(MongoBaseModel):
    """轮播图条目模型"""

    name: str
    description: str | None = None
    image_url: str  # 图片链接
    product_id: str | None = ""
    is_active: bool | None = True

    class Config(MongoBaseModel.Config):
        schema_extra_children = {}


class Address(BaseModel):
    """地址模型"""

    longitude: float | None = None  # 经度
    latitude: float | None = None  # 纬度
    postal_code: str | None = None  # 邮编

    country: str | None = "中华人民共和国"  # 国家
    province: str | None = None  # 省份
    city: str | None = None  # 城市
    town: str | None = None  # 区县
    street: str | None = None  # 街道
    detail_address: str | None = None  # 详细地址


class CategoryTemplate(MongoBaseModel):
    """平台定义的分类模板，支持1-2级分类"""
    name: str = Field(..., min_length=1, max_length=50)
    alias: str | None = Field(None, max_length=50)
    description: str | None = Field(None, max_length=200)
    rich_text: str | None = None  # 存放原生HTML
    image_url: str | None = None  # 分类广告图
    level: int = Field(1, ge=1, le=2)  # 仅允许1-2级
    order: int = Field(1, ge=0)  # 排序值
    parent: str | None = None  # 父分类ID
    children: list[str] = []  # 子分类ID列表
    is_active: bool = True  # 是否启用


class ProductCategory(MongoBaseModel):
    """分类模型"""
    store_id: str
    name: str = Field(..., min_length=1, max_length=50)
    alias: str | None = Field(None, max_length=50)
    description: str | None = Field(None, max_length=200)
    rich_text: str | None = None  # 存放原生HTML
    image_url: str | None = None  # 分类广告图

    # 可跳转至产品详情页或者优惠券/红包领取页
    navigate_url: str | None = None  # 广告上的链接

    level: int = Field(1, ge=1, le=2)  # 仅允许1-2级
    order: int = Field(1, ge=0)  # 排序值
    parent: str | None = None  # 父分类ID
    children: list[str] = []  # 子分类ID列表
    is_active: bool = True  # 是否启用

    class Config(MongoBaseModel.Config):
        schema_extra_children = {
        }


class Store(MongoBaseModel):
    """店铺模型"""

    name: str  # 店铺名称
    alias: str | None = Field(None, max_length=50)
    description: str | None = None  # 店铺描述
    announce: list[str] | None = []  # 店铺公告
    owner_id: str  # 店铺所有者ID
    is_active: bool | None = True  # 店铺是否激活
    address: Address | None = None  # 店铺地址
    contact_phone: str | None = None  # 联系电话
    rating: float | None = None  # 店铺综合评分


class ProductTag(MongoBaseModel):

    """
    产品标签模型类，用于存储产品标签相关信息
    继承自MongoBaseModel，用于MongoDB数据库操作
    """
    name: str | None = None  # 标签名称，可选字符串类型
    detail: str | None = None  # 标签详细信息，可选字符串类型
    alias: str | None = None  # 标签别名，可选字符串类型
    color: str | None = "black"  # 标签文字颜色，默认为黑色
    bg_color: str | None = "#f0fff0"  # 标签背景颜色，默认为浅绿色
    border_radius: int | None = 5  # rpx


class ProductAttribute(BaseModel):
    name: str
    alias: str | None = None
    values: list[str]


class Product(MongoBaseModel):
    """产品模型"""

    name: str
    alias: str | None = None
    description: str | None = None
    store_id: str | None = None
    category_id: str | None = None
    order:int | None = 0 # 排序

    # 显示之前的价格
    price_before: float | None = None
    price: float
    stock: int | None = 0
    sold_count: int | None = 0
    sold_out:bool|None=False # 是否售罄

    # 缩略图
    image_url: str | None = None
    is_active: bool|None = True

class Contact(MongoBaseModel):
    """联系人模型"""

    name: str  # 联系人姓名
    phone: str  # 联系人手机号
    address: Address | None = None  # 地址


class ProductDetail(MongoBaseModel):
    product_id: str
    swiper_urls: list[str] | None = None  # 详情页轮播图
    video_url: str | None = None  # 首页视频

    # 商品详情和说明的文字 如 "os":"Android 10.0"
    description_attributions: dict | None = {}

    # 存储tag id,以防在创建商品时直接创建新的tag
    tags: list[ProductTag] | None = []

    # 购物时可选的属性
    attributes: list[ProductAttribute] | None = None

    # 发货地址 虚拟商品无发货地址
    shipping_address: Address | None

    # 发货期限，单位为小时
    shipping_deadline: int | None = None

    # 商品详情和说明的图片
    detail_urls: list[str] | None = None


class Combo(MongoBaseModel):
    """套餐模型"""

    name: str  # 套餐名称
    description: str | None = None  # 套餐描述
    product_id: str  # 产品id

    # 即在计算时会减去多少库存
    product_count: int  # 产品数量

    # 原价 可以是product单价*数量
    price_before: float | None = None

    price: float  # 套餐价格
    is_active: bool | None = True  # 套餐是否可用
    start_time: datetime | None = None  # 套餐开始时间
    end_time: datetime | None = None  # 套餐结束时间
    enable_attributes: list[str] | None = None  # 可选属性


class ShippingAddress(MongoBaseModel):
    """收获地址模型"""

    # 在用户侧使用
    user_id: str
    contact: Contact
    is_default: bool | None = False  # 是否为常用地址


class OrderStatus(str, Enum):
    """订单状态"""

    pending = "pending"  # 待支付
    paid = "paid"  # 已支付
    refunded = "refunded"  # 已退款
    cancelled = "cancelled"  # 已取消
    completed = "completed"  # 已完成


class Order(MongoBaseModel):
    """订单模型"""

    # 订单号
    order_id: str
    user_id: str  # 用户ID
    product_id: str  # 产品ID
    combo_id: str | None = None  # 套餐ID

    # 这里是套餐的数量 发布套餐时默认创建一个单个商品的套餐
    combo_quantity: int

    total_price: float  # 总价
    actual_payment: float | None = None  # 实际付款金额

    status: OrderStatus = OrderStatus.pending  # 订单状态

    pay_at: datetime | None = None  # 支付时间
    refund_at: datetime | None = None  # 退款时间
    cancel_at: datetime | None = None  # 取消时间

    recipient_info: Contact | None = None  # 收货人信息

    remark: str | None = None  # 备注

    payment_method: str = "wechat"  # 支付方式
    payment_number: str
    order_number: str | None = None  # 订单号

    refund_number: str | None = None  # 退款号
    cancel_number: str | None = None  # 取消号

    refund_money: float | None = None  # 退款金额
    cancel_money: float | None = None  # 取消金额

    refund_remark: str | None = None  # 退款备注
    cancel_remark: str | None = None  # 取消备注

    refund_time: datetime | None = None  # 退款时间
    cancel_time: datetime | None = None  # 取消时间

    @staticmethod
    def get_pay_id(payment_method: str) -> str:
        return generate_order_id(payment_method)

    @staticmethod
    def get_refund_id(payment_method: str) -> str:
        return generate_order_id("refund")

    @staticmethod
    def get_cancel_id(payment_method: str) -> str:
        return generate_order_id("cancel")


class ShoppingCart(MongoBaseModel):
    """购物车模型"""

    user_id: str  # 用户ID
    product_id: str  # 产品ID
    quantity: int  # 数量
    selected: bool | None = (
        True  # 表示该购物车中的商品是否被选中，默认为选中状态，可用于结算等操作时筛选商品
    )


class MessageContent(BaseModel):
    text: str
    images: list[str] | None = None
    tags: list[str] | None = None


class Comment(MongoBaseModel):
    """评论模型"""

    user_id: str  # 用户ID
    product_id: str  # 产品ID
    parent_id: str | None = None  # 父评论ID，用于回复时引用
    content: MessageContent  # 评论内容
    rating: int = Field(default=5, gt=0, lt=6)  # 评分，例如1 - 5星
    reply_count: int | None = 0  # 回复次数


class UserMembership(MongoBaseModel):
    """用户会员模型"""

    user_id: str  # 用户ID
    level: int | None = 0  # 会员等级，默认为0级
    total_points: int | None = 0  # 总积分，据此计算会员等级
    points: int | None = 0  # 当前积分，消费后将会小于总积分


class CouponType(str, Enum):
    """优惠券类型"""

    DISCOUNT = "discount"  # 折扣券
    FIXED = "fixed"  # 固定金额券
    FREE_SHIPPING = "free_shipping"  # 免运费券
    COMBO = "combo"  # 组合券


class Coupon(MongoBaseModel):
    """店家或者平台发布的优惠券模型"""

    name: str  # 优惠券名称
    description: str | None = None  # 优惠券描述
    type: CouponType  # 优惠券类型
    value: float  # 优惠券值(折扣率或固定金额)

    # =0代表无门槛券
    min_order_amount: float | None = 0  # 最低订单金额

    max_discount: float | None = None  # 最大折扣金额

    start_time: datetime  # 开始时间
    end_time: datetime  # 结束时间

    is_active: bool | None = True  # 是否激活

    usage_limit: int | None = None  # 总使用次数限制
    usage_per_user: int | None = 1  # 每人使用次数限制

    applicable_products: list[str] | None = None  # 适用商品
    applicable_categories: list[str] | None = None  # 适用分类

    applicable_store: list[str] | None = None  # 适用店铺

    # @validator('end_time')
    # def end_time_must_be_after_start_time(cls, v, values):
    #     if 'start_time' in values and v <= values['start_time']:
    #         raise ValueError('结束时间必须晚于开始时间')
    #     return v
    #
    # @validator('value')
    # def validate_value_based_on_type(cls, v, values):
    #     if 'type' in values:
    #         if values['type'] == CouponType.DISCOUNT and (v <= 0 or v >= 1):
    #             raise ValueError('折扣率必须在0-1之间')
    #         elif values['type'] == CouponType.FIXED and v <= 0:
    #             raise ValueError('固定金额必须大于0')
    #     return v


class UserCoupon(MongoBaseModel):
    """用户优惠券模型"""

    user_id: str  # 用户ID
    coupon_id: str  # 优惠券ID
    is_used: bool | None = False  # 是否已使用
    used_time: datetime | None = None  # 使用时间
    order_id: str | None = None  # 关联订单ID
    obtained_time: datetime | None = datetime.now()  # 获取时间
    expire_time: datetime | None = None  # 到期日期


class FruitShopWay(MongoBaseModel):
    name: str
    alias: str | None = None

    # 用户显示时排序
    order: int | None = 0
    is_active: bool | None = False

    image_url: str | None = None
    rich_text: str | None = None
    # 单位为rpx
    image_height: int | None = 300
    image_width: int | None = 300

    # 点击后跳转的页面
    page_url: str | None = None


class ShopWidget(MongoBaseModel):
    name: str  # 名称  不用于显示
    alias: str | None = None  # 别名 用于显示
    description: str | None = None  # 显示二级说明

    order: int | None = 0
    is_active: bool | None = False
    is_tab: bool | None = False  # 用于跳转tab还是跳转页面
    image_url: str | None = None
    rich_text: str | None = None

    image_height: int | None = 100
    image_width: int | None = 100

    # 点击后跳转的页面
    page_url: str | None = None
