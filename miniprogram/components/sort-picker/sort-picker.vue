<template>
	<view class="sort-picker">
		<view class="sort-item" v-for="(field, index) in fields" :key="index" @tap="handleSortClick(index)">
			<text class="sort-text"
				:class="{'active-text': sort === field.value || sort === '-' + field.value}">{{ field.name }}</text>
			<view class="sort-icons" v-if="field.bidirectional === true">
				<view class="sort-icon up" :class="{ 'active': sort === field.value }"></view><!-- ▲ -->
				<view class="sort-icon down" :class="{ 'active': sort === '-' + field.value }"></view><!-- ▼ -->
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'sort-picker',
		props: {
			fields: {
				type: Array,
				required: true,
				default: () => []
			},
			defaultSortField: {
				type: String,
				default: ''
			},
			defaultSortOrder: {
				type: String,
				default: 'desc'
			}
		},
		data() {
			return {
				sort: this.defaultSortOrder === "asc" ? this.defaultSortField : "-" + this.defaultSortField
			}
		},
		methods: {
			handleSortClick(index) {
				const field = this.fields[index]

				if (field.bidirectional === false) {
					// 不可双向排序，始终使用正序
					this.sort = field.value
				} else {
					// 如果点击的是当前排序字段（无论正序还是倒序）
					if (this.sort === field.value || this.sort === '-' + field.value) {
						// 切换排序顺序
						this.sort = this.sort === field.value ? '-' + field.value : field.value
					} else {
						// 否则，设置为新的排序字段，默认正序
						this.sort = field.value
					}
				}

				// 触发排序事件，将排序信息传递给父组件
				this.$emit('sortChange', this.sort)
			}
		}
	}
</script>

<style lang="scss">
	.sort-picker {
		display: flex;
		flex-wrap: wrap;
		gap: 15rpx;
	}

	.sort-item {
		display: flex;
		align-items: center;
		padding: 8rpx 16rpx;
		background-color: #f5f5f5;
		border-radius: 6rpx;
		cursor: pointer;
	}

	.sort-text {
		font-size: 28rpx;
		color: #333;
		margin-right: 8rpx;
	}

	.sort-text.active-text {
		color: $uni-color-success;
	}

	.sort-icons {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		width: 24rpx;
		height: 32rpx;
	}

	.sort-icon {
		width: 0;
		height: 0;
		border-left: 10rpx solid transparent;
		border-right: 10rpx solid transparent;
		opacity: 0.4;
	}

	.sort-icon.up {
		border-bottom: 12rpx solid #666;
		margin-bottom: 2rpx;
	}

	.sort-icon.down {
		border-top: 12rpx solid #666;
		margin-top: 2rpx;
	}

	.sort-icon.active {
		opacity: 1;
		color: $uni-color-success;
	}

	.sort-icon.up.active {
		border-bottom-color: $uni-color-success ;
	}

	.sort-icon.down.active {
		border-top-color: $uni-color-success;
	}
</style>