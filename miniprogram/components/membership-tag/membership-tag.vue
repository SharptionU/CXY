<template>
	<view class="membership-tag-container">
		<!-- 使用传入的levelRichText -->
		<rich-text v-if="levelRichText.length>0" :nodes="levelRichText[level-1]"></rich-text>

		<!-- 如果没有富文本内容，则使用本地样式渲染 -->
		<view v-else :class="['membership-tag-local', 'level-' + level]">
			{{ levelName[level-1] }}
		</view>

	</view>
</template>

<script>
	export default {
		name: "membership-tag",
		props: {
			// 会员等级名称（直接传入字符串）
			levelName: {
				type: Array,
				default: ['果园初遇', '果树萌芽', '繁花满枝', '硕果盈枝', '丰收满园'],
			},
			// 会员等级富文本内容
			levelRichText: {
				type: Array,
				default: []
			},
			// 会员等级（直接传入）
			level: {
				type: Number,
				required: true,
				default: 0,
				validator: value => {
					return value >= 1 && value <= 5 && Number.isInteger(value);
				}
			}
		}
	}
</script>

<style lang="scss">
	
	/* 样式部分保持不变 */
	.membership-tag-container {
		display: inline-block;
		padding: 4rpx 12rpx;
		border-radius: 16rpx;
		font-size: 24rpx;
		font-weight: 500;
	}

	/* 等级1样式 - 最低等级 */
	.level-1 {
		background-color: #f0fff0;
		color: lightpink;
		border: 1rpx solid #e0e0e0;
	}

	/* 等级2样式 */
	.level-2 {
		background-color: #e8f5e9;
		color: #4caf50;
		border: 1rpx solid #c8e6c9;
	}

	/* 等级3样式 */
	.level-3 {
		background-color: #e3f2fd;
		color: #2196f3;
		border: 1rpx solid #bbdefb;
	}

	/* 等级4样式 */
	.level-4 {
		background-color: #f3e5f5;
		color: #9c27b0;
		border: 1rpx solid #e1bee7;
	}

	/* 补充等级5样式 */
	.level-5 {
		background-color: #fff3e0;
		color: #ff9800;
		border: 1rpx solid #ffe0b2;
		box-shadow: 0 2rpx 8rpx rgba(255, 152, 0, 0.2);
	}

	.membership-tag-local {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 4rpx 16rpx;
		border-radius: 20rpx;
		font-size: 24rpx;
		font-weight: 500;
	}
</style>