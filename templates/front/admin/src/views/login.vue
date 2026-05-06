<template>
	<div>
		<div class="login-container" :style="{'backgroundImage': indexBgUrl?`url(${$base.url + indexBgUrl})`:''}">
			<el-form class="login_form animate__animated animate__">
				<div class="login_form2">
					<div class="title-container">基于spank的社交媒体情感分析系统的设计与实现登录</div>
					<div v-if="loginType==1" class="list-item">
						<input placeholder="请输入账号：" name="username" type="text" v-model="rulesForm.username">
					</div>
					<div v-if="loginType==1" class="list-item">
						<div class="password-box">
							<input placeholder="请输入密码：" name="password" :type="showPassword?'text':'password'" v-model="rulesForm.password">
							<span class="icon iconfont" :class="showPassword?'icon-liulan13':'icon-liulan17'" @click="showPassword=!showPassword"></span>
						</div>
					</div>

					<div class="list-item select" v-if="roles.length>1&&loginType<=2">
						<el-select v-model="rulesForm.role" placeholder="请选择角色：">
							<el-option v-if="loginType==1||(loginType==2&&item.role!='users')" v-for="item in roles" :key="item.roleName" :label="item.roleName" :value="item.roleName" />
						</el-select>
					</div>

		
					<div class="login-btn">
						<div class="login-btn1">
							<el-button v-if="loginType==1||loginType==3||loginType==4" type="primary" @click="login()" class="loginInBt">登录</el-button>
						</div>
						<div class="login-btn2">
						</div>
						<div class="login-btn3">
						</div>
					</div>
				</div>
			</el-form>
		</div>
	</div>
</template>
<script>
	import 'animate.css'
	import menu from "@/utils/menu";
	export default {
		data() {
			return {
				verifyCheck2: false,
				flag: false,
				baseUrl:this.$base.url,
				loginType: 1,
				rulesForm: {
					username: "",
					password: "",
					role: "",
				},
				menus: [],
				roles: [],
				tableName: "",
				showPassword: false,
				indexBgUrl: '',
			};
		},
		mounted() {
			let menus = menu.list();
			this.menus = menus;

			for (let i = 0; i < this.menus.length; i++) {
				if (this.menus[i].hasBackLogin=='是') {
					this.roles.push(this.menus[i])
				}
			}

		},
		created() {
			this.$http.get('config/info?name=bLoginBackgroundImg',).then(rs=>{this.indexBgUrl = rs.data.data?rs.data.data.value:''})
		},
		destroyed() {
		},
		components: {
		},
		methods: {

			//注册
			register(tableName){
				this.$storage.set("loginTable", tableName);
				this.$router.push({path:'/register',query:{pageFlag:'register'}})
			},
			// 登陆
			login() {
				if(this.loginType==1) {

					if (!this.rulesForm.username) {
						this.$message.error("请输入用户名");
						return;
					}
					if (!this.rulesForm.password) {
						this.$message.error("请输入密码");
						return;
					}
					if(this.roles.length>1) {
						if (!this.rulesForm.role) {
							this.$message.error("请选择角色");
							return;
						}
					
						for (let i = 0; i < this.roles.length; i++) {
							if (this.roles[i].roleName == this.rulesForm.role) {
								this.tableName = this.roles[i].tableName;
							}
						}
					} else {
						this.tableName = this.roles[0].tableName;
						this.rulesForm.role = this.roles[0].roleName;
					}
				}
		
				this.loginPost()
			},
			loginPost() {
				this.$http({
					url: `${this.tableName}/login?username=${this.rulesForm.username}&password=${this.rulesForm.password}`,
					method: "post"
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.$storage.set("Token", data.token);
						this.$storage.set("role", this.rulesForm.role);
						this.$storage.set("sessionTable", this.tableName);
						this.$storage.set("adminName", this.rulesForm.username);
						this.$nextTick(()=>{
							this.$http({
								url: this.tableName + '/session',
								method: "get"
							}).then(({
								data
							}) => {
								if (data && data.code === 0) {
									if(this.tableName == 'yonghu') {
										this.$storage.set('headportrait',data.data.touxiang)
									}
									if(this.tableName == 'users') {
										this.$storage.set('headportrait',data.data.image)
									}
									this.$storage.set('userForm',JSON.stringify(data.data))
									this.$storage.set('userid',data.data.id);
								} else {
									let message = this.$message
									message.error(data.msg);
								}
								if(this.boardAuth('hasBoard','查看',this.rulesForm.role)) {
									this.$router.replace({ path: "/board" });
								}else {
									this.$router.replace({ path: "/" });
								}
							});
						})
					}
					else {
						this.$message.error(data.msg);
					}
				});
			},
		}
	}
</script>

