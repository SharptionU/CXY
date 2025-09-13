import App from './App'

import {
	$http
} from "@escook/request-miniprogram"

// 替换全局请求对象
uni.$http = $http

// 请求base url
$http.baseUrl = "http://127.0.0.1:8000/api/v1"

// 添加请求和响应拦截器
$http.beforeRequest = function() {
	uni.showLoading({
		title: "数据加载中..."
	})
}

// 响应拦截器 隐藏loading显示效果
$http.afterRequest = function() {
	uni.hideLoading()
}


// 封装uni 弹窗方法
uni.$msg = function(m = "消息填充", d = 1500) {
	uni.showToast({
		title: m,
		duration: d,
		icon:"none"
	})
}

// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
// 导入工具类
import commonUtil from './utils/common.js'
// 挂载到Vue原型上
Vue.prototype.$utils = commonUtil

Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
	...App
})
app.$mount()
// #endif


// #ifdef VUE3
import {
	createSSRApp
} from 'vue'

import * as Pinia  from 'pinia'

// 导入工具类
import commonUtil from './utils/common.js'

export function createApp() {
	const app = createSSRApp(App)
	app.use(Pinia.createPinia())
	// 全局属性挂载
	app.config.globalProperties.$utils = commonUtil
	return {
		app,
		Pinia
	}
}
// #endif