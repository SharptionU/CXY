<template>
  <view class="item-container" :style="{ width: width + 'rpx', height: height + 'rpx' }" @click="onClick">
    <view class="item-image-container">
      <image :src="image_url || '/static/image/default.png'" mode="aspectFill" class="item-image"></image>
      <view class="item-stock" v-if="stock <= 0">缺货</view>
    </view>
    <view class="item-info">
      <text class="item-name">{{ name }}</text>
      <text class="item-price">¥{{ price }}</text>
      <view class="item-meta">
        <text class="item-sold">销量: {{ sold_count }}</text>
        <text class="item-stock-count" v-if="stock > 0">库存: {{ stock }}</text>
      </view>
      <text class="item-description">{{ description }}</text>
    </view>
  </view>
</template>

<script>
  export default {
    name: "product-item",
    props: {
      name: {
        type: String,
        default: ""
      },
      description: {
        type: String,
        default: ""
      },
      price: {
        type: Number,
        default: 0.0
      },
      sold_count: {
        type: Number,
        default: 0
      },
      stock: {
        type: Number,
        default: 0
      },
      width: {
        type: Number,
        default: 400
      },
      height: {
        type: Number,
        default: 500
      },
      image_url: {
        type: String,
        default: ''
      }
    },
    data() {
      return {

      }
    },
    methods: {
      onClick() {
        // 跳转到详情页
        uni.navigateTo({
          url: `/subpkg//product-detail?id=${this.id || this._id}&name=${encodeURIComponent(this.name)}`
        })
      }
    }
  }
</script>

<style lang="scss">
  .item-container {
    background-color: #fff;
    border-radius: 10rpx;
    overflow: hidden;
    box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
  }

  .item-image-container {
    width: 100%;
    height: 240rpx;
    position: relative;
    overflow: hidden;
  }

  .item-image {
    width: 100%;
    height: 100%;
  }

  .item-stock {
    position: absolute;
    top: 10rpx;
    right: 10rpx;
    background-color: rgba(230, 67, 64, 0.8);
    color: #fff;
    font-size: 24rpx;
    padding: 5rpx 10rpx;
    border-radius: 5rpx;
  }

  .item-info {
    padding: 15rpx;
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .item-name {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 10rpx;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .item-price {
    font-size: 32rpx;
    color: #e64340;
    margin-bottom: 10rpx;
  }

  .item-meta {
    display: flex;
    justify-content: space-between;
    font-size: 24rpx;
    color: #999;
    margin-bottom: 10rpx;
  }

  .item-description {
    font-size: 24rpx;
    color: #666;
    flex: 1;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>