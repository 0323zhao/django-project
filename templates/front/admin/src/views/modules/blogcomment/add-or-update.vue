






















<template>
	<div class="addEdit-block">
		<el-form
			class="add-update-preview"
			ref="ruleForm"
			:model="ruleForm"
			:rules="rules"
			label-width="180px"
		>
			<template >
				<el-form-item class="input" v-if="type!='info'"  label="评论人" prop="pluser" >
					<el-input v-model="ruleForm.pluser" placeholder="评论人" clearable  :readonly="ro.pluser"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="评论人" prop="pluser" >
					<el-input v-model="ruleForm.pluser" placeholder="评论人" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="支持数" prop="likecount" >
					<el-input v-model.number="ruleForm.likecount" placeholder="支持数" clearable  :readonly="ro.likecount"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="支持数" prop="likecount" >
					<el-input v-model="ruleForm.likecount" placeholder="支持数" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="发布地" prop="fbplace" >
					<el-input v-model="ruleForm.fbplace" placeholder="发布地" clearable  :readonly="ro.fbplace"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="发布地" prop="fbplace" >
					<el-input v-model="ruleForm.fbplace" placeholder="发布地" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="评论时间" prop="pltime" >
					<el-input v-model="ruleForm.pltime" placeholder="评论时间" clearable  :readonly="ro.pltime"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="评论时间" prop="pltime" >
					<el-input v-model="ruleForm.pltime" placeholder="评论时间" readonly></el-input>
				</el-form-item>
			</template>
			<el-form-item class="textarea" v-if="type!='info'" label="详情地址" prop="detailurl" >
				<el-input
					style="min-width: 200px; max-width: 600px;"
					type="textarea"
					:rows="8"
					placeholder="详情地址"
					v-model="ruleForm.detailurl" >
				</el-input>
			</el-form-item>
			<el-form-item v-else-if="ruleForm.detailurl" label="详情地址" prop="detailurl"  class="textBox">
				<span class="text">{{ruleForm.detailurl}}</span>
			</el-form-item>
			<el-form-item class="textarea" v-if="type!='info'" label="评论内容" prop="plcontent" >
				<el-input
					style="min-width: 200px; max-width: 600px;"
					type="textarea"
					:rows="8"
					placeholder="评论内容"
					v-model="ruleForm.plcontent" >
				</el-input>
			</el-form-item>
			<el-form-item v-else-if="ruleForm.plcontent" label="评论内容" prop="plcontent"  class="textBox">
				<span class="text">{{ruleForm.plcontent}}</span>
			</el-form-item>
			<el-form-item class="btn">
				<el-button class="btn3"  v-if="type!='info'" type="success" @click="onSubmit">
					<span class="icon iconfont icon-queren15"></span>
					提交
				</el-button>
				<el-button class="btn4" v-if="type!='info'" type="success" @click="back()">
					<span class="icon iconfont icon-guanbi2"></span>
					取消
				</el-button>
				<el-button class="btn5" v-if="type=='info'" type="success" @click="back()">
					<span class="icon iconfont icon-fanhui13"></span>
					返回
				</el-button>
			</el-form-item>
		</el-form>
    

	</div>
