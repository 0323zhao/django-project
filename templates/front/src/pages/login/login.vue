<template>
	<div>
		<div class="login-container" :style="{'backgroundImage': indexBgUrl?`url(${$config.baseUrl + indexBgUrl})`:''}">
			<el-form ref="loginForm" :model="loginForm" :rules="rules" class="login_form animate__animated animate__">
				<div class="login_form2">
					<div class="login-title">基于spank的社交媒体情感分析系统的设计与实现</div>
					<div v-if="loginType==1" class="list-item" prop="username">
						<div class="lable">
							账号：
						</div>
						<input v-model="loginForm.username" placeholder="请输入账号：">
					</div>
					<div v-if="loginType==4" class="list-item" prop="username">
						<div class="lable">
							手机号
						</div>
						<input v-model="phone" placeholder="请输入手机号">
					</div>
					<div class="list-code" v-if="loginType==4">
						<div class="lable">
							手机验证码
						</div>
						<input v-model="phonecode" placeholder="请输入手机验证码" type="text">
						<div v-if="isEndFlag" class="nums" @click="phoneClick">
							发送验证码
						</div>
						<div v-if="!isEndFlag" class="nums">
							{{emailText}}
						</div>
					</div>
					<div class="list-item" v-if="phoneroles.length>1&&loginType==4">
						<div class="lable">
							角色：
						</div>
						<div class="list-type" prop="role">
							<el-radio v-model="loginForm.tableName" :label="item.tableName" v-for="(item, index) in phoneroles" :key="index" @change.native="getCurrentRow(item)">{{item.roleName}}</el-radio>
						</div>
					</div>
					<div v-if="loginType==1" class="list-item" prop="password">
						<div class="lable">
							密码：
						</div>
						<div class="password-box">
							<input v-model="loginForm.password" placeholder="请输入密码：" :type="showPassword?'text':'password'">
							<span class="icon iconfont" :class="showPassword?'icon-liulan13':'icon-liulan17'" @click="showPassword=!showPassword"></span>
						</div>
					</div>

					<div class="list-item" v-if="roles.length>1&&loginType<=2">
						<div class="lable">
							角色：
						</div>
						<div class="list-type" prop="role">
							<el-radio v-model="loginForm.tableName" :label="item.tableName" v-for="(item, index) in roles" :key="index" @change.native="getCurrentRow(item)">{{item.roleName}}</el-radio>
						</div>
					</div>

			
					<div class="list-btn">
						<el-button class="login_btn" v-if="loginType==1||loginType==3||loginType==4" @click="submitForm('loginForm')">登录</el-button>

						<div class="list-btn2">
							<router-link class="register_btn" :to="{path: '/register', query: {role: item.tableName,pageFlag:'register'}}" v-if="item.hasFrontRegister=='是'" v-for="(item, index) in roles2" :key="index">注册{{item.roleName.replace('注册','')}}</router-link>
							<a v-if="loginType==1" class="resetpwd_btn" @click="loginType=4;loginForm.tableName=''">手机号登录</a>
							<a v-if="loginType==2||loginType==3||loginType==4" class="resetpwd_btn" @click="passwordLoginChange">用户密码登录</a>
						</div>
					</div>
				</div>
				<div class="idea1"></div>
				<div class="idea2"></div>
			</el-form>
		</div>
	</div>
</template>

<script>
	import 'animate.css';
