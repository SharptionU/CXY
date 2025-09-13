<template>
	<view class="main-container" :style="{'height':windowHeight +'px'}">
		<view class="search-container" @click="searchHandler">
			<view class="search-box">
				<uni-icons type="search"></uni-icons>
				<text class="placeholder">搜一搜</text>
			</view>
		</view>
		<view class="shop-way-container">
			<view class="shop-way" :class="{'active': shopWay === 'pick'}" @click="setShopWay('pick')">采摘</view>
			<view class="shop-way" :class="{'active': shopWay === 'express'}" @click="setShopWay('express')">代采</view>
		</view>
		<view class="hr-line"></view>


		<!-- 店家信息和选择 -->
		<view class="store-info-container">
			<!-- 店铺名称 -->
			<!-- tab 与 页面数据交互 使用pinia -->
			<view class="store-name-container">
				<view class="store-favorite" @click="storeFavoriteHandler">
					<uni-icons :type="favorite ? 'star-filled' : 'star'" :color="favorite ? '#fd9191' : ''"
						size="20"></uni-icons>
				</view>
				<view class="store-name">{{storeInfo.name}} > </view>
			</view>
			<!-- 店铺距离 -->
			<view class="store-loc-container">
				<uni-icons type="location"></uni-icons>
				<view class="store-distance">距您直线{{storeInfo.distance}}
				</view>
			</view>

			<!-- 店铺公告 -->
			<view class="store-announce-container">
				<view class="text-container">
					<uni-icons type="sound-filled" color="#fd9191"></uni-icons>
					<scroll-text :scrollText="storeInfo.announce" :color="'#fd9191'" :fontSize="25" :height="30"
						:width="400" :interval="3000"></scroll-text>
				</view>
				<view class="store-announce-more" @click="popupOpen">查看店铺公告 ></view>
			</view>

			<uni-popup ref="sotreInfoPopup" background-color="#fff" border-radius="30rpx 30rpx 0 0">
				<view class="store-pop-info">
					<view style="font-weight: bold;">门店公告</view>
					<view v-for="(sv,sk) in storeInfo.annonce" :key="sk" class="store-announce-popup">{{sv}}</view>
					<!-- 跳转至门店信息页面 -->
					<view class="store-more-detail" @click="storeDetailHandler"> 查看更多门店详细信息 > </view>
				</view>
			</uni-popup>
		</view>

		<!-- 商品信息 -->
		<view class="product-info-confainer">
			<view class="top-cate-container">
				<scroll-view scroll-x="true" show-scrollbar="true">
					<view class="scroll-x-container" :style="{width:topCateWidth}">
						<view v-for="(cv,ci) in topCateList" :key="ci" class="scroll-x-item"
							:style="{width:topCateItemWidth}" @click="topCateHandler(ci)">
							<!-- 如果有rich_text则优先显示 -->
							<rich-text v-if="cv.rich_text && cv.rich_text.length>0" :nodes="cv.rich_text"
								class="top-cate-rich-text">{{cv}}</rich-text>
							<view v-else-if="cv.alias && cv.alias.length>0" class="top-cate-alias">{{cv.alias}}</view>
							<view v-else class="top-cate-name">{{cv.name}}</view>
						</view>
					</view>
				</scroll-view>
			</view>
			<!-- 分类等级一的广告 -->
			<view v-if="topCateList[topCateIndex].image_url" @click="cate1AdvHandler" class="cate-1-adv">
				<!-- :src="cateList[topCateIndex].image_url" -->
				<image src="http://127.0.0.1:8000/api/v1/static/image/swiper-spring.jpeg" mode="aspectFill"></image>
			</view>
			<!-- 商品内容 -->
			<view class="bottom-cate-container">
				<!-- 左侧分类 -->
				<view class="left-cate-container">
<!-- 					<scroll-view class="left-scroll" scroll-y="true" scroll-with-animation="false">
						<view v-for="(cv,ci) in " :key="" class="left-cate-item"
							:class="{active:secondCateIndex===index}" @click="secondCateHandler(index)"></view>
					</scroll-view> -->
				</view>

				<!-- 右侧详情 -->
				<view class="right-cate-container">
					<view class="cate-level-3-i">
					</view>
				</view>

			</view>
		</view>
	</view>
</template>

