const base = {
	get() {
		return {
			url : "http://localhost:8080/djangop8gh5erc/",
			name: "djangop8gh5erc",
			// 退出到首页链接
			indexUrl: 'http://localhost:8080/front/dist/index.html'
		};
	},
	getProjectName(){
		return {
			projectName: "基于spank的社交媒体情感分析系统的设计与实现"
		} 
	},
	getUsersName(){
		return {
			usersname: '管理员'
		}
	},
	getBgName() {
		return {
			bgNameList: [
				{
					name: '后台登录页',
					value: 'bLoginBackgroundImg'
				},
				{
					name: '后台注册页',
					value: 'bRegisterBackgroundImg'
				},
				{
					name: '后台首页',
					value: 'bIndexBackgroundImg'
				},
				{
					name: '后台头部LOGO',
					value: 'bTopLogo'
				},
				{
					name: '后台首页LOGO',
					value: 'bHomeLogo'
				},
				{
					name: '前台登录页',
					value: 'fLoginBackgroundImg'
				},
				{
					name: '前台注册页',
					value: 'fRegisterBackgroudImg'
				},
				{
					name: '前台头部LOGO',
					value: 'fTopLogo'
				},
				{
					name: 'APP登录页',
					value: 'appLoginBackgroundImg'
				},
				{
					name: 'APP注册页',
					value: 'appRegisterBackgroudImg'
				},
				{
					name: 'APP登录页LOGO',
					value: 'appLoginLogo'
				},
				{
					name: 'APP注册页LOGO',
					value: 'appRegLogo'
				},
			]
		}
	}
}
export default base
