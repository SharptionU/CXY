// 工具函数集合
const commonUtil = {
	// 防抖函数
	debounce(fn, delay = 300) {
		let timer = null
		return function(...args) {
			if (timer) clearTimeout(timer)
			timer = setTimeout(() => {
				fn.apply(this, args)
			}, delay)
		}
	},

	// 节流函数
	throttle(fn, interval = 300) {
		let lastTime = 0
		return function(...args) {
			const nowTime = Date.now()
			if (nowTime - lastTime >= interval) {
				fn.apply(this, args)
				lastTime = nowTime
			}
		}
	},

	// 格式化日期
	formatDate(date, fmt = 'yyyy-MM-dd hh:mm:ss') {
		if (!(date instanceof Date)) {
			date = new Date(date)
		}
		const o = {
			'M+': date.getMonth() + 1,
			'd+': date.getDate(),
			'h+': date.getHours(),
			'm+': date.getMinutes(),
			's+': date.getSeconds(),
			'q+': Math.floor((date.getMonth() + 3) / 3),
			'S': date.getMilliseconds()
		}
		if (/(y+)/.test(fmt)) {
			fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
		}
		for (const k in o) {
			if (new RegExp('(' + k + ')').test(fmt)) {
				fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k])
					.length)))
			}
		}
		return fmt
	},

	getAbspath(url) {
		// 检查url是否以/开头（相对路径）且base存在
		if (url && typeof url === 'string' && url.startsWith("/")) {
			return uni.$http.baseUrl + url;
		}
		// 其他情况返回原url（绝对路径或无效输入）
		return url;
	},

	// 格式化距离
	formatDistance(distance) {

		// 确保输入是数字
		if (typeof distance !== 'number') {
			distance = parseFloat(distance);
			if (isNaN(distance)) {
				return '无效距离';
			}
		}
		if (distance >= 1000) {
			// 转换为公里并保留一位小数
			return (distance / 1000).toFixed(1) + '公里';
		} else {
			// 保持为米并四舍五入到整数
			return Math.round(distance) + '米';
		}
	},
	
}

export default commonUtil