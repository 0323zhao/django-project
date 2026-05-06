<template>
	<div class="navbar">
		<div class="title">
			<span class="title-name">{{this.$project.projectName}}</span>
		</div>
		<el-dropdown class="dropdown-box" @command="handleCommand" trigger="click">
			<div class="el-dropdown-link">
				<el-image v-if="avatar" :src="avatar?this.$base.url + avatar : require('@/assets/img/avator.png')" fit="cover"></el-image>
				<span class="label">欢迎</span>
				<span class="nickname">{{this.$storage.get('adminName')}}</span>
				<span class="icon iconfont icon-xiala"></span>
			</div>
			<el-dropdown-menu class="top-el-dropdown-menu" slot="dropdown">
				<el-dropdown-item class="item1" :command="''">
					<span class="icon iconfont icon-home19"></span>
					首页
				</el-dropdown-item>
				<el-dropdown-item class="item2" :command="'center'">
					<span class="icon iconfont icon-touxiang09"></span>
					个人中心
				</el-dropdown-item>
				<el-dropdown-item v-if="this.$storage.get('sessionTable')!='users'" class="item3" :command="'front'">
					<span class="icon iconfont icon-fanhui19"></span>
					退出到前台
				</el-dropdown-item>
				<el-dropdown-item v-if="isAuth('hasBoard','查看')" class="item3" :command="'board'">
					<span class="icon iconfont icon-fanhui19"></span>
					看板				</el-dropdown-item>
				<el-dropdown-item v-if="this.$storage.get('sessionTable')=='users'" class="item3" :command="'backUp'">
					<span class="icon iconfont icon-fanhui19"></span>
					数据备份
				</el-dropdown-item>
				<el-dropdown-item v-if="this.$storage.get('sessionTable')=='users'" class="item3" :command="'analyze'">
					<span class="icon iconfont icon-fanhui19"></span>
					数据分析
				</el-dropdown-item>
				<el-dropdown-item class="item4" :command="'logout'">
					<span class="icon iconfont icon-guanbi19"></span>
					退出登录
				</el-dropdown-item>
			</el-dropdown-menu>
		</el-dropdown>
	</div>
</template>

<script>
	import {
		Loading
	} from 'element-ui';
	import axios from 'axios';
	export default {
		data() {
			return {
				dialogVisible: false,
				ruleForm: {},
				user: null,
				topLogoUrl: '',
			};
		},
		created() {
			this.$http.get('config/info?name=bTopLogo',).then(rs=>{this.topLogoUrl = rs.data.data?rs.data.data.value:''})
		},
		computed: {
			avatar(){
				return this.$storage.get('headportrait')?this.$storage.get('headportrait'):''
			},
		},
		mounted() {
		},
		methods: {
			handleCommand(name) {
				if (name == 'logout') {
					this.onLogout()
				} 
				else if (name == 'front') {
					this.onIndexTap()
				}
				else if (name == 'board'){
					this.toBoard()
				}
				else if (name == 'backUp'){
					this.backUp()
				}
				else if (name == 'analyze'){
					this.analyzeClick()
				}
				else {
					let router = this.$router
					name = '/'+name
					router.push(name)
				}
			},
			async onLogout() {
				await this.$http.post(`${this.$storage.get('sessionTable')}/logout`).then(rs=>{
					let storage = this.$storage
					let router = this.$router
					storage.clear()
					this.$store.dispatch('tagsView/delAllViews')
					router.replace({
						name: "login"
					});
				})
			},
			onIndexTap(){
				localStorage.setItem("frontToken", localStorage.getItem("Token"));
				localStorage.setItem("frontRole", localStorage.getItem("role"));
				localStorage.setItem("frontSessionTable", localStorage.getItem("sessionTable"));
				localStorage.setItem("frontHeadportrait", localStorage.getItem("headportrait"));
				localStorage.setItem("UserTableName", localStorage.getItem("sessionTable"));
				localStorage.setItem("frontUserid", localStorage.getItem("userid"));
				localStorage.setItem("username", localStorage.getItem("adminName"));
				window.location.href = `${this.$base.indexUrl}`
			},
			toBoard(){
				let routeData = this.$router.resolve({ path: '/board'});
				window.open(routeData.href, '_blank');
			},
			analyzeClick() {
				this.$confirm('是否进行大数据分析?', '数据分析提示', {
					confirmButtonText: '是',
					cancelButtonText: '否',
					type: 'warning'
				}).then(() => {
					let loading = null;
					loading = Loading.service({
						target: this.$refs['roleMenuBox'],
						fullscreen: false,
						text: '数据分析中，请稍等...'
					})
					this.$http({
						url: '/spark/analyze',
						method: "get"
					}).then(({
						data
					}) => {
						if(loading) loading.close()
						if(data.code==0){
							this.$message({
								message: '数据分析完成',
								type: 'success',
								duration: 1500,
							});
						}
					},err=>{
						if(loading) loading.close()
					});
				});
			},
			backUp() {
				this.$confirm('是否备份数据库?', '数据备份提示', {
					confirmButtonText: '是',
					cancelButtonText: '否',
					type: 'warning'
				}).then(() => {
					this.$http({
						url: '/mysqldump',
						method: "get"
					}).then(({
						data
					}) => {
						if (data) {
							const binaryData = [];
							binaryData.push(data);
							const objectUrl = window.URL.createObjectURL(new Blob(binaryData, {
								type: 'application/pdf;chartset=UTF-8'
							}))
							const a = document.createElement('a')
							a.href = objectUrl
							a.download = 'mysql.dmp'
							// a.click()
							// 下面这个写法兼容火狐
							a.dispatchEvent(new MouseEvent('click', {
								bubbles: true,
								cancelable: true,
								view: window
							}))
							window.URL.revokeObjectURL(data)
							message.message("数据备份成功")
						} else {
							let message = this.$message
							message.error(data.msg);
						}
					});
				});
			},
		}
	};