<script>
	export default {
		components: {},
		mounted(options) {},
		data() {
			return {
				windowHeight: 0, //screenHight减去navigation 和 tarbar
				screeHeigth: 0,
				activeCate: 0,
				topCateList: [],
				topCateIndex: 0,
				topCateWidth: "200%",
				topCateItemWidth: "30%",
				secondCateList: [],
				secondCateIndex: 0,
				storeId: "spring",
				favorite: false,
				storeInfo: {
					id: "",
					name: "常香野 (官方店)",
					announce: [
						"这是1条公告",
						"这是2条公告",
						"这是3条公告"
					],
					distance: 10000.11
				},
				shopWay: "pick",
				product:{1:{
					
				},2:{
					
				}},
				categoryPositions:{
					0:{
						0:0,
						1:10,
					}
				}
			};
		},
		onLoad() {
			this.initWindowsHeight()
			this.getStoreInfo()
			this.getCateInfo()
		},

		methods: {

			setShopWay(way) {
				this.shopWay = way
			},
			searchHandler() {
				uni.navigateTo({
					url: "/subpkg/search/search"
				})
			},

			initWindowsHeight() {
				const winInfo = uni.getWindowInfo()
				this.windowHeight = winInfo.windowHeight
			},

			async getStoreInfo() {
				//...根据用户选择的storeid获取店铺信息
				//计算方便的距离
				this.storeInfo.distance = this.$utils.formatDistance(this.storeInfo.distance)
			},

			async getCateInfo() {
				const {
					data,
					statusCode
				} = await uni.$http.get("/public/product-category?store_id=" + this.storeId)

				if (statusCode !== 200) {
					uni.$msg("getCateList 数据加载失败！")
				} else {
					this.topCateList = data
					this.topCateWidth = `${25*data.length}%`
					this.topCateItemWidth = `${Math.floor(100/data.length)}%`
				}
			},
			
			async getCategoryProducts(){
				// 初始化商品分类数据结构
				const productCategories = [];

				try {
					// 遍历顶级分类
					for (const topCate of this.topCateList) {
						// 创建顶级分类对象
						const topCateObj = {
							id: topCate.id,
							name: topCate.name,
							alias: topCate.alias,
							children: []
						};

						// 检查是否有二级分类
						if (topCate.children && topCate.children.length > 0) {
							// 遍历二级分类
							for (const secondCate of topCate.children) {
								// 调用API获取该分类下的商品
								const { data, statusCode } = await uni.$http.get(
									`/public/product?store_id=${this.storeId}&category_id=${secondCate.id}`
								);

								// 创建二级分类对象
								const secondCateObj = {
									id: secondCate.id,
									name: secondCate.name,
									products: statusCode === 200 ? data : []
								};

								// 添加到顶级分类的children数组
								topCateObj.children.push(secondCateObj);
							}
						}

						// 添加到商品分类数据结构
						productCategories.push(topCateObj);
					}

					// 打印结果或进行其他处理
					console.log('商品分类数据:', productCategories);
					return productCategories;
				} catch (error) {
					console.error('获取商品分类数据失败:', error);
					uni.$msg('获取商品分类数据失败');
					return [];
				}
			},
			secondCateHandler(index) {

			},
			async getUserLocation() {
				this.isLoading = true;
				this.errorMessage = '';
				this.locationData = null;

				try {
					// 1. 检查位置授权状态
					const authStatus = await this.checkLocationAuth();
					if (!authStatus) {
						this.errorMessage = '请授予位置权限后再试';
						this.isLoading = false;
						return;
					}

					// 2. 获取位置信息
					const locationRes = await this.getLocation();
					this.locationData = locationRes;

				} catch (err) {
					this.errorMessage = `获取失败：${err.message || err.errMsg}`;
					console.error('位置获取失败:', err);
				} finally {
					this.isLoading = false;
				}
			},

			// 检查位置授权状态
			checkLocationAuth() {
				return new Promise((resolve) => {
					uni.getSetting({
						success: (res) => {
							// 已授权
							if (res.authSetting['scope.userLocation']) {
								resolve(true);
							} else {
								// 未授权，请求授权
								uni.authorize({
									scope: 'scope.userLocation',
									success: () => resolve(true),
									fail: () => resolve(false)
								});
							}
						},
						fail: () => resolve(false)
					});
				});
			},

			// 获取位置信息
			getLocation() {
				return new Promise((resolve, reject) => {
					uni.getLocation({
						type: 'gcj02', // 坐标系类型：gcj02(国测局坐标)，兼容微信/高德地图
						altitude: true, // 是否获取高度信息
						isHighAccuracy: true, // 开启高精度定位
						highAccuracyExpireTime: 3000, // 高精度定位超时时间
						success: (res) => resolve(res),
						fail: (err) => reject(err)
					});
				});
			},

			popupOpen() {
				this.$refs.sotreInfoPopup.open("bottom")
			},

			storeFavoriteHandler() {
				this.favorite = !this.favorite
				// TODO 后端处理逻辑
			},

			storeDetailHandler() {
				uni.navigateTo({
					url: "/subpkg/store-detail/store-detail?id=" + this.storeInfo.id
				})
			},
			topCateHandler(index) {
				this.topCateIndex = index
				// 切换顶级分类索引和和顶级分类下内容
				this.secondCateList = this.cateList[index].children

				console.log("indexChangeTo", index)
				// 重新渲染底部
			},
			cate1AdvHandler() {
				// 一级分类下广告处理 跳转至商品详情或者红包领取
				let n_url = this.cateList[this.topCateIndex].navigate_url
				// 添加路径非法判断
				if (n_url) {
					uni.navigateTo({
						url: this.cateList[this.topCateIndex].navigate_url
					})
				}
			}
		}

	}
