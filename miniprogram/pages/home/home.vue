<template>
	<view class="main-container">

		<!-- usw 代码块 快速生成 -->
		<swiper :indicator-dots="true" :autoplay="true" :interval="3000" :duration="1000" :circular="true"
			mode="'aspectFit'">
			<swiper-item v-for="(d,i) in swiperList" :key="i">
				<!-- 动态绑定商品id,跳转到商品详情页 -->
				<navigator class="swiper-item" :url="'/subpkg/goods_detail/goods_detail?good_id='+d.goods_id">
					<image :src="d.image_url"></image>
				</navigator>
			</swiper-item>
		</swiper>

		<!-- 用户信息展示 -->
		<view class="membership-container">
			<view class="user-container">
				<user-info :user="userInfo"></user-info>
			</view>
			<view class="membership-introduce">
				<view class="membership-introduce-local">购物：会员九八折，最高可享八八折</view>
			</view>
		</view>


		<view class="fruit-shopping-container">
			<view v-for="(sway,sindex) in shopWay" :key="sindex" class="fruit-shopping-item">
				<image :src="sway.image_url"></image>
				<view v-if="typeof sway.alias ==='string' && sway.alias.length>0" class="fruit-shopping-title">
					{{sway.alias}}
				</view>
			</view>
		</view>

		<view class="fruit-shopping-widget-container">
			<view v-for="(w,wi) in shopWidget" :key="wi" class="fruit-shopping-widget">
				<image :src="w.image_url"></image>
				<view class="fruit-shopping-widget-name">{{w.alias}}</view>
				<view class="fruit-shopping-widget-desc">{{w.description}}</view>
			</view>
		</view>

		<view class="pos-container">
			<view class="pos-content">
				<view class='pos-text'>{{nearbyInfo.name}}</view>
				<view class="pos-image-container">
					<image :src="nearbyInfo.image_url"></image>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import {
		userStore
	} from '../../stores/user';

	export default {
		data() {
			return {

				//页面数据
				swiperList: [],
				userInfo: {
					username: "",
					avatar: "",
					id: ""
				},
				userStore: null,
				shopWay: [],
				shopWidget: [],
				nearbyInfo: {}
			};
		},

		async onLoad() {
			this.getSwiperList()
			this.getShopWay()
			this.getShopWidget()
			this.getNearbyInfo()
			// this.getUserInfo()
			// 处理头像为空的情况
			if (!this.userInfo.avatar || this.userInfo.avatar === '') {
				this.userInfo.avatar = await this.getDefaultAvatar()
				this.userInfo.avatar = this.$utils.getAbspath(this.userInfo.avatar)
			}
		},

		methods: {
			initUserInfo() {
				this.userStore = userStore()
				this.userStore.init()
			},

			async getSwiperList() {
				const {
					data,
					statusCode
				} = await uni.$http.get("/public/swiper")
				if (statusCode !== 200) {
					return uni.$msg("数据加载失败！")
				} else {
					// 处理图片路径
					this.swiperList = data.map(item => ({
						...item,
						image_url: this.$utils.getAbspath(item.image_url) // 调用路径处理方法
					}));
					uni.$msg("数据请求成功！")
				}

			},
			async getUserInfo() {
				const {
					data,
					statusCode
				} = await uni.$http.get("/protect/profile")
				if (statusCode !== 200) {
					return uni.$msg("数据加载失败！")
				} else {
					this.userInfo = data
				}

			},

			async getDefaultAvatar() {
				const {
					data,
					statusCode
				} = await uni.$http.get("/public/default-avatar")
				if (statusCode !== 200) {
					return ""
				} else {
					return data.url
				}
			},

			async getShopWay() {
				const {
					data,
					statusCode
				} = await uni.$http.get("/public/fruit-shop-way")
				if (statusCode !== 200) {
					uni.$msg("获取购物分类失败！")
				} else {
					// 处理图片路径
					this.shopWay = data.map(item => ({
						...item,
						image_url: this.$utils.getAbspath(item.image_url) // 调用路径处理方法
					}));
				}
			},

			async getShopWidget() {
				const {
					data,
					statusCode
				} = await uni.$http.get("/public/shop-widget")
				if (statusCode !== 200) {
					uni.$msg("获取购物小组件失败！")
				} else {
					// 处理图片路径
					this.shopWidget = data.map(item => ({
						...item,
						image_url: this.$utils.getAbspath(item.image_url) // 调用路径处理方法
					}));
				}
			},


			async getNearbyInfo() {
				const {
					data,
					statusCode
				} = await uni.$http.get("/public/nearby-info")
				if (statusCode !== 200) {
					uni.$msg("获取购物小组件失败！")
				} else {
					data.image_url = this.$utils.getAbspath(data.image_url)
					this.nearbyInfo = data
				}
			}


		}
	}
