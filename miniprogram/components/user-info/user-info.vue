<template>
	<view class="user-info-container">

		<view class="user-avatar-container">
			<image :src="user.avatar"></image>
		</view>

		<view class="inner-membership-container">
			<view class="membership-info-up">
				<view class="user-name">
					{{user.username || user.name || '匿名用户'}}
				</view>
				<membership-tag :level="1"></membership-tag>
			</view>
			<view class="membership-info-down">
				<view class="membership-level">
					<progress :percent="membershipLevelProgress" :activeColor="activeColor" :active="true"
						:backgroundColor="'#f0fff0'" stroke-width="8" :border-radius="5"></progress>
					<text class="progress-text">{{membershipLevelProgress}}%</text>
				</view>
			</view>
		</view>

		<view class="point-container">
			<text class="point-label">积分</text>
			<text class="point-value">0</text>
		</view>
		<view class="coupon-container">
			<text class="coupon-label">优惠券</text>
			<text class="coupon-value">0</text>
		</view>

	</view>
</template>

<script>
	// 脚本部分保持不变
	export default {
		name: "user-info",
		mounted() {
			console.log("user-info组件：", this.user)
		},
		props: {
			user: {
				type: Object,
				default: () => {
					return {
						id: "",
						avatar: "",
						name: "",
						phone: "",
						alias: "",
					}
				}
			},
			activeColor: {
				type: String,
				default: "#fd9191"
			}
		},
		data() {
			return {
				membershipLevelProgress: 70,
			};
		},
		methods: {
			computMembershipLevelProgress() {
				// 计算会员等级进度
			}
		}
	}
</script>

<style lang="scss">
	// 确保组件不超过父类高度
	.user-info-container {
		display: flex;
		height: 100%;
		align-items: stretch; // 使所有子项高度相同
		padding: 10rpx;
		box-sizing: border-box;
		justify-content: space-around;
	}

	// 头像容器
	.user-avatar-container {
		width: 15%;
		display: flex;
		justify-content: center;
		align-items: center;
		box-sizing: border-box;

		image {
			width: 100rpx;
			height: 100rpx;
			border-radius: 50%;
			border: 2rpx solid #eee;
		}
	}

	// 会员信息容器
	.inner-membership-container {
		width: 50%;
		display: flex;
		height: 100%;
		flex-direction: column;
		justify-content: space-around;
		margin: 10rpx 30rpx 30rpx 10rpx;
		box-sizing: border-box;
	}

	.membership-info-up {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.user-name {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		max-width: 60%;
	}

	.membership-info-down {
		width: 100%;
	}

	.membership-level {
		// position: relative;
		display: flex;
		justify-content: space-between;
		width: 100%;
	}

	progress {
		display: flex;
		width: 60%;
		margin-bottom: 20rpx;
	}

	.progress-text {
		display: flex;
		font-size: 20rpx;
		color: green;
		margin-bottom: 20rpx;
	}

	// 积分容器
	.point-container,
	.coupon-container {

		width: 15%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 10rpx;
		box-sizing: border-box;
		background-color: #f9f9f9;
		border-radius: 10rpx;
		margin: 0 5rpx;
	}



	.point-label,
	.coupon-label {
		font-size: 24rpx;
		color: #666;
	}

	.point-value,
	.coupon-value {
		font-size: 32rpx;
		font-weight: bold;
		color: $theme-red;
		margin-top: 5rpx;
	}
</style>