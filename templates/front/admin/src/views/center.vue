<template>
	<div :style='{"padding":" 30px","background":"#DCEAF7","height":"100vh"}'>
		<el-form
			:style='{"border":" 1px solid #FFFFFF","padding":"30px","margin":"0","borderRadius":"24px","flexWrap":"wrap","background":"#F0F5FB","display":"flex","width":"100%"}'
			class="add-update-preview"
			ref="ruleForm"
			:model="ruleForm"
			label-width="180px"
		>
				<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}'   v-if="flag=='yonghu'"  label="用户账号" prop="yonghuzhanghao">
					<el-input v-model="ruleForm.yonghuzhanghao" :readonly="ro.yonghuzhanghao" placeholder="用户账号" clearable></el-input>
				</el-form-item>
				<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}'   v-if="flag=='yonghu'"  label="用户姓名" prop="yonghuxingming">
					<el-input v-model="ruleForm.yonghuxingming" :readonly="ro.yonghuxingming" placeholder="用户姓名" clearable></el-input>
				</el-form-item>
				<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}' v-if="flag=='yonghu'" label="头像" prop="touxiang">
					<file-upload
						tip="点击上传头像"
						action="file/upload"
						:limit="1"
						:multiple="false"
						:fileUrls="ruleForm.touxiang?ruleForm.touxiang:''"
						@change="yonghutouxiangUploadChange"
					></file-upload>
				</el-form-item>
				<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}' v-if="flag=='yonghu'"  label="性别" prop="xingbie">
					<el-select filterable v-model="ruleForm.xingbie" :disabled="ro.xingbie" placeholder="请选择性别">
						<el-option
							v-for="(item,index) in yonghuxingbieOptions"
							v-bind:key="index"
							:label="item"
							:value="item">
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}'   v-if="flag=='yonghu'"  label="手机号" prop="mobile">
					<el-input v-model="ruleForm.mobile" :readonly="ro.mobile" placeholder="手机号" clearable></el-input>
				</el-form-item>
				<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}' v-if="flag=='users'" label="用户名" prop="username">
					<el-input v-model="ruleForm.username" placeholder="用户名"></el-input>
				</el-form-item>
				<el-form-item :style='{"width":"calc(50% - 0px)","margin":"0 0 15px 0 ","display":"flex"}' v-if="flag=='users'" label="头像" prop="image">
					<file-upload
						tip="点击上传头像"
						action="file/upload"
						:limit="1"
						:multiple="false"
						:fileUrls="ruleForm.image?ruleForm.image:''"
						@change="usersimageUploadChange"
					></file-upload>
				</el-form-item>
				<el-form-item :style='{"padding":"0","margin":"10px 0 10px 180px","flexWrap":"wrap","background":"none","display":"flex","width":"auto","justifyContent":"center"}'>
					<el-button class="btn3" type="primary" @click="onUpdateHandler">
						<span class="icon iconfont icon-queren15"></span>
						提交
					</el-button>
				</el-form-item>
		</el-form>
	</div>
