<template>
	<view class="search-container" :style="{'background-color':bgcolor}" @click="searchHandler">
		<view class="search-box">
			<uni-icons type="search"></uni-icons>
			<text class="placeholder" :style="{'border-radius':radius}">{{placeholder}}</text>
		</view>
	</view>
</template>

<script>

	export default {
		name: "cust-search",
		props: {
			placeholder: {
				type: String,
				default: "搜索"
			},
			bgcolor: {
				type: String,
				default: "#00000000",
			},
			radius: {
				type: Number,
				default: 10
			},
			bgimageurl: { //背景图片
				type: String,
				default: ""
			},
			url: {
				type: String,
				default: ""
			}
		},
		methods: {
			searchHandler() {
				uni.navigateTo({
					url: this.url
				})
			}
		},
		data() {
			return {

			};
		}
	}
</script>

<style lang="scss">
	.search-container {
		height: 50px;
		background-color: transparent;
		display: flex;
		align-items: center;
		padding: 0 10px;

		.search-box {
			background-color: #ffffff;
			height: 30px;
			border-radius: 10px;
			width: 100%;
			display: flex;
			justify-content: center;
			align-items: center;
		}

		.placeholder {
			font-size: 15px;
			margin-left: 10px;
		}
	}
</style>