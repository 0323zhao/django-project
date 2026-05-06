<template>
	<div>

		<div class="container" :style="{'backgroundImage': indexBgUrl?`url(${$config.baseUrl + indexBgUrl})`:''}">
			<el-form class='rgs-form animate__animated animate__' v-if="pageFlag=='register'" ref="registerForm" :model="registerForm" :rules="rules">
				<div class="rgs-form2">
					<div class="title">基于spank的社交媒体情感分析系统的设计与实现</p></div>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="yonghuzhanghao">
						<div class="label" :class="changeRules('yonghuzhanghao')?'required':''">用户账号：</div>
						<el-input v-model="registerForm.yonghuzhanghao" :readonly="ro.yonghuzhanghao" placeholder="请输入用户账号" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="mima">
						<div class="label" :class="changeRules('mima')?'required':''">密码：</div>
						<el-input v-model="registerForm.mima" type="password" placeholder="请输入密码"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="mima2">
						<div class="label" :class="changeRules('mima')?'required':''">确认密码：</div>
						<el-input v-model="registerForm.mima2" type="password" placeholder="请再次输入密码" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="yonghuxingming">
						<div class="label" :class="changeRules('yonghuxingming')?'required':''">用户姓名：</div>
						<el-input v-model="registerForm.yonghuxingming" :readonly="ro.yonghuxingming" placeholder="请输入用户姓名" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="touxiang">
						<div class="label" :class="changeRules('touxiang')?'required':''">头像：</div>
						<file-upload
							tip="点击上传头像"
							action="file/upload"
							:limit="1"
							:multiple="true"
							:fileUrls="registerForm.touxiang?registerForm.touxiang:''"
							@change="yonghutouxiangUploadChange"
						></file-upload>
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="xingbie">
						<div class="label" :class="changeRules('xingbie')?'required':''">性别：</div>
						<el-select filterable v-model="registerForm.xingbie" placeholder="请选择性别" :disabled="ro.xingbie">
							<el-option
								v-for="(item,index) in yonghuxingbieOptions"
								:key="index"
								:label="item"
								:value="item">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item v-if="tableName=='yonghu'" class="el-email list-item">
						<div class="label required">手机号：</div>
						<div style="display: flex;flex: 1;">
							<input v-model="registerForm.mobile" type="text" id="mobile" name="mobile" placeholder="请输入手机号" autocomplete="off" class="emailInput">
							<button v-if="isEndFlag" @click="sendsmscode" id="sendsmscode" type="button" class="el-btn">发送验证码</button>
							<button v-if="!isEndFlag" disabled="disabled" type="button" class="el-btn">{{count}}秒后重发</button>
						</div>
					</el-form-item>
					<el-form-item v-if="tableName=='yonghu'" class="el-email list-item">
						<div class="label required">验证码：</div>
						<el-input v-model="smscode" type="text" id="smscode" name="smscode" placeholder="请输入验证码" autocomplete="off" class="el-input" />
					</el-form-item>
					<div class="register-btn">
						<div class="register-btn1">
							<el-button class="register_btn" type="primary" @click="submitForm('registerForm')">注册</el-button>
						</div>
						<div class="register-btn2">
							<router-link class="has_btn" to="/login">已有账号，直接登录</router-link>
						</div>
					</div>
				</div>
				<div class="idea1"></div>
				<div class="idea2"></div>
			</el-form>
		</div>
	</div>
</div>
</template>

<script>
	import 'animate.css';

