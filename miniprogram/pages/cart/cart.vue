<template>
  <view class="container">
    <view class="scroll-container">
      <view class="scroll-wrapper" :style="{ transform: `translateY(-${currentIndex * itemHeight}px)` }">
        <!-- 滚动的文字列表 -->
        <view class="scroll-item" v-for="(item, index) in textList" :key="index">
          {{ item }}
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 滚动的文字内容列表
      textList: [
        "最新公告：系统将于今晚23点进行维护",
        "优惠活动：全场商品满100减30",
        "重要通知：请及时更新您的个人信息",
        "新品上市：夏季新款已正式发售"
      ],
      currentIndex: 0, // 当前显示的索引
      itemHeight: 60, // 每个文字项的高度（rpx）
      timer: null // 定时器
    };
  },
  onLoad() {
    this.startScroll();
  },
  onUnload() {
    // 页面卸载时清除定时器
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  methods: {
    // 开始滚动动画
    startScroll() {
      // 每隔2秒切换一次内容
      this.timer = setInterval(() => {
        // 计算下一个索引，循环显示
        this.currentIndex = (this.currentIndex + 1) % this.textList.length;
      }, 2000);
    }
  }
};
</script>

<style scoped>
.container {
  padding: 30rpx;
}

/* 滚动容器：限制只显示一行 */
.scroll-container {
  width: 100%;
  height: 60rpx; /* 与itemHeight保持一致 */
  overflow: hidden; /* 隐藏超出容器的内容 */
  position: relative;
  border: 1px solid #eee;
  border-radius: 8rpx;
  padding: 0 20rpx;
}

/* 滚动包裹层：通过transform实现向上滚动 */
.scroll-wrapper {
  width: 100%;
  transition: transform 0.5s ease; /* 滚动动画过渡效果 */
}

/* 每个文字项：高度与容器一致 */
.scroll-item {
  height: 60rpx; /* 与容器高度保持一致 */
  line-height: 60rpx; /* 垂直居中 */
  white-space: nowrap; /* 防止文字换行 */
  overflow: hidden; /* 超出部分隐藏 */
  text-overflow: ellipsis; /* 文字溢出显示省略号 */
  font-size: 28rpx;
}
</style>
    