</template>
<script>
	import { 
		isIntNumer,
		isURL,
	} from "@/utils/validate";
	export default {
		data() {
			var validateUrl = (rule, value, callback) => {
				if(!value){
					callback();
				} else if (!isURL(value)) {
					callback(new Error("请输入正确的URL地址"));
				} else {
					callback();
				}
			};
			var validateIntNumber = (rule, value, callback) => {
				if(!value){
					callback();
				} else if (!isIntNumer(value)) {
					callback(new Error("请输入整数"));
				} else {
					callback();
				}
			};
			return {
				id: '',
				type: '',
			
			
				ro:{
					detailurl : false,
					pluser : false,
					plcontent : false,
					likecount : false,
					fbplace : false,
					pltime : false,
					thumbsupnum : false,
					crazilynum : false,
					clicknum : false,
					discussnum : false,
					storeupnum : false,
				},
			
				ruleForm: {
					detailurl: '',
					pluser: '',
					plcontent: '',
					likecount: '',
					fbplace: '',
					pltime: '',
					thumbsupnum: Number('0'),
					crazilynum: Number('0'),
					clicknum: Number('0'),
					discussnum: Number('0'),
					storeupnum: Number('0'),
				},

				rules: {
					detailurl: [
						{ validator: validateUrl, trigger: 'blur' },
					],
					pluser: [
					],
					plcontent: [
					],
					likecount: [
						{ validator: validateIntNumber, trigger: 'blur' },
					],
					fbplace: [
					],
					pltime: [
					],
					thumbsupnum: [
						{ validator: validateIntNumber, trigger: 'blur' },
					],
					crazilynum: [
						{ validator: validateIntNumber, trigger: 'blur' },
					],
					clicknum: [
						{ validator: validateIntNumber, trigger: 'blur' },
					],
					discussnum: [
						{ validator: validateIntNumber, trigger: 'blur' },
					],
					storeupnum: [
						{ validator: validateIntNumber, trigger: 'blur' },
					],
				},
			};
		},
		props: ["parent"],
		computed: {
			sessionForm() {
				return JSON.parse(this.$storage.getObj('userForm'))
			},
			sessionTable() {
				return this.$storage.get('sessionTable')
			},



		},
		components: {
		},
		created() {
		},
		methods: {
			imgPreView(url){
				this.$parent.imgPreView(url)
			},
			// 下载
			download(file){
				window.open(`${file}`)
			},
			// 初始化
			init(id,type ) {
				if (id) {
					this.id = id;
					this.type = type;
				}
				if(this.type=='info'||this.type=='else'||this.type=='msg'){
					this.info(id);
				}else if(this.type=='logistics'){
					for(let x in this.ro) {
						this.ro[x] = true
					}
					this.logistics=false;
					this.info(id);
				}else if(this.type=='cross'){
					var obj = this.$storage.getObj('crossObj');
					for (var o in obj){
						if(o=='detailurl'){
							this.ruleForm.detailurl = obj[o];
							this.ro.detailurl = true;
							continue;
						}
						if(o=='pluser'){
							this.ruleForm.pluser = obj[o];
							this.ro.pluser = true;
							continue;
						}
						if(o=='plcontent'){
							this.ruleForm.plcontent = obj[o];
							this.ro.plcontent = true;
							continue;
						}
						if(o=='likecount'){
							this.ruleForm.likecount = obj[o];
							this.ro.likecount = true;
							continue;
						}
						if(o=='fbplace'){
							this.ruleForm.fbplace = obj[o];
							this.ro.fbplace = true;
							continue;
						}
						if(o=='pltime'){
							this.ruleForm.pltime = obj[o];
							this.ro.pltime = true;
							continue;
						}
						if(o=='thumbsupnum'){
							this.ruleForm.thumbsupnum = obj[o];
							this.ro.thumbsupnum = true;
							continue;
						}
						if(o=='crazilynum'){
							this.ruleForm.crazilynum = obj[o];
							this.ro.crazilynum = true;
							continue;
						}
						if(o=='clicknum'){
							this.ruleForm.clicknum = obj[o];
							this.ro.clicknum = true;
							continue;
						}
						if(o=='discussnum'){
							this.ruleForm.discussnum = obj[o];
							this.ro.discussnum = true;
							continue;
						}
						if(o=='storeupnum'){
							this.ruleForm.storeupnum = obj[o];
							this.ro.storeupnum = true;
							continue;
						}
					}
				}

			
			},
			// 多级联动参数

			async info(id) {
				await this.$http({
					url: `blogcomment/info/${id}`,
					method: "get"
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.ruleForm = data.data;
						//解决前台上传图片后台不显示的问题
						let reg=new RegExp('../../../upload','g')//g代表全部
					} else {
						this.$message.error(data.msg);
					}
				});
			},

			// 提交
			async onSubmit() {
					var objcross = this.$storage.getObj('crossObj');
					if(!this.ruleForm.id) {
						delete this.ruleForm.userid
					}
					await this.$refs["ruleForm"].validate(async valid => {
						if (valid) {
							if(this.type=='cross'){
								var statusColumnName = this.$storage.get('statusColumnName');
								var statusColumnValue = this.$storage.get('statusColumnValue');
								if(statusColumnName!='') {
									var obj = this.$storage.getObj('crossObj');
									if(statusColumnName && !statusColumnName.startsWith("[")) {
										for (var o in obj){
											if(o==statusColumnName){
												obj[o] = statusColumnValue;
											}
										}
										var table = this.$storage.get('crossTable');
										await this.$http({
											url: `${table}/update`,
											method: "post",
											data: obj
										}).then(({ data }) => {});
									}
								}
							}
							await this.$http({
								url: `blogcomment/${!this.ruleForm.id ? "save" : "update"}`,
								method: "post",
								data: this.ruleForm
							}).then(async ({ data }) => {
								if (data && data.code === 0) {
									this.$message({
										message: "操作成功",
										type: "success",
										duration: 1500,
										onClose: () => {
											this.parent.showFlag = true;
											this.parent.addOrUpdateFlag = false;
											this.parent.blogcommentCrossAddOrUpdateFlag = false;
											this.parent.search();
										}
									});
								} else {
									this.$message.error(data.msg);
								}
							});
						}
					});
			},
			// 获取uuid
			getUUID () {
				return new Date().getTime();
			},
			// 返回
			back() {
				this.parent.showFlag = true;
				this.parent.addOrUpdateFlag = false;
				this.parent.blogcommentCrossAddOrUpdateFlag = false;
			},
		}
	};
