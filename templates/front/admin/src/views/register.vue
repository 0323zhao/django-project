<template>
	<div>
		<div class="register-container" :style="{'backgroundImage': indexBgUrl?`url(${$base.url + indexBgUrl})`:''}">
			<el-form v-if="pageFlag=='register'" ref="ruleForm" class="rgs-form animate__animated animate__" :model="ruleForm" :rules="rules">
				<div class="rgs-form2">
					<div class="title">基于spank的社交媒体情感分析系统的设计与实现</div>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<el-input  v-model="ruleForm.yonghuzhanghao" :readonly="ro.yonghuzhanghao" autocomplete="off" placeholder="用户账号"  type="text"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<el-input  v-model="ruleForm.mima" :readonly="ro.mima" autocomplete="off" placeholder="密码"  type="password"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<el-input  v-model="ruleForm.mima2" autocomplete="off" placeholder="确认密码" type="password" :readonly="ro.mima" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<el-input  v-model="ruleForm.yonghuxingming" :readonly="ro.yonghuxingming" autocomplete="off" placeholder="用户姓名"  type="text"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<file-upload
							tip="点击上传头像"
							action="file/upload"
							:limit="3"
							:multiple="true"
							:fileUrls="ruleForm.touxiang?ruleForm.touxiang:''"
							@change="yonghutouxiangUploadChange"
						></file-upload>
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<el-select filterable v-model="ruleForm.xingbie" placeholder="请选择性别" :disabled="ro.xingbie">
							<el-option
								v-for="(item,index) in yonghuxingbieOptions"
								v-bind:key="index"
								:label="item"
								:value="item">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item class="list-item email" v-if="tableName=='yonghu'">
						<div style="display: flex;flex: 1;">
							<input v-model="ruleForm.mobile" autocomplete="off" placeholder="手机号"/>
							<button v-if="isEndFlag" type="success" class="register-code" @click="sendsmscode()">发送验证码</button>
							<button v-if="!isEndFlag" type="success" class="register-code" disabled="disabled">{{SecondToDate}}</button>
						</div>
					</el-form-item>
					<el-form-item class="list-item email-code" v-if="tableName=='yonghu'">
						<el-input  v-model="smscode" autocomplete="off" placeholder="验证码" />
					</el-form-item>
					<div class="register-btn">
						<div class="register-btn1">
							<button type="button" class="r-btn" @click="login()">注册</button>
						</div>
						<div class="register-btn2">
							<div class="r-login" @click="close()">已有账号，立即登录</div>
						</div>
					</div>
				</div>
			</el-form>
		</div>
	</div>
</template>

<script>
	import 'animate.css'