</script>

<style lang="scss">
	.main-container {
		display: flex;
		flex-direction: column;
		background-color: #f0fff0;
		padding-top: 100rpx;
		box-sizing: border-box;
		// background-color: linear-gradient(90deg, rgba(180, 230, 180, 1) 0%, rgba(230, 255, 230, 0) 100%);
	}

	.shop-way-container {
		display: flex;
		padding: 20rpx;
		width: 30%;
		justify-content: space-around;

		.shop-way {
			text-align: center;
			margin: 0 0 0 20rpx;

			&.active {
				font-weight: bold;
				color: green;
			}
		}
	}

	.search-container {
		position: fixed;
		width: 55%;
		left: 250rpx;
		top: 110rpx;
		z-index: 99;

		.search-box {
			border-radius: 20rpx;
			background-color: #ffffff;
			height: 30px;
			border-radius: 10px;
			width: 100%;
			display: flex;
			justify-content: center;
			align-items: center;

			.placeholder {
				font-size: 15px;
				margin-left: 10px;
			}
		}
	}


	.hr-line {
		width: 100%;
		height: 1px;
		background-color: #eee;
		margin: 10rpx 0 0 0;
	}

	.store-info-container {
		background-color: #fff;
		padding: 5rpx 15rpx;

		.store-name-container {
			display: flex;
			padding: 5rpx;
			gap: 15rpx;
			height: 40rpx;

			.store-name {
				font-weight: bold;
				font-size: 30rpx;
			}
		}

		.store-loc-container {
			display: flex;
			gap: 15rpx;
			padding: 5rpx;
			height: 40rpx;

			.store-distance {
				font-size: 25rpx;
				color: lightskyblue;
				padding-left: 5rpx;
			}
		}

		.store-announce-container {
			display: flex;
			justify-content: space-between;
			height: 40rpx;
			padding: 5rpx;

			.text-container {
				display: flex;
			}

			.store-announce-more {
				font-size: 25rpx;
			}
		}

	}

	.store-pop-info {
		padding: 25rpx;
		display: flex;
		flex-direction: column;
		justify-content: space-around;
		gap: 8rpx;

		.store-announce-popup {
			font-size: 25rpx;
		}

		.store-more-detail {
			padding-top: 10rpx;
			font-size: 23rpx;
		}
	}

	.product-info-confainer {
		display: flex;
		flex-direction: column;
		flex: 1;

		.top-cate-container {
			padding: 20rpx;
			height: 40rpx;
			background-color: #fff;

			scroll-view {
				width: 100%;
			}
		}

		.top-cate-alias {
			text-align: center;
			font-size: 28rpx;
		}

		.top-cate-name {
			text-align: center;
			font-size: 28rpx;
		}

		.scroll-x-container {
			display: flex;
			justify-content: space-between
		}

		.bottom-cate-container {
			flex: 1;
		}

		.cate-1-adv {
			height: 150rpx;
			overflow: hidden;
			padding: 10rpx 15rpx;

			image {
				width: 100%;
				height: 100%;
				border-radius: 20rpx;
			}
		}

		.left-cate-container {
			height: 100%;
			background-color: #eee;
			border-top-right-radius: 20rpx;
			width: 25%;
		}
	}
</style>