</script>
<style lang="scss" scoped>
	.addEdit-block {
		padding: 30px 30px 30px 30px;
		background: #DCEAF7;
		width: 100%;
	}
	.add-update-preview {
		border:  1px solid #FFFFFF;
		border-radius: 24px;
		padding: 30px;
		margin: 0;
		background: #F0F5FB;
		display: flex;
		width: 100%;
		flex-wrap: wrap;
	}
	.amap-wrapper {
		width: 100%;
		height: 500px;
	}
	
	.search-box {
		position: absolute;
	}
	
	.el-date-editor.el-input {
		width: auto;
	}
	.add-update-preview /deep/ .el-form-item {
		margin: 0 0 15px 0 ;
		display: flex;
		width: calc(50% - 0px);
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
	.add-update-preview /deep/ .el-form-item.editorBox {
		margin: 0 0 15px 0 ;
		display: flex;
		width: 100%;
	}
	.add-update-preview .el-form-item.editorBox /deep/ .el-form-item__label {
		padding: 0 10px;
		color: #333333;
		white-space: nowrap;
		font-weight: 600;
		width: 180px;
		font-size: 16px;
		line-height: 64px;
		text-align: right;
		height: 64px;
	}
	
	.add-update-preview .el-form-item.editorBox /deep/ .el-form-item__content {
		margin-left: auto !important;
		padding: 0;
		margin: auto !important;
		flex: 1;
		display: flex;
		width: 100%;
		justify-content: flex-start;
		align-items: flex-start;
		flex-wrap: wrap;
	}
	.add-update-preview /deep/.el-form-item.editorBox .editor {
		border-radius: 4px;
		box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
		max-width: 100% !important;
		align-content: flex-start;
		flex: 1;
		background: #fff;
		display: flex;
		align-items: flex-start;
		flex-wrap: wrap;
		height: auto;
	}
	.add-update-preview /deep/.el-form-item.editorBox .editor .ql-toolbar {
		background: none;
		width: 100%;
	}
	.add-update-preview /deep/.el-form-item.editorBox .editor .ql-container {
		background: none;
		width: 100%;
		min-height: 200px;
	}
	.add-update-preview /deep/.el-form-item.editorBox .editor .ql-container .ql-blank::before {
		color: #999;
	}
	
	.add-update-preview /deep/ .el-form-item.textBox {
		margin: 0 0 15px 0 ;
		display: flex;
		width: calc(100% - 0px);
	}
	.add-update-preview .el-form-item.textBox /deep/ .el-form-item__label {
		padding: 0 10px;
		color: #333333;
		white-space: nowrap;
		font-weight: 500;
		width: 180px;
		font-size: 16px;
		line-height: 64px;
		text-align: right;
		height: 64px;
	}
	
	.add-update-preview .el-form-item.textBox /deep/ .el-form-item__content {
		margin-left: auto !important;
		padding: 0;
		margin: auto !important;
		flex: 1;
		display: flex;
		width: 100%;
		justify-content: flex-start;
		align-items: flex-start;
		flex-wrap: wrap;
	}
	.add-update-preview /deep/.el-form-item.textBox span.text {
		border: 1px solid #DADFE6;
		border-radius: 4px;
		padding: 12px 12px;
		box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
		outline: none;
		color: #333;
		background: #fff;
		flex: 1;
		width: 100%;
		font-size: 16px;
		line-height: 30px;
		height: auto;
	}
	
	.add-update-preview .el-input {
		flex: 1;
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
	.add-update-preview .el-input /deep/ .el-input__inner[readonly="readonly"] {
		border: 0px solid #DADFE6;
		border-radius: 4px;
		padding: 0 12px;
		box-shadow: none;
		outline: none;
		color: #666;
		background: none;
		flex: 1;
		width: 100%;
		font-size: 16px;
		height: 64px;
	}
	.add-update-preview .el-input-number {
		text-align: left;
		flex: 1;
	}
	.add-update-preview .el-input-number /deep/ .el-input__inner {
		text-align: left;
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
	.add-update-preview .el-input-number /deep/ .is-disabled .el-input__inner {
		text-align: left;
		border: 0px solid #DADFE6;
		border-radius: 4px;
		padding: 0 12px;
		box-shadow: none;
		outline: none;
		color: #666;
		background: none;
		flex: 1;
		width: 100%;
		font-size: 16px;
		height: 64px;
	}
	.add-update-preview .el-input-number /deep/ .el-input-number__decrease {
		display: none;
	}
	.add-update-preview .el-input-number /deep/ .el-input-number__increase {
		display: none;
	}
	.add-update-preview .el-select {
		width: auto;
		min-width: 100%;
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
	.add-update-preview .el-select /deep/ .is-disabled .el-input__inner {
		border: 0px solid #DADFE6;
		border-radius: 4px;
		padding: 0 12px;
		box-shadow: none;
		outline: none;
		color: #666;
		background: none;
		flex: 1;
		width: 100%;
		font-size: 16px;
		height: 64px;
	}
	.add-update-preview .el-date-editor {
		width: auto;
		min-width: 100%;
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
	.add-update-preview .el-date-editor /deep/ .el-input__inner[readonly="readonly"] {
		border: 0px solid #DADFE6;
		border-radius: 4px;
		padding: 0 30px;
		box-shadow: none;
		outline: none;
		color: #333;
		background: none;
		flex: 1;
		width: 100%;
		font-size: 16px;
		height: 64px;
	}
	.add-update-preview .viewBtn {
		border: 1px solid #B2F9F0;
		border-radius: 4px;
		padding: 0 20px;
		box-shadow:  inset 0px -6px 6px 1px #3EE3F9;
		outline: none;
		color: #FFFFFF;
		background: linear-gradient( 135deg, #087FF3 0%, #32B2F3 100%);
		font-weight: bold;
		width: auto;
		font-size: 16px;
		min-width: 120px;
		height: 48px;
		.iconfont {
			margin: 0 2px;
			color: #fff;
			display: none;
			font-size: 14px;
			height: 40px;
		}
	}
	.add-update-preview .viewBtn:hover {
		opacity: 0.8;
	}
	.add-update-preview .downBtn {
		border: 1px solid #B2F9F0;
		border-radius: 4px;
		padding: 0 20px;
		box-shadow:  inset 0px -6px 6px 1px #3EE3F9;
		outline: none;
		color: #FFFFFF;
		background: linear-gradient( 135deg, #087FF3 0%, #32B2F3 100%);
		font-weight: bold;
		width: auto;
		font-size: 16px;
		min-width: 120px;
		height: 48px;
		.iconfont {
			margin: 0 2px;
			color: #fff;
			display: none;
			font-size: 14px;
			height: 40px;
		}
	}
	.add-update-preview .downBtn:hover {
		opacity: 0.8;
	}
	.add-update-preview .unBtn {
		border: 1px solid #B2F9F0;
		border-radius: 4px;
		padding: 0 20px;
		box-shadow:  inset 0px -6px 6px 1px #3EE3F9;
		outline: none;
		color: #FFFFFF;
		background: linear-gradient( 135deg, #087FF3 0%, #32B2F3 100%);
		font-weight: bold;
		width: auto;
		font-size: 16px;
		min-width: 120px;
		height: 48px;
		.iconfont {
			margin: 0 2px;
			color: #fff;
			display: none;
			font-size: 14px;
			height: 40px;
		}
	}
	.add-update-preview .unBtn:hover {
		opacity: 0.8;
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
	
	.add-update-preview /deep/ .upload .upload-img {
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
	.add-update-preview /deep/ .el-upload__tip {
		padding: 0 10px;
		color: #666;
		font-size: 15px;
	}
	.add-update-preview /deep/ .el-form-item.fileupload {
		margin: 0 0 15px 0 ;
		display: flex;
		width: calc(50% - 0px);
	}
	.add-update-preview .el-form-item.fileupload /deep/ .el-form-item__label {
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
	
	.add-update-preview .el-form-item.fileupload /deep/ .el-form-item__content {
		margin-left: auto !important;
		margin: auto !important;
		flex: 1;
		display: flex;
		width: 100%;
		justify-content: flex-start;
		align-items: flex-start;
		flex-wrap: wrap;
	}
	.add-update-preview .el-form-item.fileupload /deep/ .el-upload-dragger {
		border-radius: 4px;
		padding: 0px 22px;
		box-shadow: inset 0px 3px 6px 1px rgba(0,0,0,0.16);
		outline: none;
		color: #333;
		background: #fff;
		width: 100%;
		font-size: 24px;
		border-color: #e8e9eb;
		border-width: 1px;
		border-style: solid;
		height: auto;
	}
	.add-update-preview .el-form-item.fileupload .el-upload-dragger /deep/ .el-icon-upload {
		padding: 0;
		margin: 10px 0 0;
		color: #f3a213;
		font-size: 62px;
		line-height: 1;
	}
	.add-update-preview .el-form-item.fileupload .el-upload-dragger /deep/ .el-upload__text {
		padding: 0;
		margin: 0 0 20px;
		color: #606266;
		line-height: 1;
	}
	.add-update-preview .el-form-item.fileupload .el-upload-dragger /deep/ .el-upload__text em {
		color: #409EFF;
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
	.add-update-preview .el-textarea /deep/ .el-textarea__inner[readonly="readonly"] {
		border-radius: 4px;
		padding: 20px 12px 12px;
		box-shadow: none;
		outline: none;
		color: #666;
		background: none;
		width: 100%;
		font-size: 16px;
		border-color: #e8e9eb;
		border-width: 0px;
		border-style: solid;
		height: auto;
	}
	.add-update-preview /deep/ .el-form-item.btn {
		padding: 0;
		margin: 10px 0 10px 180px;
		background: none;
		display: flex;
		width: auto;
		justify-content: center;
		flex-wrap: wrap;
		.btn1 {
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
		.btn1:hover {
			opacity: 0.8;
		}
		.btn2 {
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
		.btn2:hover {
			opacity: 0.8;
		}
		.btn3 {
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
		.btn3:hover {
			opacity: 0.8;
		}
		.btn4 {
			border: 1px solid #B2F9F0;
			cursor: pointer;
			padding: 0 24px;
			margin: 10px 10px 0 0;
			color: #fff;
			font-weight: bold;
			font-size: 16px;
			border-radius: 24px  ;
			outline: none;
			background: #216CF6;
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
		.btn4:hover {
			opacity: 0.8;
		}
		.btn5 {
			border: 1px solid #B2F9F0;
			cursor: pointer;
			padding: 0 24px;
			margin: 10px 10px 0 0;
			color: #fff;
			font-weight: bold;
			font-size: 16px;
			border-radius: 24px  ;
			outline: none;
			background: #216CF6;
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
		.btn5:hover {
			opacity: 0.8;
		}
	}
	.add-update-preview .el-form-item.btn /deep/ .el-form-item__label {
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
	
	.add-update-preview .el-form-item.btn /deep/ .el-form-item__content {
	}
</style>
