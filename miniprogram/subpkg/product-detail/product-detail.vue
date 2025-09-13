<template>
	<view>
		<uni-goods-nav></uni-goods-nav>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				product_id: "",
				productDetail: {},

			};
		},
		onLoad(options) {
			this.product_id = options.product_id,
			this.getProductDetail()
		},
		methods: {
			async getProductDetail() {
				const {
					data,
					statusCode
				} = await uni.$http.get("/public/product/" + this.id)
				if (statusCode !== 200) {
					uni.$msg("数据获取失败！")
				} else {
					this.productDetail = data
				}
			}
		}
	}
</script>

<style lang="scss">

</style>