import menu from '@/config/menu'
export default {
	//数据集合
	data() {
		return {
            baseUrl: this.$config.baseUrl,
            loginType: 1,
			roleMenus: [],
			loginForm: {
				username: '',
				password: '',
				tableName: '',
			},
			phone: '',
			phonecode: '',
			phoneroles: [
				{
					tableName: 'yonghu',
					roleName: '用户'
				},
			],
			// 倒计时时间
			count: 60,
			// 倒计时定时器
			inter: null,
			// 倒计时是否结束
			isEndFlag: true,
			role: '',
			roles: [],
			roles2: [],
			rules: {
				username: [
					{ required: true, message: '请输入账号', trigger: 'blur' }
				],
				password: [
					{ required: true, message: '请输入密码', trigger: 'blur' }
				]
			},
			codes: [{
				num: 1,
				color: '#000',
				rotate: '10deg',
				size: '16px'
			}, {
				num: 2,
				color: '#000',
				rotate: '10deg',
				size: '16px'
			}, {
				num: 3,
				color: '#000',
				rotate: '10deg',
				size: '16px'
			}, {
				num: 4,
				color: '#000',
				rotate: '10deg',
				size: '16px'
			}],
			flag: false,
			verifyCheck2: false,
			showPassword: false,
			indexBgUrl: ''
		}
	},
	components: {
	},
	created() {
		this.$http.get('config/info?name=fLoginBackgroundImg',).then(rs=>{this.indexBgUrl = rs.data.data?rs.data.data.value:''})
		this.roleMenus = menu.list()
		for(let item in this.roleMenus) {
			if(this.roleMenus[item].hasFrontLogin=='是') {
				this.roles.push(this.roleMenus[item]);
			}
			if(this.roleMenus[item].hasFrontRegister=='是') {
				this.roles2.push(this.roleMenus[item]);
			}
		}
		
	},
	mounted() {
	},
	computed: {
		emailText: function() {
			var time = this.count;
			if (null != time && "" != time) {
				time = parseInt(time) + "秒后重发";
			}
			return time;
		}
	},
	//方法集合
	methods: {
		phoneClick() {
			if(!this.phone){
				this.$message.error(`手机号码不能为空`);
				return
			}
			if(this.phone&&(!this.$validate.isMobile2(this.phone))){
				this.$message.error(`请输入正确的手机格式`);
				return
			}
			if (this.phoneroles.length!=1) {
				if (!this.role) {
					this.$message.error("请选择登录用户类型");
					return false;
				}
			} else {
				this.role = this.phoneroles[0].roleName;
				this.loginForm.tableName = this.phoneroles[0].tableName;
			}
			var _this = this;
			this.$http({
				url: `${this.loginForm.tableName}/sendsms/login?mobile=`+this.phone,
				method: "get",
				params: {}
			}).then(({ data }) => {
				if (data && data.code === 0) {
					this.isEndFlag = false;
					this.inter = window.setInterval(function() {
						_this.count = _this.count - 1;
						if (_this.count <= 0) {
							window.clearInterval(_this.inter);
							_this.isEndFlag = true;
							_this.count=60;
						}
					}, 1000);
					this.$message.success(`发送成功`);
				} else {
					this.$message.error(data.msg)
				}
			});
		},
		randomString() {
			var len = 4;
			var chars = [
				'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
				'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
				'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
				'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
				'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2',
				'3', '4', '5', '6', '7', '8', '9'
			]
			var colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
			var sizes = ['14', '15', '16', '17', '18']
			
			var output = []
			for (var i = 0; i < len; i++) {
				// 随机验证码
				var key = Math.floor(Math.random() * chars.length)
				this.codes[i].num = chars[key]
				// 随机验证码颜色
				var code = '#'
				for (var j = 0; j < 6; j++) {
					var key = Math.floor(Math.random() * colors.length)
					code += colors[key]
				}
				this.codes[i].color = code
				// 随机验证码方向
				var rotate = Math.floor(Math.random() * 45)
				var plus = Math.floor(Math.random() * 2)
				if (plus == 1) rotate = '-' + rotate
				this.codes[i].rotate = 'rotate(' + rotate + 'deg)'
				// 随机验证码字体大小
				var size = Math.floor(Math.random() * sizes.length)
				this.codes[i].size = sizes[size] + 'px'
			}
		},
		getCurrentRow(row) {
			this.role = row.roleName;
		},
		submitForm(formName) {
			if(this.loginType==1) {
				if (this.roles.length!=1) {
					if (!this.role) {
						this.$message.error("请选择登录用户类型");
						return false;
					}
				} else {
					this.role = this.roles[0].roleName;
					this.loginForm.tableName = this.roles[0].tableName;
				}
				if (!this.loginForm.username) {
					this.$message.error("请输入用户名");
					return;
				}
				if (!this.loginForm.password) {
					this.$message.error("请输入密码");
					return;
				}
			}
			if(this.loginType==3) {
				if (!this.phone) {
					this.$message.error("请输入手机号");
					return;
				}
				if (!this.phonecode) {
					this.$message.error("请输入手机验证码");
					return;
				}
				if (this.phoneroles.length!=1) {
					if (!this.role) {
						this.$message.error("请选择登录用户类型");
						return false;
					}
				} else {
					this.role = this.phoneroles[0].roleName;
					this.loginForm.tableName = this.phoneroles[0].tableName;
				}
			}

			this.loginPost(formName)
		},
		passwordLoginChange() {
			this.loginType = 1
		},
		loginPost(formName) {
				if(this.loginType==4) {
					this.phoneLogin()
					return false
				}
			this.$refs[formName].validate((valid) => {
				if (valid) {
					this.$http.get(`${this.loginForm.tableName}/login`, {params: this.loginForm}).then(res => {
						if (res.data.code === 0) {
							localStorage.setItem('frontToken', res.data.token);
							localStorage.setItem('UserTableName', this.loginForm.tableName);
							localStorage.setItem('username', this.loginForm.username);
							localStorage.setItem('frontSessionTable', this.loginForm.tableName);
							localStorage.setItem('frontRole', this.role);
							localStorage.setItem('keyPath', 0);
							this.$router.push('/');
							this.$message({
								message: '登录成功',
								type: 'success',
								duration: 1500,
							});
						} 
						else {
							this.$message.error(res.data.msg);
						}
					});
				} else {
					return false;
				}
			});
		},
		phoneLogin() {
			this.$http.post(`${this.loginForm.tableName}/sms/login?mobile=` + this.phone + '&smscode=' + this.phonecode,{}).then(res=>{
				if(res.data.code === 0) {
					localStorage.setItem('frontToken', res.data.token);
					localStorage.setItem('UserTableName', this.loginForm.tableName);
					localStorage.setItem('username', res.data.username);
					localStorage.setItem('frontSessionTable', this.loginForm.tableName);
					localStorage.setItem('frontRole', this.role);
					localStorage.setItem('keyPath', 0);
					this.$router.push('/');
					this.$message({
						message: '登录成功',
						type: 'success',
						duration: 1500,
					});
				} 
				else {
					this.$message.error(res.data.msg);
				}
			})
		},
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.login-container {
		background-repeat: no-repeat;
		background-size: 100% 100% !important;
		background: url(http://codegen.caihongy.cn/20251208/2b6ea75742934e0d8f62eb3ea599392c.jpg) no-repeat center / 100% 100%;
		display: flex;
		width: 100%;
		min-height: 100vh;
		justify-content: center;
		align-items: center;
		background-position: center center;
		position: relative;
		background: url(http://codegen.caihongy.cn/20251208/2b6ea75742934e0d8f62eb3ea599392c.jpg) no-repeat center / 100% 100%;
		.login_form {
			border-radius: 40px;
			padding: 30px 30px 30px 600px;
			box-shadow: 0 0px 0px rgba(0, 0, 0, .5);
			margin: 0 auto;
			z-index: 10;
			background: rgba(255,255,255,0.3);
			width: 80%;
			position: relative;
			height: auto;
			.login_form2 {
				width: 100%;
				.login-title {
					padding: 0 0 10px;
					margin: 0 0 0px 0;
					color: #000000;
					font-weight: 600;
					font-size: 22px;
					border-color: #ff6f3c50;
					line-height: 2;
					text-shadow: none;
					top: 40%;
					left: 0;
					background: none;
					width: 600px;
					border-width: 0;
					position: absolute;
					border-style: solid;
					text-align: center;
				}
				.list-item {
					margin: 0 0 30px 0;
					display: flex;
					width: 100%;
					border-color: #ff6f3c50;
					border-width: 0;
					align-items: center;
					border-style: dashed;
					.lable {
						color: #000;
						width: 160px;
						font-size: 16px;
						line-height: 40px;
						text-align: right;
					}
					input {
						border: 1px solid #000000;
						border-radius: 0;
						padding: 0 30px;
						box-shadow: none;
						color: #000000;
						flex: 1;
						background: none;
						width: 100%;
						font-size: 16px;
						height: 60px;
					}
					input:focus {
						border: 1px solid #000000;
						border-radius: 0;
						padding: 0 30px;
						box-shadow: none;
						color: #000000;
						flex: 1;
						background: none;
						width: 100%;
						font-size: 16px;
						height: 60px;
					}
					.password-box {
						flex: 1;
						display: flex;
						width: calc(100% - 100px);
						position: relative;
						align-items: center;
						input {
							border: 1px solid #000000;
							border-radius: 0;
							padding: 0 30px;
							box-shadow: none;
							color: #000000;
							flex: 1;
							background: none;
							width: 100%;
							font-size: 16px;
							height: 60px;
						}
						input:focus {
							border: 1px solid #000000;
							border-radius: 0;
							padding: 0 30px;
							box-shadow: none;
							color: #000000;
							flex: 1;
							background: none;
							width: 100%;
							font-size: 16px;
							height: 60px;
						}
						.iconfont {
							cursor: pointer;
							z-index: 1;
							color: #000;
							top: 0;
							font-size: 16px;
							line-height: 60px;
							position: absolute;
							right: 30px;
						}
					}
					input::placeholder {
						color: #999;
						font-size: 16px;
					}
				}
				.list-code {
					margin: 0 0 30px 0;
					display: flex;
					width: 100%;
					border-color: #ff6f3c50;
					border-width: 0;
					align-items: center;
					border-style: dashed;
					.lable {
						color: #000;
						width: 160px;
						font-size: 16px;
						line-height: 40px;
						text-align: right;
					}
					input {
						border: 1px solid #000000;
						border-radius: 0;
						padding: 0 30px;
						box-shadow: none;
						color: #000000;
						flex: 1;
						background: none;
						width: 100%;
						font-size: 16px;
						height: 60px;
					}
					input:focus {
						border: 1px solid #000000;
						border-radius: 0;
						padding: 0 30px;
						box-shadow: none;
						color: #000000;
						flex: 1;
						background: none;
						width: 100%;
						font-size: 16px;
						height: 60px;
					}
					.nums {
						cursor: pointer;
						padding: 0 15px;
						margin: 0 0 5px 10px;
						white-space: nowrap;
						display: inline-block;
						vertical-align: middle;
						border-color: #ddd;
						line-height: 60px;
						border-radius: 60px;
						background: #fff;
						width: auto;
						border-width: 0px;
						border-style: solid;
						text-align: center;
						height: 60px;
					}
					input::placeholder {
						color: #999;
						font-size: 16px;
					}
				}
				.list-type {
					flex: 1;
					width: 100%;
					line-height: 60px;
					height: 60px;
					/deep/ .el-radio__input .el-radio__inner {
						background: rgba(53, 53, 53, 0);
						border-color: #333;
					}
					/deep/ .el-radio__input.is-checked .el-radio__inner {
						background: #000000;
						border-color: #000000;
					}
					/deep/ .el-radio__label {
						color: #333;
						font-size: 16px;
					}
					/deep/ .el-radio__input.is-checked+.el-radio__label {
						color: #000000;
						font-size: 16px;
					}
				}
				.list-btn {
					padding: 0;
					margin: 0px auto;
					align-content: center;
					display: flex;
					width: 100%;
					align-items: center;
					flex-wrap: wrap;
					text-align: center;
					.login_btn {
						border: 0 solid #707070;
						cursor: pointer;
						padding: 0 24px;
						margin: 0 auto;
						color: #000000;
						display: inline-block;
						font-size: 20px;
						line-height: 60px;
						transition: all 0s;
						border-radius: 27px;
						outline: none;
						background: #FFFFFF;
						width: 417px;
						min-width: 150px;
						height: 60px;
					}
					.login_btn:hover {
						opacity: 0.8;
					}
					.list-btn2 {
						padding: 0;
						margin: 0px 0 0;
						display: flex;
						width: 100%;
						justify-content: center;
						align-items: center;
						flex-wrap: wrap;
						text-align: center;
						.register_btn {
							cursor: pointer;
							padding: 0 20px;
							margin: 0;
							color: #000000;
							background: none;
							flex: none;
							display: inline-block;
							text-decoration: none;
							font-size: 16px;
							line-height: 60px;
							height: 60px;
						}
						.register_btn:hover {
							opacity: 0.8;
						}
						.resetpwd_btn {
							cursor: pointer;
							margin: 0;
							color: #000;
							display: inline-block;
							width: auto;
							font-size: 16px;
							text-align: center;
						}
						.resetpwd_btn:hover {
							opacity: 0.8;
						}
					}
				}
			}
			.idea1 {
				background: red;
				display: none;
				width: 100%;
				height: 40px;
			}
			.idea2 {
				background: blue;
				display: none;
				width: 100%;
				height: 40px;
			}
		}
	}
</style>
