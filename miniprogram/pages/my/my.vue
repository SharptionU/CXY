<template>
	<view>
		<scroll-text :scrollText="scrollText"></scroll-text>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				scrollText:[
					"这是一条公告",
					"这是另一条公告"
				]
			};
		}
	}
</script>

<style lang="scss">

</style>