export default {
    //数据集合
    data() {
		return {
            pageFlag : '',
			tableName: '',
			registerForm: {},
			forgetForm: {},
			rules: {},
			ro: {},
			requiredRules: {},
            yonghuxingbieOptions: [],
            smscode:'',
			//倒计时60s
			count: 60,
			//倒计时定时器
			inter: null,
			//倒计结束标识
			isEndFlag: true,
			indexBgUrl: '',
		}
    },
	mounted() {
		if(this.$route.query.pageFlag=='register'){
			this.tableName = this.$route.query.role;
			if(this.tableName=='yonghu'){
				this.registerForm = {
					yonghuzhanghao: '',
					mima: '',
					mima2: '',
					yonghuxingming: '',
					touxiang: '',
					xingbie: '',
					mobile: '',
					status: '',
				}
				this.ro = {
					yonghuzhanghao: false,
					mima: false,
					yonghuxingming: false,
					touxiang: false,
					xingbie: false,
					mobile: false,
					status: false,
				}
			}
			if ('yonghu' == this.tableName) {
				this.rules.yonghuzhanghao = [{ required: true, message: '请输入用户账号', trigger: 'blur' }];
				this.requiredRules.yonghuzhanghao = [{ required: true, message: '请输入用户账号', trigger: 'blur' }]
				this.rules.mima = [{ required: true, message: '请输入密码', trigger: 'blur' }];
				this.requiredRules.mima = [{ required: true, message: '请输入密码', trigger: 'blur' }]
				this.rules.yonghuxingming = [{ required: true, message: '请输入用户姓名', trigger: 'blur' }];
				this.requiredRules.yonghuxingming = [{ required: true, message: '请输入用户姓名', trigger: 'blur' }]
				this.yonghuxingbieOptions = "男,女".split(',');
				this.rules.mobile = [{ required: true, validator: this.$validate.isMobile, trigger: 'blur' }];
				this.rules.status = [{ required: true, validator: this.$validate.isIntNumer, trigger: 'blur' }];
			}
		}
	},
    created() {
		this.$http.get('config/info?name=fRegisterBackgroudImg',).then(rs=>{this.indexBgUrl = rs.data.data?rs.data.data.value:''})
		this.pageFlag = this.$route.query.pageFlag;
    },
    //方法集合
    methods: {
		changeRules(name){
			if(this.requiredRules[name]){
				return true
			}
			return false
		},
		// 获取uuid
		getUUID () {
			return new Date().getTime();
		},
        // 下二随
		yonghutouxiangUploadChange(fileUrls) {
			this.registerForm.touxiang = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
		},

		// 多级联动参数

		sendsmscode() {
			if(!this.registerForm.mobile){
				this.$message.error(`手机号码不能为空`);
				return
			}
			let mobileF = this.$validate.isMobile2(this.registerForm.mobile);
			if(this.registerForm.mobile&&(!this.$validate.isMobile2(this.registerForm.mobile))){
				this.$message.error(`请输入正确的手机格式`);
				return
			}
			this.isEndFlag = false;
			var _this = this;
			this.inter = window.setInterval(function() {
				_this.count = _this.count - 1;
				if (_this.count <= 0) {
					window.clearInterval(_this.inter);
					_this.isEndFlag = true;
					_this.count=60;
				}
			}, 1000);
			this.$http({
				url: `${this.tableName}/sendsms?mobile=`+this.registerForm.mobile,
				method: "get",
				params: {}
			}).then(({ data }) => {
				if (data && data.code === 0) {
					this.$message.success(`发送成功`);
				} else {
					this.$message.error(data.msg)
				}
			});
		},

		submitForm(formName) {
			this.$refs[formName].validate((valid) => {
				if (valid) {
					var url=this.tableName+"/register";
					if(`yonghu` == this.tableName ){
						url=this.tableName+"/register?smscode="+this.smscode;
						if(this.registerForm.mobile&&(!this.$validate.isMobile2(this.registerForm.mobile))){
							this.$message.error(`请输入正确的手机格式`);
							return
						}
					}
					if((!this.smscode) && `yonghu` == this.tableName){
						this.$message.error(`验证码不能为空`);
						return
					}
					if(`yonghu` == this.tableName && this.registerForm.mima!=this.registerForm.mima2) {
						this.$message.error(`两次密码输入不一致`);
						return
					}
					this.$http.post(url, this.registerForm).then(res => {
						if (res.data.code === 0) {
							this.$message({
								message: '注册成功',
								type: 'success',
								duration: 1500,
								onClose: () => {
									this.$router.push('/login');
								}
							});
						} else {
							this.$message.error(res.data.msg);
						}
					});
				} else {
					return false;
				}
			});
		},
		resetForm(formName) {
			this.$refs[formName].resetFields();
		},
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.container {
		padding: 30px 0;
		background-repeat: no-repeat;
		background-size: 100% 100% !important;
		background-attachment: fixed;
		background: url(http://codegen.caihongy.cn/20251208/2b6ea75742934e0d8f62eb3ea599392c.jpg) no-repeat center / 100% 100%;
		display: flex;
		width: 100%;
		min-height: 100vh;
		justify-content: center;
		align-items: center;
		background-position: center center;
		position: relative;
		background: url(http://codegen.caihongy.cn/20251208/2b6ea75742934e0d8f62eb3ea599392c.jpg) no-repeat center / 100% 100%;
		.rgs-form {
			border-radius: 40px;
			padding: 30px 30px 30px 600px;
			box-shadow: 0 0px 0px rgba(0, 0, 0, .5);
			margin: 0 auto;
			z-index: 10;
			background: rgba(255,255,255,0.3);
			width: 80%;
			position: relative;
			height: auto;
			.rgs-form2 {
				width: 100%;
				.title {
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
				.subtitle {
					margin: 0 0 10px 0;
					text-shadow: 4px 4px 2px rgba(64, 158, 255, .5);
					color: rgba(64, 158, 255, 1);
					width: 100%;
					font-size: 20px;
					line-height: 44px;
					text-align: center;
				}
				.list-item {
					padding: 0;
					margin: 15px auto 0;
					width: 100%;
					border-color: #ff6f3c50;
					border-width: 0;
					position: relative;
					border-style: dashed;
					height: auto;
					/deep/.el-form-item__content {
						padding: 0 0 0 120px;
						display: block;
						width: 100%;
						.label {
							padding: 0 5px 0 0;
							z-index: 9;
							color: #333;
							left: 0;
							width: 120px;
							font-size: 16px;
							line-height: 40px;
							position: absolute !important;
							text-align: right;
						}
						
						.required {
							position: relative;
						}
						.required::after{
							color: red;
							left: 110px;
							position: absolute;
							content: "*";
						}
						.el-input {
							flex: 1;
							width: 100%;
						}
						.el-input .el-input__inner {
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
						.el-input .el-input__inner:focus {
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
						.el-input-number {
							flex: 1;
							width: 100%;
						}
						.el-input-number .el-input__inner {
							text-align: left;
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
						.el-input-number .el-input-number__decrease {
							display: none;
						}
						.el-input-number .el-input-number__increase {
							display: none;
						}
						.el-select {
							flex: 1;
							width: 100%;
						}
						.el-select .el-input__inner {
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
						.el-select .el-input__inner:focus {
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
						.el-date-editor {
							flex: 1;
							width: 100%;
						}
						.el-date-editor .el-input__inner {
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
						.el-date-editor .el-input__inner:focus {
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
						.el-upload--picture-card {
							background: transparent;
							border: 0;
							border-radius: 0;
							width: auto;
							height: auto;
							line-height: initial;
							vertical-align: middle;
						}
						.upload .upload-img {
							border: 1px solid #000000;
							cursor: pointer;
							border-radius: 0;
							color: #000000;
							background: rgba(255,255,255,.5);
							object-fit: cover;
							width: 60px;
							font-size: 22px;
							line-height: 60px;
							text-align: center;
							height: 60px;
						}
						.el-upload-list .el-upload-list__item {
							border: 1px solid #000000;
							cursor: pointer;
							border-radius: 0;
							color: #000000;
							background: rgba(255,255,255,.5);
							object-fit: cover;
							width: 60px;
							font-size: 22px;
							line-height: 60px;
							text-align: center;
							height: 60px;
							font-size: 14px;
							line-height: 1.8;
						}
						.el-upload .el-icon-plus {
							border: 1px solid #000000;
							cursor: pointer;
							border-radius: 0;
							color: #000000;
							background: rgba(255,255,255,.5);
							object-fit: cover;
							width: 60px;
							font-size: 22px;
							line-height: 60px;
							text-align: center;
							height: 60px;
						}
						.el-upload__tip {
							color: #000000;
							font-size: 16px;
						}
						.emailInput {
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
						.emailInput:focus {
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
						.el-btn {
							border: 0;
							cursor: pointer;
							padding: 0 15px;
							margin: 0 0 5px;
							color: #000;
							font-size: 15px;
							float: right;
							border-radius: 20px;
							box-shadow: 0 0 0px rgba(64, 158, 255, .5);
							outline: none;
							background: #fff;
							width: auto;
							height: 60px;
						}
						.el-btn:hover {
							opacity: 0.5;
						}
						
						.el-input__inner::placeholder {
							color: #999;
							font-size: 16px;
						}
						input::placeholder {
							color: #999;
							font-size: 16px;
						}
						.editor {
							margin: 0 0 15px;
							background: #fff;
							width: 100%;
							height: auto;
						}
						.editor .ql-toolbar {
							background: none;
						}
						.editor .ql-container {
							background: none;
						}
						.editor .ql-container .ql-blank::before {
							color: #999;
						}
					}
				}
				.register-btn {
					padding: 0;
					margin: 0px 0 0;
					width: 100%;
				}
				.register-btn1 {
					margin: 0 0 30px 0;
					width: 100%;
					text-align: center;
				}
				.register-btn2 {
					width: 100%;
					text-align: center;
				}
				.register_btn {
					border: 0 solid #707070;
					cursor: pointer;
					padding: 0 24px;
					margin: 0 auto;
					color: #000;
					display: inline-block;
					font-size: 20px;
					line-height: 60px;
					transition: all 0s;
					border-radius: 27px;
					outline: none;
					background: #fff;
					width: 417px;
					min-width: 150px;
					height: 60px;
				}
				.register_btn:hover {
					opacity: 0.8;
				}
				.has_btn {
					cursor: pointer;
					padding: 0;
					color: #000;
					text-decoration: none;
					display: inline-block;
					font-size: 16px;
				}
				.has_btn:hover {
					opacity: 0.8;
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
	
	::-webkit-scrollbar {
		display: none;
	}
</style>
