
























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
				<el-form-item class="input" v-if="type!='info'"  label="用户名" prop="username" >
					<el-input v-model="ruleForm.username" placeholder="用户名" clearable  :readonly="ro.username"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="用户名" prop="username" >
					<el-input v-model="ruleForm.username" placeholder="用户名" readonly></el-input>
				</el-form-item>
				<el-form-item class="select" v-if="type!='info'"  label="状态" prop="isdone" >
					<el-select :disabled="ro.isdone" v-model="ruleForm.isdone" placeholder="请选择状态"  filterable>
						<el-option
							v-for="(item,index) in isdoneOptions"
							v-bind:key="index"
							:label="item"
							:value="item">
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item v-else class="input" label="状态" prop="isdone" >
					<el-input v-model="ruleForm.isdone"
						placeholder="状态" readonly></el-input>
				</el-form-item>
				<el-form-item class="date" v-if="type!='info'" label="置顶时间" prop="toptime" >
					<el-date-picker
						value-format="yyyy-MM-dd HH:mm:ss"
						v-model="ruleForm.toptime" 
						type="datetime"
						:readonly="ro.toptime"
						placeholder="置顶时间"
					></el-date-picker>
				</el-form-item>
				<el-form-item class="input" v-else-if="ruleForm.toptime" label="置顶时间" prop="toptime" >
					<el-input v-model="ruleForm.toptime" placeholder="置顶时间" readonly></el-input>
				</el-form-item>
				<el-form-item class="upload" v-if="type!='info' && !ro.cover" label="封面" prop="cover" >
					<file-upload
						tip="点击上传封面"
						action="file/upload"
						:limit="3"
						:disabled="ro.cover"
						:multiple="true"
						:fileUrls="ruleForm.cover?ruleForm.cover:''"
						@change="coverUploadChange"
					></file-upload>
				</el-form-item>
				<el-form-item class="upload" v-else-if="ruleForm.cover" label="封面" prop="cover" >
					<img v-if="ruleForm.cover.substring(0,4)=='http'&&ruleForm.cover.split(',w').length>1" class="upload-img" style="margin-right:20px;" v-bind:key="index" :src="ruleForm.cover" width="100" height="100" @click="imgPreView(ruleForm.tupian)">
					<img v-else-if="ruleForm.cover.substring(0,4)=='http'" class="upload-img" style="margin-right:20px;" v-bind:key="index" :src="ruleForm.cover.split(',')[0]" width="100" height="100" @click="imgPreView(ruleForm.tupian.split(',')[0])">
					<img v-else class="upload-img" style="margin-right:20px;" v-bind:key="index" v-for="(item,index) in ruleForm.cover.split(',')" :src="$base.url+item" width="100" height="100" @click="imgPreView($base.url+item)">
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="是否匿名" prop="isanon">
					<el-select v-model="ruleForm.isanon" placeholder="是否匿名">
						<el-option label="是" :value="1"></el-option>
						<el-option label="否" :value="0"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item v-else class="input" label="是否匿名" prop="isanon" >
					{{ruleForm.isanon==1?'是':'否'}}
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="是否删除" prop="delflag">
					<el-select v-model="ruleForm.delflag" placeholder="是否删除">
						<el-option label="是" :value="1"></el-option>
						<el-option label="否" :value="0"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item v-else class="input" label="是否删除" prop="delflag" >
					{{ruleForm.delflag==1?'是':'否'}}
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="帖子标题" prop="title" >
					<el-input v-model="ruleForm.title" placeholder="帖子标题" clearable  :readonly="ro.title"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="帖子标题" prop="title" >
					<el-input v-model="ruleForm.title" placeholder="帖子标题" readonly></el-input>
				</el-form-item>
			</template>
			<el-form-item v-if="type!='info'" class="editorBox" label="帖子内容" prop="content" >
				<editor 
					style="min-width: 200px; max-width: 600px;"
					v-model="ruleForm.content" 
					class="editor"
					myQuillEditor="content"
					action="file/upload">
				</editor>
			</el-form-item>
			<el-form-item v-else-if="ruleForm.content" label="帖子内容" prop="content"  class="textBox">
				<span class="text ql-snow ql-editor" v-html="ruleForm.content"></span>
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
	} from "@/utils/validate";
	export default {
		data() {
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
					content : false,
					parentid : false,
					username : false,
					avatarurl : false,
					isdone : false,
					istop : false,
					toptime : false,
					cover : false,
					isanon : false,
					delflag : false,
					title : false,
					userid : false,
				},
			
				ruleForm: {
					content: '',
					parentid: '',
					username: '',
					avatarurl: '',
					isdone: '',
					istop: Number('0'),
					toptime: '',
					cover: '',
					isanon: Number('0'),
					delflag: Number('0'),
					title: '',
					userid: '',
				},
				isdoneOptions: [],

				rules: {
					content: [
						{ required: true, message: '帖子内容不能为空', trigger: 'blur' },
					],
					parentid: [
					],
					username: [
					],
					avatarurl: [
					],
					isdone: [
					],
					istop: [
						{ validator: validateIntNumber, trigger: 'blur' },
					],
					toptime: [
					],
					cover: [
					],
					isanon: [
						{ validator: validateIntNumber, trigger: 'blur' },
					],
					delflag: [
						{ validator: validateIntNumber, trigger: 'blur' },
					],
					title: [
					],
					userid: [
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
						if(o=='content'){
							this.ruleForm.content = obj[o];
							this.ro.content = true;
							continue;
						}
						if(o=='parentid'){
							this.ruleForm.parentid = obj[o];
							this.ro.parentid = true;
							continue;
						}
						if(o=='username'){
							this.ruleForm.username = obj[o];
							this.ro.username = true;
							continue;
						}
						if(o=='avatarurl'){
							this.ruleForm.avatarurl = obj[o];
							this.ro.avatarurl = true;
							continue;
						}
						if(o=='isdone'){
							this.ruleForm.isdone = obj[o];
							this.ro.isdone = true;
							continue;
						}
						if(o=='istop'){
							this.ruleForm.istop = obj[o];
							this.ro.istop = true;
							continue;
						}
						if(o=='toptime'){
							this.ruleForm.toptime = obj[o];
							this.ro.toptime = true;
							continue;
						}
						if(o=='cover'){
							this.ruleForm.cover = obj[o];
							this.ro.cover = true;
							continue;
						}
						if(o=='isanon'){
							this.ruleForm.isanon = obj[o];
							this.ro.isanon = true;
							continue;
						}
						if(o=='delflag'){
							this.ruleForm.delflag = obj[o];
							this.ro.delflag = true;
							continue;
						}
						if(o=='title'){
							this.ruleForm.title = obj[o];
							this.ro.title = true;
							continue;
						}
						if(o=='userid'){
							this.ruleForm.userid = obj[o];
							this.ro.userid = true;
							continue;
						}
					}
				}

				this.isdoneOptions = "开放,关闭".split(',')
			
			},
			// 多级联动参数

			async info(id) {
				await this.$http({
					url: `forum/info/${id}`,
					method: "get"
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.ruleForm = data.data;
						//解决前台上传图片后台不显示的问题
						let reg=new RegExp('../../../upload','g')//g代表全部
						this.ruleForm.content = this.ruleForm.content.replace(reg,'../../../djangop8gh5erc/upload');
					} else {
						this.$message.error(data.msg);
					}
				});
			},

			// 提交
			async onSubmit() {
					if(this.ruleForm.avatarurl!=null) {
						this.ruleForm.avatarurl = this.ruleForm.avatarurl.replace(new RegExp(this.$base.url,"g"),"");
					}
					if(this.ruleForm.cover!=null) {
						this.ruleForm.cover = this.ruleForm.cover.replace(new RegExp(this.$base.url,"g"),"");
					}
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
								url: `forum/${!this.ruleForm.id ? "save" : "update"}`,
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
											this.parent.forumCrossAddOrUpdateFlag = false;
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
				this.parent.forumCrossAddOrUpdateFlag = false;
			},
			avatarurlUploadChange(fileUrls) {
				this.ruleForm.avatarurl = fileUrls;
			},
			coverUploadChange(fileUrls) {
				this.ruleForm.cover = fileUrls;
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
