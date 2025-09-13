from views.base import ModelView
from models.mall import *

__all__ = ["category_template_router",
           "swiper_router",
           "store_router",
           "product_category_router",
           "fruit_shop_way_router",
           "product_detail_router",
           "product_router",
           "shop_widget_router"]
# 首页轮播图
swiper_router = ModelView(Swiper).router

# 分类模板
category_template_router = ModelView(CategoryTemplate).router

# 店铺下的商品分类
product_category_router = ModelView(ProductCategory).router

# 店铺
store_router = ModelView(Store).router

# 商品
product_router = ModelView(Product).router

# 商品详情
product_detail_router = ModelView(ProductDetail).router

# 首页购物方式
fruit_shop_way_router = ModelView(FruitShopWay).router

# 首页下方小组件
shop_widget_router = ModelView(ShopWidget).router