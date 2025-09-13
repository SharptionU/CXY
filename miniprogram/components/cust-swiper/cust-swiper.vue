<template>
	<view>
		这是一个自定义组件
	</view>
</template>

<script>
	export default {
		name: "cust-swiper",
		props: {
			field1: {
				type: String,
				default: "this is a String"
			},
			field2: {
				type: Number,
				default: 0
			}
		},
		data() {
			return {

			};
		}
	}
</script>

<style lang="scss">

</style>