</script>


<style lang="scss" scoped>
	.navbar {
		.title {
			margin: 0 auto 0 0;
			background: none;
			display: flex;
			width: auto;
			justify-content: center;
			align-items: center;
			height: auto;
			.title-name {
				padding: 0;
				color: #E3FDFC;
				font-weight: 600;
				font-size: 26px;
				line-height: 44px;
				float: left;
			}
		}
		.dropdown-box {
			color: #666;
			display: flex;
			font-size: 16px;
			order: 11;
			.el-dropdown-link {
				border-radius: 8px;
				padding: 5px;
				background: none;
				display: flex;
				justify-content: flex-end;
				align-items: center;
				min-width: 112px;
				height: 47px;
				.el-image {
					border-radius: 100%;
					margin: 0 10px;
					object-fit: cover;
					display: inline-block;
					width: 24px;
					height: 24px;
				}
				.label {
					color: #212D3F;
					display: none;
					font-size: 16px;
				}
				.nickname {
					color: #212D3F;
					font-size: 16px;
					line-height: 32px;
				}
				.iconfont {
					margin: 0 0 0 5px;
					color: #212D3F;
					font-size: 14px;
				}
			}
		}
	}
	.top-el-dropdown-menu {
		border: 1px solid #EBEEF5;
		border-radius: 4px;
		padding: 10px 0;
		box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
		margin: 18px 0;
		background: #FFF;
		width: 150px;
		right: 20px;
		li.el-dropdown-menu__item.item1 {
			cursor: pointer;
			padding: 0 20px;
			margin: 0;
			outline: 0;
			color: #606266;
			background: #fff;
			font-size: 14px;
			line-height: 36px;
			list-style: none;
			.iconfont {
				margin: 0 4px 0 0;
				color: #000;
				font-size: 14px;
			}
		}
		li.el-dropdown-menu__item.item1:hover {
			background: #ecf5ff;
		}
		li.el-dropdown-menu__item.item2 {
			cursor: pointer;
			padding: 0 20px;
			margin: 0;
			outline: 0;
			color: #606266;
			background: #fff;
			font-size: 14px;
			line-height: 36px;
			list-style: none;
			.iconfont {
				margin: 0 4px 0 0;
				color: #000;
				font-size: 14px;
			}
		}
		li.el-dropdown-menu__item.item2:hover {
			background: #ecf5ff;
		}
		li.el-dropdown-menu__item.item3 {
			cursor: pointer;
			padding: 0 20px;
			margin: 0;
			outline: 0;
			color: #606266;
			background: #fff;
			font-size: 14px;
			line-height: 36px;
			list-style: none;
			.iconfont {
				margin: 0 4px 0 0;
				color: #000;
				font-size: 14px;
			}
		}
		li.el-dropdown-menu__item.item3:hover {
			background: #ecf5ff;
		}
		li.el-dropdown-menu__item.item4 {
			cursor: pointer;
			padding: 0 20px;
			margin: 0;
			outline: 0;
			color: #606266;
			background: #fff;
			font-size: 14px;
			line-height: 36px;
			list-style: none;
			.iconfont {
				margin: 0 4px 0 0;
				color: #000;
				font-size: 14px;
			}
		}
		li.el-dropdown-menu__item.item4:hover {
			background: #ecf5ff;
		}
	}
</style>