export default {
	data() {
		return {
			ruleForm: {
			},
			forgetForm: {},
            pageFlag : '',
			tableName:"",
			rules: {},
			ro: {},
            smscode:'',
			// 倒计时时间
			count: 60,
			// 倒计时定时器
			inter: null,
			// 倒计时是否结束
			isEndFlag: true,
            yonghuxingbieOptions: [],
			indexBgUrl: '',
		};
	},
	computed: {
		SecondToDate: function() {
			var time = this.count;
			if (null != time && "" != time) {
				time = parseInt(time) + "秒后重发";
			}
			return time;
		}
	},
	mounted(){
		this.pageFlag = this.$route.query.pageFlag
		if(this.$route.query.pageFlag=='register'){
			
			let table = this.$storage.get("loginTable");
			this.tableName = table;
			if(this.tableName=='yonghu'){
				this.ruleForm = {
					yonghuzhanghao: '',
					mima: '',
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
				this.rules.yonghuzhanghao = [{ required: true, message: '请输入用户账号', trigger: 'blur' }]
			}
			if ('yonghu' == this.tableName) {
				this.rules.mima = [{ required: true, message: '请输入密码', trigger: 'blur' }]
			}
			if ('yonghu' == this.tableName) {
				this.rules.yonghuxingming = [{ required: true, message: '请输入用户姓名', trigger: 'blur' }]
			}
			this.yonghuxingbieOptions = "男,女".split(',')
		}
	},
	created() {
		this.$http.get('config/info?name=bRegisterBackgroundImg',).then(rs=>{this.indexBgUrl = rs.data.data?rs.data.data.value:''})
	},
	destroyed() {
		  	},
	methods: {
		changeRules(name){
			if(this.rules[name]){
				return true
			}
			return false
		},
		// 获取uuid
		getUUID () {
			return new Date().getTime();
		},
		close(){
			this.$router.push({ path: "/login" });
		},
        yonghutouxiangUploadChange(fileUrls) {
            this.ruleForm.touxiang = fileUrls;
        },

        // 多级联动参数

		sendsmscode() {
			if(!this.ruleForm.mobile){
				this.$message.error(`手机号码不能为空`);
				return
			}
			if(this.ruleForm.mobile&&(!this.$validate.isMobile(this.ruleForm.mobile))){
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
				url: `${this.tableName}/sendsms?mobile=`+this.ruleForm.mobile,
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

		// 注册
		login() {
			var url=this.tableName+"/register";
			if((!this.ruleForm.yonghuzhanghao) && `yonghu` == this.tableName){
				this.$message.error(`用户账号不能为空`);
				return
			}
			if((!this.ruleForm.mima) && `yonghu` == this.tableName){
				this.$message.error(`密码不能为空`);
				return
			}
			if((this.ruleForm.mima!=this.ruleForm.mima2) && `yonghu` == this.tableName){
				this.$message.error(`两次密码输入不一致`);
				return
			}
			if((!this.ruleForm.yonghuxingming) && `yonghu` == this.tableName){
				this.$message.error(`用户姓名不能为空`);
				return
			}
            if(this.ruleForm.touxiang!=null) {
                this.ruleForm.touxiang = this.ruleForm.touxiang.replace(new RegExp(this.$base.url,"g"),"");
            }
			if(`yonghu` == this.tableName && this.ruleForm.mobile &&(!this.$validate.isMobile(this.ruleForm.mobile))){
				this.$message.error(`手机号应输入手机格式`);
				return
			}
			if(`yonghu` == this.tableName ){
				url=this.tableName+"/register?smscode="+this.smscode;
				if(this.ruleForm.mobile&&(!this.$validate.isMobile(this.ruleForm.mobile))){
					this.$message.error(`请输入正确的手机格式`);
					return
				}
			}
			if((!this.smscode) && `yonghu` == this.tableName){
				this.$message.error(`验证码不能为空`);
				return
			}
			this.$http({
				url: url,
				method: "post",
				data:this.ruleForm
			}).then(({ data }) => {
				if (data && data.code === 0) {
					this.$message({
						message: "注册成功",
						type: "success",
						duration: 1500,
						onClose: () => {
							this.$router.replace({ path: "/login" });
						}
					});
				} else {
					this.$message.error(data.msg);
				}
			});
		},
	}
};
</script>

<style lang="scss" scoped>
.register-container {
	position: relative;
	background: url(http://codegen.caihongy.cn/20260126/b3bbb43de2cd4e47b6128878ac0e9265.jpg) no-repeat center center / 100% 100%;
	background: url(http://codegen.caihongy.cn/20260126/b3bbb43de2cd4e47b6128878ac0e9265.jpg) no-repeat center center / 100% 100%;
	display: flex;
	width: 100%;
	min-height: 100vh;
	justify-content: flex-end;
	align-items: center;
	position: relative !important;
	.rgs-form {
		.rgs-form2 {
		padding: 0 40px;
		margin: auto;
		align-content: center;
		background: none;
		display: flex;
		width: 100%;
		align-items: center;
		flex-wrap: wrap;
		}
		border-radius: 10px;
		padding: 75px 35px;
		margin: 0 208px 0 0;
		z-index: 1;
		background: url(http://codegen.caihongy.cn/20250914/6f34c6f3174d4e8184c0f041a4bfafaa.png) no-repeat  center center / 100% 100%;
		width: 723px;
		.title {
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
			width: 100%;
			/deep/ .el-form-item__content {
				display: block;
			}
			.el-input {
				width: 100%;
			}
			.el-input /deep/ .el-input__inner {
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
			.el-input /deep/ .el-input__inner:focus {
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
			.el-input-number {
				width: 100%;
			}
			.el-input-number /deep/ .el-input__inner {
				text-align: center;
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
			.el-input-number /deep/ .el-input__inner:focus {
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
			.el-input-number /deep/ .el-input-number__decrease {
				display: none;
			}
			.el-input-number /deep/ .el-input-number__increase {
				display: none;
			}
			.el-select {
				width: 100%;
			}
			.el-select /deep/ .el-input__inner {
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
			.el-select /deep/ .el-input__inner:focus {
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
			.el-date-editor {
				width: 100%;
			}
			.el-date-editor /deep/ .el-input__inner {
				border: 1px solid #DADFE6;
				border-radius: 4px;
				padding: 0 30px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #333;
				background: #fff;
				flex: 1;
				width: 100%;
				font-size: 16px;
				height: 64px;
			}
			.el-date-editor /deep/ .el-input__inner:focus {
				border: 1px solid #DADFE6;
				border-radius: 4px;
				padding: 0 30px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #333;
				background: #fff;
				flex: 1;
				width: 100%;
				font-size: 16px;
				height: 64px;
			}
			.el-date-editor.el-input {
				width: 100%;
			}
			/deep/ .el-upload--picture-card {
				background: transparent;
				border: 0;
				border-radius: 0;
				width: auto;
				height: auto;
				line-height: initial;
				vertical-align: middle;
			}
			/deep/ .upload .upload-img {
				border: 1px solid #ddd;
				cursor: pointer;
				border-radius: 4px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				margin: 5px 0 0;
				color: #999;
				background: #fff;
				width: 90px;
				font-size: 26px;
				line-height: 64px;
				text-align: center;
				height: 64px;
			}
			/deep/ .el-upload-list .el-upload-list__item {
				border: 1px solid #ddd;
				cursor: pointer;
				border-radius: 4px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				margin: 5px 0 0;
				color: #999;
				background: #fff;
				width: 90px;
				font-size: 26px;
				line-height: 64px;
				text-align: center;
				height: 64px;
			}
			/deep/ .el-upload .el-icon-plus {
				border: 1px solid #ddd;
				cursor: pointer;
				border-radius: 4px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				margin: 5px 0 0;
				color: #999;
				background: #fff;
				width: 90px;
				font-size: 26px;
				line-height: 64px;
				text-align: center;
				height: 64px;
			}
			/deep/ .el-upload__tip {
				margin: 0;
				color: #666;
				font-size: 16px;
			}
			/deep/ .el-input__inner::placeholder {
				color: #123;
				font-size: 16px;
			}
			.required {
				position: relative;
			}
			.required::after{
				color: red;
				left: 120px;
				position: absolute;
				content: "*";
			}
			.editor {
				border: 1px solid #DADFE6;
				border-radius: 4px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				background: #fff;
				width: 100%;
				min-width: 100%;
				height: auto;
			}
			.editor>.avatar-uploader {
				line-height: 0;
				height: 0;
			}
		}
		.list-item.email {
			input {
				border-radius: 4px 0 0 4px;
				padding: 0 10px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #333;
				background: #fff;
				width: 100%;
				font-size: 16px;
				border-color: #eee;
				border-width: 0 0 1px;
				border-style: solid;
				height: 64px;
			}
			input:focus {
				border-radius: 4px 0 0 4px;
				padding: 0 10px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #333;
				background: #fff;
				width: 100%;
				font-size: 16px;
				border-color: #eee;
				border-width: 0 0 1px;
				border-style: solid;
				height: 48px;
			}
			input::placeholder {
				color: #123;
				font-size: 16px;
			}
			button {
				cursor: pointer;
				border-radius: 0 4px 4px   0px ;
				color: #fff;
				background: linear-gradient( 135deg, #087FF3 0%, #32B2F3 100%);
				display: flex;
				width: 180px;
				border-color: #acacac;
				border-width: 0;
				justify-content: center;
				align-items: center;
				border-style: solid;
				height: 64px;
			}
			button:hover {
				opacity: 1;
			}
		}
		.register-btn {
			padding: 0;
			display: flex;
			width: 100%;
			justify-content: center;
			flex-wrap: wrap;
		}
		.register-btn1 {
			padding: 0;
			margin: 0 50px 0 0;
			width: 100%;
			text-align: center;
		}
		.register-btn2 {
			padding: 0;
			margin: 0;
			width: 100%;
		}
		.r-btn {
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
		.r-btn:hover {
			opacity: 0.5;
		}
		.r-login {
			cursor: pointer;
			border-radius: 4px;
			margin: 10px auto;
			outline: none;
			color: #0D1818;
			font-weight: bold;
			width: 100%;
			font-size: 16px;
			line-height: 47px;
			text-align: center;
			height: 47px;
		}
		.r-login:hover {
			opacity: 0.8;
		}
	}
}
	
	::-webkit-scrollbar {
	  display: none;
	}
</style>
