<template>
	<view class="main-container">
		<!-- search 页面 -->
		<view class="search-container">
			<uni-search-bar @confirm="confirm" :radius="10" :focus="true" :placeholder="placeHolder" ref="searchBar" @input="handleInput"></uni-search-bar>
		</view>

		<!-- 搜索历史和热搜推荐 -->
		<view v-if="showSearchSuggestions" class="search-suggestions-container">
			<!-- 搜索历史 -->
			<view v-if="searchHistory.length > 0" class="section-container">
				<view class="section-title">
					<text>搜索历史</text>
					<view class="clear-history" @tap="clearSearchHistory">清除历史</view>
				</view>
				<view class="tag-container">
					<view v-for="(item, index) in searchHistory" :key="index" class="tag-item" @tap="searchByHistory(item)">
						<text>{{ item }}</text>
						<view class="delete-icon" @tap.stop="deleteHistoryItem(index)">×</view>
					</view>
				</view>
			</view>

			<!-- 热搜推荐 -->
			<view class="section-container">
				<view class="section-title">
					<text>热搜推荐</text>
				</view>
				<view class="tag-container">
					<view v-for="(hint, index) in searchHint" :key="index" class="tag-item" @tap="searchByHint(hint)">
						<text>{{ hint }}</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 搜索结果 -->
		<view v-if="showSearchResult" class="search-result-container">
			<view class="result-header">
				<view class="result-title">搜索结果</view>
				<!-- 使用自定义排序组件 -->
				<sort-picker :fields="sortFields" :defaultSortField="''" :defaultSortOrder="'desc'" @sortChange="handleSortChange"></sort-picker>
			</view>

			<!-- 商品卡片列表 -->
			<view v-if="searchResult.length > 0" class="goods-grid">
				<view v-for="(item, index) in searchResult" :key="index" class="goods-card" :style="{marginBottom: index % 2 === 0 ? '20rpx' : '40rpx'}">
					<view class="goods-image-container">
						<image :src="item.image_url || '/static/image/default.png'" mode="aspectFill" class="goods-image"></image>
					</view>
					<view class="goods-info">
						<text class="goods-name">{{ item.name }}</text>
						<text class="goods-price">¥{{ item.price }}</text>
						<view class="goods-meta">
							<text class="goods-sold">销量: {{ item.sold_count }}</text>
							<text class="goods-stock">库存: {{ item.stock }}</text>
						</view>
						<text class="goods-description">{{ item.description }}</text>
					</view>
				</view>
			</view>
			
			<view v-else class="no-result">
				<image src="/static/image/not-found.png"></image>
				<view>暂无相关商品，换个关键词再试一次吧~</view>
			</view>
		</view>
	</view>
</template>

<script>
	// 引入排序组件

	export default {
		data() {
			return {
				searchHint: [],
				placeHolder: "搜一搜",
				showSearchHint: true, // 控制热搜提示显示
				showSearchResult: false, // 控制搜索结果显示
				showSearchSuggestions: true, // 控制搜索建议(历史+热搜)显示
				searchResult: [], // 搜索结果数据
				searchKeyword: '', // 当前搜索关键词
				searchHistory: [], // 搜索历史
				// 排序字段配置
				sortFields: [
					{ name: '综合', value: '', bidirectional: false },
					{ name: '销量', value: 'sold_count', bidirectional: false },
					{ name: '价格', value: 'price', bidirectional: true }
				],
				sort: 'sold_count', // 当前排序字段
			};
		},
		onLoad() {
			this.getSearchHint();
			this.loadSearchHistory();
		},
		methods: {
			confirm(e) {
				this.searchKeyword = e.value;
				this.saveSearchHistory();
				this.performSearch();
			},
			// 处理输入框变化
			handleInput(e) {
				this.searchKeyword = e.value;
				// 当输入框为空时显示搜索建议，有内容时隐藏
				this.showSearchSuggestions = !this.searchKeyword;
				this.showSearchResult = false;
			},
			// 点击热搜提示项进行搜索
			searchByHint(keyword) {
				this.searchKeyword = keyword;
				this.saveSearchHistory();
				// 设置搜索框的值
				this.$nextTick(() => {
					const searchBar = this.$refs.searchBar;
					if (searchBar && searchBar.setValue) {
						searchBar.setValue(keyword);
					}
				});
				this.performSearch();
			},
			// 点击历史记录项进行搜索
			searchByHistory(keyword) {
				this.searchKeyword = keyword;
				// 设置搜索框的值
				this.$nextTick(() => {
					const searchBar = this.$refs.searchBar;
					if (searchBar && searchBar.setValue) {
						searchBar.setValue(keyword);
					}
				});
				this.performSearch();
			},
			// 保存搜索历史
			saveSearchHistory() {
				if (!this.searchKeyword) return;
				// 避免重复添加
				if (this.searchHistory.includes(this.searchKeyword)) {
					// 移到最前面
					this.searchHistory = this.searchHistory.filter(item => item !== this.searchKeyword);
				}
				// 限制历史记录数量
				if (this.searchHistory.length >= 10) {
					this.searchHistory.pop();
				}
				// 添加到开头
				this.searchHistory.unshift(this.searchKeyword);
				// 保存到本地存储
				uni.setStorageSync('searchHistory', this.searchHistory);
			},
			// 加载搜索历史
			loadSearchHistory() {
				const history = uni.getStorageSync('searchHistory');
				if (history) {
					this.searchHistory = history;
				}
			},
			// 清除所有搜索历史
			clearSearchHistory() {
				uni.showModal({
					title: '提示',
					content: '确定清除所有搜索历史？',
					success: (res) => {
						if (res.confirm) {
							this.searchHistory = [];
							uni.removeStorageSync('searchHistory');
						}
					}
				});
			},
			// 删除单个历史记录项
			deleteHistoryItem(index) {
				this.searchHistory.splice(index, 1);
				uni.setStorageSync('searchHistory', this.searchHistory);
			},
			// 处理排序变更
			handleSortChange(sortInfo) {
				console.log('排序变更:', sortInfo);
				this.sort = sortInfo;
				this.performSearch();
			},
			// 执行搜索
			async performSearch() {
				// 隐藏搜索建议，显示搜索结果
				this.showSearchSuggestions = false;
				this.showSearchResult = true;

				// 显示加载提示
				uni.showLoading({
					title: '搜索中...'
				});

				try {
					// 构建搜索参数，包含关键词和排序方式
					let searchParams = `keyword=${this.searchKeyword}`;
					searchParams += `&sort=${this.sort}`;

					// 发送搜索请求
					console.log('搜索参数:', searchParams);

					const { data, statusCode } = await uni.$http.get(`/public/search?${searchParams}`);

					uni.hideLoading();

					if (statusCode === 200) {
						this.searchResult = data || [];
					} else {
						this.searchResult = [];
						uni.$msg('搜索失败，请重试');
					}
			
				} catch (error) {
					uni.hideLoading();
					this.searchResult = [];
					uni.$msg('网络错误，请检查网络后重试');
				};
				
			},
			async getSearchHint() {
				const { data, statusCode } = await uni.$http.get("/public/search-hints");
				if (statusCode === 200 && data.length > 0) {
					this.placeHolder = data[0];
					this.searchHint = data;
				}
			}
		}
	}
