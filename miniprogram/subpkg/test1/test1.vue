<template>
	<view class="main-container" :style="{'height':windowHeight +'px'}">
		<view class="search-container">
			<cust-search :radius="20" :url="'/subpkg/search/search'"></cust-search>
		</view>
		<view class="shop-way-container">
			<view class="shop-way">采摘</view>
			<view class="shop-way">代采</view>
		</view>
		<view class="hr-line"></view>


		<!-- 店家信息和选择 -->
		<view class="store-info-container">
			<!-- 店铺名称 -->
			<view class="store-name-container">

			</view>
			<!-- 店铺距离 -->
			<view class="store-loc-container">

			</view>
			<!-- 店铺公告 -->
			<view class="store-announce-container">
				<view class="store-announce">这是一个公告</view>

				<view class="store-announce-more" @click="popupOpen">查看更多 ></view>
				<van-popup v-model:show="fPopup" position="bottom" @close="popupClose">
					<view class="store-pop-info">
						<view style="font-weight: bold;">门店公告</view>
						<view v-for="{sv,sk} in storeInfo.annonce" :key="sk">{{sv}}</view>
						<view class="store-more-detail" @click="storeDetailHandler"> 查看更多门店详细信息 > </view>
					</view>
				</van-popup>
			</view>
		</view>

		<view class="product-info-confainer">
			<view class="cate-level-1">
				<!-- v-for -->
				<view class="cate-level-1-i"></view>
			</view>
			<view class="cate-level-23">
				<view class="cate-level-2">
					<view class="cate-level-2-i">
						<!-- TODO -->
					</view>
				</view>
				<view class="cate-level-3">
					<view class="cate-level-3-i">
						<!-- TODO -->
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		components: {},
		mounted(options) {
			// tab页面不能传入参数
			console.log("页面参数: ", options)
		},
		data() {
			return {
				windowHeight: 0, //screenHight减去navigation 和 tarbar
				screeHeigth: 0,
				activeCate: 0,
				topCateList: [],
				topCateIndex: 0,
				secondCateList: [],
				secondCateIndex: [],
				fPopup: false,
				storeId: "",
				storeInfo: {
					name: "这是一家店",
					annonce: [
						"这是一段公告",
						"这是另一段公告"
					],
					detail_url: ""
				},
				shopWay: "pick"
			};
		},
		onLoad() {
			this.initWindowsHeight()
		},

		methods: {
			initWindowsHeight() {
				const sysInfo = uni.getSystemInfoSync()
				this.windowHeight = sysInfo.windowHeight
			},
			async getTopCateList() {
				const {
					data,
					stausCode
				} = await uni.$http.get("/public/category?level=1")
				if (stausCode !== 200) {
					uni.$msg("数据加载失败！")
				} else {
					this.cateList = data
					console.log(data)
				}
			},

			// async getUserLocation() {
			// 	this.isLoading = true;
			// 	this.errorMessage = '';
			// 	this.locationData = null;

			// 	try {
			// 		// 1. 检查位置授权状态
			// 		const authStatus = await this.checkLocationAuth();
			// 		if (!authStatus) {
			// 			this.errorMessage = '请授予位置权限后再试';
			// 			this.isLoading = false;
			// 			return;
			// 		}

			// 		// 2. 获取位置信息
			// 		const locationRes = await this.getLocation();
			// 		this.locationData = locationRes;

			// 	} catch (err) {
			// 		this.errorMessage = `获取失败：${err.message || err.errMsg}`;
			// 		console.error('位置获取失败:', err);
			// 	} finally {
			// 		this.isLoading = false;
			// 	}
			// },

			// // 检查位置授权状态
			// checkLocationAuth() {
			// 	return new Promise((resolve) => {
			// 		uni.getSetting({
			// 			success: (res) => {
			// 				// 已授权
			// 				if (res.authSetting['scope.userLocation']) {
			// 					resolve(true);
			// 				} else {
			// 					// 未授权，请求授权
			// 					uni.authorize({
			// 						scope: 'scope.userLocation',
			// 						success: () => resolve(true),
			// 						fail: () => resolve(false)
			// 					});
			// 				}
			// 			},
			// 			fail: () => resolve(false)
			// 		});
			// 	});
			// },

			// // 获取位置信息
			// getLocation() {
			// 	return new Promise((resolve, reject) => {
			// 		uni.getLocation({
			// 			type: 'gcj02', // 坐标系类型：gcj02(国测局坐标)，兼容微信/高德地图
			// 			altitude: true, // 是否获取高度信息
			// 			isHighAccuracy: true, // 开启高精度定位
			// 			highAccuracyExpireTime: 3000, // 高精度定位超时时间
			// 			success: (res) => resolve(res),
			// 			fail: (err) => reject(err)
			// 		});
			// 	});
			// },


			popupOpen() {
				this.fPopup = true
			},
			popupClose() {
				this.fPopup = false
			}

		}

	}
</script>

<style lang="scss">
	.main-container {
		background-color: #f0fff0;
		padding-top: 100rpx;
		box-sizing: border-box;
		// background-color: linear-gradient(90deg, rgba(180, 230, 180, 1) 0%, rgba(230, 255, 230, 0) 100%);
	}

	.search-container {
		position: fixed;
		width: 55%;
		left: 250rpx;
		top: 100rpx;
		z-index: 999
	}

	.shop-way-container {
		display: flex;
		width: 30%;
		justify-content: space-around;
		margin: 0 20rpx;
		margin-top: 40rpx;
	}

	.hr-line {
		width: 100%;
		height: 1px;
		background-color: #eee;
		margin: 10rpx 0;
	}

	.cate-container {
		display: flex;
	}

	.cate-inner-left .cate-inner-right {
		height: 100%;
	}

	.cate-inner-left {
		width: 120px;
	}


	.cate-left-item {
		position: relative; // 为伪元素定位提供基准
		background-color: #f7f7f7;
		line-height: 40px;
		text-align: center;
		font-size: 16px;
		color: #666;
		transition: all 0.3s ease; // 添加过渡效果

		// 激活状态样式
		&.cate-active {
			background-color: #fff; // 激活背景色变化
			color: #e74c3c; // 激活文字颜色
			font-weight: bold;

			// 左侧竖条强调效果
			&::before {
				content: "";
				position: absolute;
				left: 0;
				top: 10%; // 上下留空隙
				height: 80%; // 高度控制
				width: 4px; // 竖条宽度
				background-color: #e74c3c; // 竖条颜色
				border-radius: 0 3px 3px 0; // 右侧圆角
			}
		}

	}
</style>