import {
	defineStore
} from "pinia"

export const userStore = defineStore("user", {

	state: () => ({
		username: "",
		is_login: false,
		jwt_token: "",
		union_id: "",
	}),
	actions: {
		loadLocalUser() {
			savedInfo=  uni.getStorageSync("user_info")
			if (savedInfo){
				
			} 
			return savedInfo
		},
		login(userInfo){
			
		},
		logout(){
			
		},
		saved(){
			
		}
	},
	getters: {
		getUserName(state) {
			return state.username
		}
	}
})