</script>

<style lang="scss">
	/* 原有样式保持不变 */
	.main-container {
		padding: 0 20rpx;
	}

	.search-container {
		position: sticky;
		top: 0;
		z-index: 999;
		background-color: #fff;
	}

	// 搜索建议容器样式
	.search-suggestions-container {
		margin-top: 20rpx;
		background-color: #fff;
		border-radius: 10rpx;
		padding: 20rpx;
		box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);

		.section-container {
			margin-bottom: 20rpx;

			.section-title {
				display: flex;
				justify-content: space-between;
				align-items: center;
				font-size: 28rpx;
				color: #999;
				margin-bottom: 15rpx;

				.clear-history {
					font-size: 24rpx;
					color: #666;
				}
			}

			.tag-container {
				display: flex;
				flex-wrap: wrap;
				gap: 15rpx;

				.tag-item {
					display: flex;
					align-items: center;
					background-color: #f5f5f5;
					padding: 10rpx 20rpx;
					border-radius: 10rpx;
					font-size: 28rpx;
					color: #333;
					position: relative;

					.delete-icon {
						margin-left: 10rpx;
						color: #999;
						font-size: 24rpx;
					}

					&:active {
						background-color: #e9e9e9;
					}
				}
			}
		}
	}

	// 搜索结果样式
	.search-result-container {
		// 原有样式保持不变
		margin-top: 20rpx;
		padding: 20rpx;

		.result-header {
			display: flex;
			flex-wrap: wrap;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 15rpx;
		}

		.result-title {
			font-size: 28rpx;
			color: #999;
			margin-bottom: 10rpx;
		}

		// 商品网格布局
		.goods-grid {
			display: grid;
			grid-template-columns: repeat(2, 1fr);
			grid-gap: 20rpx;
		}

		// 商品卡片样式
		.goods-card {
			background-color: #fff;
			border-radius: 10rpx;
			overflow: hidden;
			box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
			display: flex;
			flex-direction: column;
		}

		.goods-image-container {
			width: 100%;
			height: 300rpx;
			overflow: hidden;
		}

		.goods-image {
			width: 100%;
			height: 100%;
		}

		.goods-info {
			padding: 15rpx;
			flex: 1;
			display: flex;
			flex-direction: column;
		}

		.goods-name {
			font-size: 28rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 10rpx;
			display: -webkit-box;
			-webkit-line-clamp: 2;
			-webkit-box-orient: vertical;
			overflow: hidden;
		}

		.goods-price {
			font-size: 32rpx;
			color: #e64340;
			margin-bottom: 10rpx;
		}

		.goods-meta {
			display: flex;
			justify-content: space-between;
			font-size: 24rpx;
			color: #999;
			margin-bottom: 10rpx;
		}

		.goods-description {
			font-size: 24rpx;
			color: #666;
			flex: 1;
			display: -webkit-box;
			-webkit-line-clamp: 2;
			-webkit-box-orient: vertical;
			overflow: hidden;
		}

		.no-result {
			text-align: center;
			padding: 60rpx 0;
			color: #999;
			font-size: 28rpx;
		}
	}
</style>