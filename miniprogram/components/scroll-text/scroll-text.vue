<template>
	<swiper class="scroll-container" :vertical="vertical" :circular="circular" :autoplay="autoplay" :interval="interval"
		:duration="duration" :indicator-dots="false" :style="{width: width + 'rpx', height: height + 'rpx'}">
		<swiper-item v-for="(item, index) in scrollText" :key="index">
			<view class="scroll-item"
				:style="{width: width + 'rpx', height: height + 'rpx', fontSize: fontSize + 'rpx', color: color}">
				{{ item }}</view>
		</swiper-item>
	</swiper>
</template>
<script>
	export default {
		name: "scroll-text",
		props: {
			scrollText: {
				type: Array,
				default: []
			},
			color: {
				type: String,
				default: "#000000"
			},
			fontSize: {
				type: Number,
				default: 30 //rpx
			},
			width: {
				type: Number,
				default: 750 //rpx (默认全屏宽度)
			},
			height: {
				type: Number,
				default: 80 //rpx (更合理的默认高度)
			},
			vertical: {
				type: Boolean,
				default: true
			},
			circular: {
				type: Boolean,
				default: true
			},
			autoplay: {
				type: Boolean,
				default: true
			},
			interval: {
				type: Number,
				default: 3000 //ms
			},
			duration: {
				type: Number,
				default: 500 //ms
			}
		},
		data() {
			return {

			};
		},
		mounted() {
			// 确保滚动文本数组不为空
			if (!this.scrollText || this.scrollText.length === 0) {
				console.warn('scrollText数组不能为空');
			}
		}
	}
</script>
<style scoped>
	.scroll-item {
		height: 100%;
		padding: 0 20rpx;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		display: flex;
		align-items: center;
	}
</style>