</template>
<script>
// 校验引入
	import { 
		isIntNumer,
		isMobile,
	} from "@/utils/validate";

	export default {
		data() {
			return {
				ruleForm: {},
				ro: {},
				flag: '',
				usersFlag: false,
				yonghuxingbieOptions: [],
			};
		},
		mounted() {
			var table = this.$storage.get("sessionTable");
			this.flag = table;
			this.$http({
				url: `${this.$storage.get("sessionTable")}/session`,
				method: "get"
			}).then(({ data }) => {
				if (data && data.code === 0) {
					if(table == 'yonghu') {
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

					this.ruleForm = data.data;
				} else {
					this.$message.error(data.msg);
				}
			});
			this.yonghuxingbieOptions = "男,女".split(',')
		},
		methods: {
			yonghutouxiangUploadChange(fileUrls) {
				this.ruleForm.touxiang = fileUrls;
			},
			usersimageUploadChange(fileUrls) {
				this.ruleForm.image = fileUrls;
			},
			onUpdateHandler() {
				if((!this.ruleForm.yonghuzhanghao)&& 'yonghu'==this.flag){
					this.$message.error('用户账号不能为空');
					return
				}
				if((!this.ruleForm.mima)&& 'yonghu'==this.flag){
					this.$message.error('密码不能为空');
					return
				}
				if((!this.ruleForm.yonghuxingming)&& 'yonghu'==this.flag){
					this.$message.error('用户姓名不能为空');
					return
				}
				if(this.ruleForm.touxiang!=null) {
					this.ruleForm.touxiang = this.ruleForm.touxiang.replace(new RegExp(this.$base.url,"g"),"");
				}
				if('yonghu' ==this.flag && this.ruleForm.mobile&&(!isMobile(this.ruleForm.mobile))){
					this.$message.error(`手机号应输入手机格式`);
					return
				}
				if('yonghu' ==this.flag && this.ruleForm.status&&(!isIntNumer(this.ruleForm.status))){
					this.$message.error(`状态应输入整数`);
					return
				}
				if('users'==this.flag && this.ruleForm.username.trim().length<1) {
					this.$message.error(`用户名不能为空`);
					return	
				}
				if(this.flag=='users'){
					this.ruleForm.image = this.ruleForm.image.replace(new RegExp(this.$base.url,"g"),"")
				}
				this.$http({
					url: `${this.$storage.get("sessionTable")}/update`,
					method: "post",
					data: this.ruleForm
				}).then(({ data }) => {
					if (data && data.code === 0) {
						if(this.flag=='users'){
							this.$storage.set('headportrait',this.ruleForm.image)
						}else {
							if(this.flag == 'yonghu') {
								this.$storage.set('headportrait',this.ruleForm.touxiang)
							}
						}
						this.$message({
							message: "修改信息成功",
							type: "success",
							duration: 1500,
							onClose: () => {
								window.location.reload();
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
	.el-date-editor.el-input {
		width: auto;
	}
	
	.add-update-preview .el-form-item /deep/ .el-form-item__label {
				padding: 0 10px;
				color: #333333;
				white-space: nowrap;
				background: none;
				font-weight: 600;
				width: 180px;
				font-size: 16px;
				line-height: 64px;
				text-align: right;
				height: 64px;
			}
	
	.add-update-preview .el-form-item /deep/ .el-form-item__content {
		margin-left: auto !important;
		margin: auto !important;
		flex: 1;
		display: flex;
		width: 100%;
		justify-content: flex-start;
		align-items: flex-start;
		flex-wrap: wrap;
	}
	
	.add-update-preview .el-input /deep/ .el-input__inner {
				border:  1px solid #DADFE6;
				border-radius: 4px;
				padding: 0 12px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				outline: none;
				color: #333;
				background: #FFFFFF;
				flex: 1;
				width: 100%;
				font-size: 16px;
				height: 64px;
			}
	
	.add-update-preview .el-select /deep/ .el-input__inner {
				border:  1px solid #DADFE6;
				border-radius: 4px;
				padding: 0 12px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				outline: none;
				color: #333;
				background: #FFFFFF;
				flex: 1;
				width: 100%;
				font-size: 16px;
				height: 64px;
			}
	
	.add-update-preview .el-date-editor /deep/ .el-input__inner {
				border:  1px solid #DADFE6;
				border-radius: 4px;
				padding: 0 30px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				outline: none;
				color: #333;
				background: #FFFFFF;
				flex: 1;
				width: 100%;
				font-size: 16px;
				height: 64px;
			}
	
	.add-update-preview /deep/ .el-upload--picture-card {
		background: transparent;
		border: 0;
		border-radius: 0;
		width: auto;
		height: auto;
		line-height: initial;
		vertical-align: middle;
	}
	
	.add-update-preview /deep/ .el-upload-list .el-upload-list__item {
				border: 1px solid #DADFE6;
				cursor: pointer;
				border-radius: 4px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #999;
				background: #fff;
				font-weight: 600;
				width: 80px;
				font-size: 30px;
				line-height: 80px;
				text-align: center;
				height: 80px;
			}
	
	.add-update-preview /deep/ .el-upload .el-icon-plus {
				border: 1px solid #DADFE6;
				cursor: pointer;
				border-radius: 4px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				color: #999;
				background: #fff;
				font-weight: 600;
				width: 80px;
				font-size: 30px;
				line-height: 80px;
				text-align: center;
				height: 80px;
			}
	
	.add-update-preview .el-textarea /deep/ .el-textarea__inner {
				border-radius: 4px;
				padding: 12px;
				box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
				outline: none;
				color: #666;
				background: #fff;
				width: 100%;
				font-size: 16px;
				border-color: #e8e9eb;
				border-width: 1px;
				border-style: solid;
				height: auto;
			}
	
	.add-update-preview .btn3 {
				border: 1px solid #B2F9F0;
				cursor: pointer;
				padding: 0 24px;
				margin: 10px 10px 0 0;
				color: #fff;
				font-weight: bold;
				font-size: 16px;
				border-radius: 24px  ;
				box-shadow: inset 0px -6px 6px 1px #3EE3F9;
				outline: none;
				background:  linear-gradient( 135deg, #087FF3 0%, #32B2F3 100%);
				width: auto;
				min-width: 175px;
				height: 47px;
				.iconfont {
						margin: 0 2px;
						color: #fff;
						display: none;
						font-size: 16px;
						height: 40px;
					}
	}
	
	.add-update-preview .btn3:hover {
				opacity: 0.8;
			}
	.editor>.avatar-uploader {
		line-height: 0;
		height: 0;
	}
</style>