<style lang="scss" scoped>
.login-container {
	min-height: 100vh;
	position: relative;
	background-repeat: no-repeat;
	background-position: center center;
	background-size: cover;
	background: url(http://codegen.caihongy.cn/20260126/b3bbb43de2cd4e47b6128878ac0e9265.jpg) no-repeat center center / 100% 100%;
	background: url(http://codegen.caihongy.cn/20260126/b3bbb43de2cd4e47b6128878ac0e9265.jpg) no-repeat center center / 100% 100%;
	display: flex;
	width: 100%;
	min-height: 100vh;
	justify-content: flex-end;
	align-items: center;
	position: relative !important;

	.login_form {
		border-radius: 10px;
		padding: 55px 35px;
		margin: 0 208px 0 0;
		z-index: 1;
		background: url(http://codegen.caihongy.cn/20250914/6f34c6f3174d4e8184c0f041a4bfafaa.png) no-repeat  center center / 100% 100%;
		width: 723px;
		.login_form2 {
			padding: 0 40px;
			margin: auto;
			align-content: center;
			background: none;
			display: flex;
			width: 100%;
			align-items: center;
			flex-wrap: wrap;
		}
		.title-container {
			margin: 0px 0 20px 0;
			color: #216CF6;
			font-weight: 600;
			width: 100%;
			font-size: 22px;
			line-height: 40px;
			text-align: center;
		}
		.list-item {
			border-radius: 0px;
			padding: 0px;
			margin: 0px auto 20px;
			background: none;
			display: flex;
			width: 585px;
			align-items: center;
			input {
				border: 1px solid #DADFE6;
				border-radius: 4px;
				padding: 0 10px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #333;
				background: #fff;
				flex: 1;
				width: 100%;
				font-size: 16px;
				height: 64px;
			}
			input:focus {
				border: 1px solid #DADFE6;
				border-radius: 4px;
				padding: 0 10px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #333;
				background: #fff;
				flex: 1;
				width: 100%;
				font-size: 16px;
				height: 64px;
			}
			.password-box {
				flex: 1;
				display: flex;
				width: 100%;
				position: relative;
				align-items: center;
				input {
					border: 1px solid #DADFE6;
					border-radius: 4px;
					padding: 0 10px;
					box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
					color: #333;
					background: #fff;
					flex: 1;
					width: 100%;
					font-size: 16px;
					height: 64px;
				}
				input:focus {
					border: 1px solid #DADFE6;
					border-radius: 4px;
					padding: 0 10px;
					box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
					color: #333;
					background: #fff;
					flex: 1;
					width: 100%;
					font-size: 16px;
					height: 64px;
				}
				.iconfont {
					cursor: pointer;
					z-index: 1;
					color: #000;
					top: 2px;
					font-size: 16px;
					line-height: 44px;
					position: absolute;
					right: 20px;
				}
			}
			input::placeholder {
				color: #C3C7CC;
				font-size: 16px;
			}
			/deep/ .el-select {
				margin: 0px auto 20px;
				flex: 1;
				width: 100%;
			}
			/deep/ .el-select .el-input__inner {
				border: 1px solid #DADFE6;
				border-radius: 4px;
				padding: 0 10px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #333;
				background: #fff;
				flex: 1;
				width: 100%;
				font-size: 16px;
				height: 64px;
			}
			/deep/ .el-select .is-focus .el-input__inner {
				border: 1px solid #DADFE6;
				border-radius: 4px;
				padding: 0 10px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #333;
				background: #fff;
				flex: 1;
				width: 100%;
				font-size: 16px;
				height: 64px;
			}
			/deep/ .el-select .el-input__inner::placeholder{
				color: #C3C7CC;
				font-size: 16px;
			}
		}
		.login-btn {
			border-radius: 30px;
			padding: 0 0px;
			margin: 0px auto 20px;
			background: none;
			display: flex;
			width: 585px;
			align-items: center;
			flex-wrap: wrap;
			.login-btn1 {
				margin: 10px 0 0 0;
				width: 100%;
				order: 1;
			}
			.login-btn2 {
			}
			.login-btn3 {
				flex: 1;
				text-align: right;
			}
			.loginInBt {
				border: 1px solid #B2F9F0;
				cursor: pointer;
				padding: 0 24px;
				margin: 0 0 15px;
				color: #FEFEF6;
				font-weight: bold;
				font-size: 18px;
				border-radius: 24px;
				box-shadow: inset 0px -6px 6px 1px #3EE3F9;
				outline: none;
				background: linear-gradient( 135deg, #087FF3 0%, #32B2F3 100%);
				width: 100%;
				height: 47px;
			}
			.loginInBt:hover {
				opacity: 0.8;
			}
			.register {
				border: 0px solid #333;
				cursor: pointer;
				border-radius: 0px;
				padding: 0;
				margin: 0 10px 15px 0;
				outline: none;
				color: #216CF6;
				background: none;
				text-decoration: underline;
				width: auto;
				font-size: 16px;
				height: 36px;
			}
			.register:hover {
				opacity: 0.8;
			}
			.forget {
				border: 0px solid #333;
				cursor: pointer;
				border-radius: 0px;
				padding: 0;
				margin: 0 10px 15px 0;
				outline: none;
				color: #0D1818;
				background: none;
				font-weight: bold;
				width: auto;
				font-size: 16px;
				height: 36px;
			}
			.forget:hover {
				opacity: 0.8;
			}
		}
	}
}

</style>