</script>

<style lang="scss">
	.main-container {
		// background: linear-gradient(90deg, rgba(180, 230, 180, 1) 0%, rgba(230, 255, 230, 0) 100%);
		// background-color: linear-gradient(135deg, #d4fc79, #96e6a1);
		background: #f0fff0;
		position: relative;
	}

	swiper {
		height: 600rpx;
		z-index: 1;

		.swiper-item,
		image {
			width: 100%;
			height: 100%;
		}
	}

	.nav-list {
		display: flex;
		justify-content: space-around;
		margin: 30rpx 0;

		.nav-img {
			width: 128rpx;
			height: 128rpx;
			border-radius: 5px;
		}
	}

	.membership-container {
		position: absolute;
		top: 500rpx;
		left: 0;
		width: calc(100% - 40rpx);
		height: 250rpx;
		border-radius: 25rpx;
		margin: 0 20rpx;
		// padding: 20rpx;
		background-color: #fff;
		z-index: 10;
		// box-shadow: 5rpx 5rpx 50rpx 5rpx gray;
	}

	.user-container {
		background-color: #ffffff;
		/* 背景色，确保内容可见 */
		border-radius: 10rpx;
		margin: 5rpx;

		height: 150rpx;
		// box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
		/* 添加阴影提升层次感 */
	}

	.membership-introduce {
		background-color: $theme-green;
		// 为啥多出来3rpx?
		height: 93rpx;
		overflow: hidden;
		border-radius: 0 0 25rpx 25rpx;
	}

	.membership-introduce-local {
		margin: 10rpx;
		text-align: center;
	}

	.fruit-shopping-container {
		display: flex;
		justify-content: space-between;
		border-radius: 25rpx 25rpx 0 0;
		background-color: #fff;
		height: 300rpx;
		margin: 180rpx 20rpx 0 20rpx;

	}

	.fruit-shopping-item {
		padding: 30rpx 70rpx 10rpx 70rpx;

		image {
			height: 200rpx;
			width: 200rpx;
			border-radius: 15rpx;
		}

		view {
			padding: 0 40rpx;
			text-align: center;
			font-weight: bold;
			// font-family: SimSun;
		}
	}

	.fruit-shopping-widget-container {
		border-radius: 0 0 25rpx 25rpx;
		background-color: #fff;
		margin: 3rpx 20rpx 0 20rpx;
		display: flex;
		justify-content: space-around;
		height: 200rpx;
	}

	.fruit-shopping-widget {
		display: flex;
		flex-direction: column;
		// border: 2rpx solid black;
		justify-content: space-around;
		margin: 10rpx;

		image {
			display: block;
			margin: auto;
			max-width: 100%;
			width: 100rpx;
			height: 100rpx;

		}

		.fruit-shopping-widget-name {
			font-size: 25rpx;
			color: #000;
			text-align: center;
		}

		.fruit-shopping-widget-desc {
			font-size: 23rpx;
			color: #1a1a1a;
			text-align: center;
		}


	}

	.pos-container {
		margin: 10rpx 20rpx;
		border-radius: 25rpx 25rpx 0 0;
		background-color: #ffffff;
		display: flex;
		/* 添加这一行，启用Flexbox布局 */
		justify-content: center;
		height: 200rpx;
	}

	.pos-content {
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: space-between;

		image {
			height: 100rpx;
			width: 200rpx;
		}

		view {
			margin-top: 15rpx;
			text-align: center;
		}
	}
</style>