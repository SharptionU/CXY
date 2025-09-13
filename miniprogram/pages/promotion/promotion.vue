<template>
  <view class="container">
    <!-- 左侧分类列表 -->
    <scroll-view 
      class="left-scroll" 
      scroll-y 
      :scroll-with-animation="false"
    >
      <view 
        v-for="(category, index) in categories" 
        :key="category.id"
        class="category-item"
        :class="{ active: currentCategoryIndex === index }"
        @click="handleCategoryClick(index)"
      >
        {{ category.name }}
      </view>
    </scroll-view>
    
    <!-- 右侧内容区域 -->
    <scroll-view 
      class="right-scroll" 
      scroll-y 
      @scroll="handleRightScroll"
      :scroll-with-animation="false"
      ref="rightScroll"
    >
      <view class="content-wrapper">
        <view 
          v-for="(category, index) in categories" 
          :key="category.id"
          :id="`category-${index}`"
          class="category-content"
        >
          <view class="content-title">{{ category.name }}</view>
          <view class="content-items">
            <view 
              class="content-item" 
              v-for="(item, i) in category.items" 
              :key="i"
            >
              <image :src="item.imgUrl" mode="widthFix" class="item-img"></image>
              <view class="item-name">{{ item.name }}</view>
              <view class="item-price">¥{{ item.price.toFixed(2) }}</view>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 当前选中的分类索引
      currentCategoryIndex: 0,
      // 分类数据
      categories: [
        {
          id: 1,
          name: "推荐",
          items: Array.from({ length: 15 }, (_, i) => ({
            imgUrl: "https://picsum.photos/200/200?random=" + i,
            name: "推荐商品 " + (i + 1),
            price: 10 + Math.random() * 90
          }))
        },
        {
          id: 2,
          name: "数码",
          items: Array.from({ length: 10 }, (_, i) => ({
            imgUrl: "https://picsum.photos/200/200?random=" + (i + 20),
            name: "数码产品 " + (i + 1),
            price: 100 + Math.random() * 900
          }))
        },
        {
          id: 3,
          name: "服装",
          items: Array.from({ length: 20 }, (_, i) => ({
            imgUrl: "https://picsum.photos/200/200?random=" + (i + 40),
            name: "服装商品 " + (i + 1),
            price: 50 + Math.random() * 300
          }))
        },
        {
          id: 4,
          name: "食品",
          items: Array.from({ length: 12 }, (_, i) => ({
            imgUrl: "https://picsum.photos/200/200?random=" + (i + 70),
            name: "食品商品 " + (i + 1),
            price: 10 + Math.random() * 50
          }))
        },
        {
          id: 5,
          name: "家居",
          items: Array.from({ length: 18 }, (_, i) => ({
            imgUrl: "https://picsum.photos/200/200?random=" + (i + 90),
            name: "家居商品 " + (i + 1),
            price: 80 + Math.random() * 500
          }))
        },
        {
          id: 6,
          name: "美妆",
          items: Array.from({ length: 14 }, (_, i) => ({
            imgUrl: "https://picsum.photos/200/200?random=" + (i + 120),
            name: "美妆商品 " + (i + 1),
            price: 60 + Math.random() * 400
          }))
        }
      ],
      // 记录每个分类的顶部位置
      categoryPositions: []
    };
  },
  onLoad() {
    // 页面加载完成后获取各分类位置信息
    this.$nextTick(() => {
      this.calculateCategoryPositions();
    });
  },
  methods: {
    // 计算每个分类的顶部位置
    calculateCategoryPositions() {
      this.categoryPositions = [];
      this.categories.forEach((_, index) => {
        const query = uni.createSelectorQuery().in(this);
        query
          .select(`#category-${index}`)
          .boundingClientRect(data => {
            if (data) {
              this.categoryPositions[index] = data.top;
            }
          })
          .exec();
      });
    },
    
    // 左侧分类点击事件
    handleCategoryClick(index) {
      this.currentCategoryIndex = index;
      // 滚动到右侧对应分类
      const query = uni.createSelectorQuery().in(this);
      query
        .select(`#category-${index}`)
        .boundingClientRect(data => {
          if (data) {
            // 滚动到对应位置（减去导航栏高度，这里假设导航栏高度为0）
            this.$refs.rightScroll.scrollTo({
              scrollTop: data.top,
              duration: 300
            });
          }
        })
        .exec();
    },
    
    // 右侧滚动事件
    handleRightScroll(e) {
      const scrollTop = e.detail.scrollTop;
      // 找到当前滚动位置所在的分类
      for (let i = this.categories.length - 1; i >= 0; i--) {
        // 检查当前滚动位置是否超过了第i个分类的顶部
        if (
          this.categoryPositions[i] !== undefined &&
          scrollTop >= this.categoryPositions[i] - 10
        ) {
          if (this.currentCategoryIndex !== i) {
            this.currentCategoryIndex = i;
            // 左侧滚动到当前选中项
            this.scrollLeftToCurrent();
          }
          break;
        }
      }
    },
    
    // 左侧滚动到当前选中的分类
    scrollLeftToCurrent() {
      const query = uni.createSelectorQuery().in(this);
      query
        .selectAll('.category-item')
        .boundingClientRect(data => {
          if (data && data[this.currentCategoryIndex]) {
            const itemTop = data[this.currentCategoryIndex].top;
            const itemHeight = data[this.currentCategoryIndex].height;
            const leftScrollHeight = 500; // 左侧scroll-view高度，可根据实际情况调整
            
            // 计算需要滚动的距离，使当前项居中显示
            const scrollTop = itemTop - leftScrollHeight / 2 + itemHeight / 2;
            this.$refs.leftScroll.scrollTo({
              scrollTop,
              duration: 300
            });
          }
        })
        .exec();
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100vh;
  background-color: #f5f5f5;
}

/* 左侧分类样式 */
.left-scroll {
  width: 200rpx;
  height: 100%;
  background-color: #ffffff;
  border-right: 1px solid #eee;
}

.category-item {
  height: 100rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30rpx;
  color: #333;
  position: relative;
}

.category-item.active {
  color: #ff4d4f;
  background-color: #fff5f5;
  font-weight: bold;
}

.category-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 6rpx;
  height: 100rpx;
  background-color: #ff4d4f;
}

/* 右侧内容样式 */
.right-scroll {
  flex: 1;
  height: 100%;
}

.content-wrapper {
  padding: 20rpx;
}

.category-content {
  margin-bottom: 40rpx;
}

.content-title {
  font-size: 36rpx;
  font-weight: bold;
  margin: 20rpx 0;
  color: #333;
}

.content-items {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.content-item {
  width: 240rpx;
  background-color: #fff;
  border-radius: 10rpx;
  padding: 15rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.item-img {
  width: 100%;
  height: 200rpx;
  border-radius: 8rpx;
}

.item-name {
  font-size: 26rpx;
  margin: 10rpx 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-price {
  font-size: 28rpx;
  color: #ff4d4f;
  font-weight: bold;
}
</style>
