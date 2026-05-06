<template>
	<div :style='{"alignContent":"flex-start","padding":"0 10%","margin":"0px auto","alignItems":"flex-start","flexWrap":"wrap","background":"none","display":"flex","width":"100%","position":"relative"}'>
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">
				<span class="icon iconfont icon-fanhui01"></span>
				<span class="text">返回</span>
			</el-button>
		</div>
		<div v-if="storeupType==1" class="section-title" :style='{"padding":"0","borderColor":"#e61f4d","margin":"10px auto","color":"#000000","textAlign":"center","display":"block","background":"none","borderWidth":"0 0 0px","width":"100%","lineHeight":"32px","fontSize":"30px","borderStyle":"solid","fontWeight":"600"}'>我的收藏</div>
		<div v-if="storeupType==21" class="section-title" :style='{"padding":"0","borderColor":"#e61f4d","margin":"10px auto","color":"#000000","textAlign":"center","display":"block","background":"none","borderWidth":"0 0 0px","width":"100%","lineHeight":"32px","fontSize":"30px","borderStyle":"solid","fontWeight":"600"}'>我的点赞</div>
		<div v-if="storeupType==81" class="section-title" :style='{"padding":"0","borderColor":"#e61f4d","margin":"10px auto","color":"#000000","textAlign":"center","display":"block","background":"none","borderWidth":"0 0 0px","width":"100%","lineHeight":"32px","fontSize":"30px","borderStyle":"solid","fontWeight":"600"}'>我的评论</div>
		<el-form v-if="storeupType!=81" :inline="true" :model="formSearch" class="list-form-pv">
			<el-form-item class="search-item">
				<el-input v-model="formSearch.name" placeholder="名称"></el-input>
			</el-form-item>
			<div class="search-btn-item">
				<el-button class="searchBtn" type="primary" @click="getStoreupList(1)">
					<span class="icon iconfont icon-fangdajing07"></span>
					查询
				</el-button>
			</div>
		</el-form>
		<div v-if="storeupType!=81" style="display: flex;flex-wrap: wrap;width: 100%">
			<div style="width: 23%;margin: 0 1% 20px" v-for="(item, index) in storeupList" :key="index" @click="toDetail(item)">
				<el-card :body-style="{ padding: '0px', cursor: 'pointer' }">
					<el-image v-if="item.picture && item.picture.substr(0,4)=='http'" :src="item.picture" fit="fill" class="image"></el-image>
					<el-image v-else-if="item.picture&& item.picture.substr(0,4)!='http'" :src="baseUrl + item.picture" fit="fill" class="image"></el-image>
					<div style="padding: 14px;">
						<span v-if="item.remark">{{item.name}}</span>
						<span v-if="!item.remark">{{item.name}}</span>
					</div>
					<div style="padding: 0 5px 5px">
						<el-button type="danger" size="mini" @click.stop="delClick(item)">删除</el-button>
					</div>
				</el-card>
			</div>
		</div>
		<div v-else style="width: 100%">
			<el-table class="tables" :stripe='false'
				:style='{"width":"100%","padding":"0","borderColor":"#eee","borderStyle":"solid","borderWidth":"1px 0 0 1px","background":"#fff"}' 
				:border='true'
				:data="storeupList">
				<el-table-column :resizable='true' :sortable='false' prop="content" label="评论内容" show-overflow-tooltip>
					<template slot-scope="scope">
						<span class="ql-snow ql-editor" style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;" v-html="scope.row.content"></span>
					</template>
				</el-table-column>
				<el-table-column :resizable='true' :sortable='false' prop="reply" label="回复内容" show-overflow-tooltip>
					<template slot-scope="scope">
						<span class="ql-snow ql-editor" style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;" v-html="scope.row.reply"></span>
					</template>
				</el-table-column>
				<el-table-column width="300" label="操作">
					<template slot-scope="scope">
						<el-button class="view" type="success" size="mini"
							@click="toDetail(scope.row)">
							查看
						</el-button>
						<el-button class="del" type="danger" size="mini"
							@click="delClick(scope.row)">
							删除
						</el-button>
					</template>
				</el-table-column>
			</el-table>
		</div>
	
		<el-pagination
			v-if="storeupType!=81"
			background
			id="pagination" class="pagination"
			:pager-count="7"
			:page-size="pageSize"
			:page-sizes="pageSizes"
			prev-text="<"
			next-text=">"
			:hide-on-single-page="true"
			:layout='["total","prev","pager","next","sizes","jumper"].join()'
			:total="total"
			:style='{"padding":"0","margin":"20px auto","whiteSpace":"nowrap","color":"#333","textAlign":"center","width":"100%","fontSize":"16px","fontWeight":"500","order":"50"}'
			@current-change="curChange"
			@prev-click="prevClick"
			@size-change="sizeChange"
			@next-click="nextClick"
			></el-pagination>
	
	</div>
</template>

<script>
	import config from '@/config/config'
	export default {
		data() {
			return {
				layouts: '',
				baseUrl: config.baseUrl,
				formSearch: {
					name: ''
				},
				storeupType: 1,
				storeupList: [],
				total: 1,
				pageSize: 8,
				pageSizes: [],
				totalPage: 1
			}
		},
		created() {
			this.storeupType = localStorage.getItem('storeupType');
			this.getStoreupList(1);
		},
		methods: {
			backClick() {
				this.$router.push('/index/center')
			},
			getStoreupList(page) {
				if(this.storeupType==81) {
					this.$http.get('comment/list', {}).then(res => {
						this.storeupList = res.data.data;
					})
					return false
				}
				let params = {page, limit: this.pageSize, type: this.storeupType, userid: Number(localStorage.getItem('frontUserid')),sort:"addtime",order:"desc"};
				let searchWhere = {
				};
				if (this.formSearch.name != '') searchWhere.name = '%' + this.formSearch.name + '%';
				this.$http.get('storeup/list', {params: Object.assign(params, searchWhere)}).then(res => {
					if (res.data.code == 0) {
						this.storeupList = res.data.data.list;
						this.total = res.data.data.total;
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			curChange(page) {
				this.getStoreupList(page);
			},
			prevClick(page) {
				this.getStoreupList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getStoreupList(1);
			},
			nextClick(page) {
				this.getStoreupList(page);
			},
			toDetail(item) {
				let params = {
					id: item.refid,
					storeupType: 1,
				}
				if(this.storeupType == 81) {
					params.discussId = item.id
				}
				this.$router.push({path: `/index/${item.tablename}Detail`, query: params});
			},
			async delClick(row){
				await this.$confirm(`是否删除此记录？`) .then(async _ => {
					if(this.storeupType==81) {
						await this.$http.post(`discuss${row.tablename}/delete`, [row.id]).then(async res => {
							if (res.data.code == 0) {
								await this.$http.get(`${row.tablename}/info/${row.refid}`).then(async rs=>{
									rs.data.data.discussnum--
									await this.$http.post(`${row.tablename}/update`,rs.data.data).then(rs2=>{})
								})
								this.$message({
									type: 'success',
									message: '删除成功!',
									duration: 1500,
									onClose: () => {
										this.getStoreupList(1);
									}
								});
							}
						});
						return false
					}
					this.$http.post('storeup/delete', [row.id]).then(async res => {
						if (res.data.code == 0) {
							if(this.storeupType==1) {
								await this.$http.get(`${row.tablename}/info/${row.refid}`).then(async rs=>{
									rs.data.data.storeupnum--
									await this.$http.post(`${row.tablename}/update`,rs.data.data).then(rs2=>{})
								})
							}
							if(this.storeupType==21) {
								await this.$http.get(`${row.tablename}/info/${row.refid}`).then(async rs=>{
									rs.data.data.thumbsupnum--
									await this.$http.post(`${row.tablename}/update`,rs.data.data).then(rs2=>{})
								})
							}
							this.$message({
								type: 'success',
								message: '删除成功!',
								duration: 1500,
								onClose: () => {
									this.getStoreupList(1);
								}
							});
						}
					});
				}).catch(_ => {});
			},
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.section {
		width: 900px;
		margin: 0 auto;
	}

	.list-form-pv {
				padding: 10px;
				margin: 10px 0;
				background: none;
				display: flex;
				width: 100%;
				justify-content: center;
				align-items: center;
				flex-wrap: wrap;
				height: auto;
				.search-item {
						margin: 0 10px;
						/deep/ .el-form-item__content {
								display: flex;
								align-items: center;
							}
			.el-input {
								width: 100%;
							}
			.el-input /deep/ .el-input__inner {
								border: 1px solid #000;
								border-radius: 0px;
								padding: 0 10px;
								margin: 0;
								outline: none;
								color: #666;
								width: 500px;
								font-size: 16px;
								line-height: 42px;
								height: 42px;
							}
		}
		.search-btn-item {
						display: flex;
						.searchBtn {
								cursor: pointer;
								border: 1px solid #000;
								border-radius: 20px;
								padding: 0px 15px;
								margin: 0 10px 0 0;
								outline: none;
								background: #000000;
								width: auto;
								font-size: 16px;
								line-height: 42px;
								height: 42px;
								.icon {
										margin: 0 5px 0 0;
										color: #fff;
									}
			}
			
			.searchBtn:hover {
								opacity: 0.8;
							}
			
			.pubBtn {
								cursor: pointer;
								border: 1px solid #000;
								border-radius: 20px;
								padding: 0px 15px;
								margin: 0 10px 0 0;
								outline: none;
								color: #000;
								background: none;
								width: auto;
								font-size: 16px;
								line-height: 42px;
								height: 42px;
								.icon {
										margin: 0 5px 0 0;
										color: #000;
										font-size: 16px;
									}
			}
			
			.pubBtn:hover {
								opacity: 0.8;
							}
		}
	}
	.image {
		height: 233px;
		width: 100%;
		display: block;
	}
	.el-table /deep/ .el-table__header-wrapper thead {
		color: #333;
		font-weight: 500;
		width: 100%;
	}
	
	.el-table /deep/ .el-table__header-wrapper thead tr {
		background: #fff;
	}
	
	.el-table /deep/ .el-table__header-wrapper thead tr th {
		padding: 12px 0;
		border-color: #eee;
		border-width: 0 1px 1px 0;
		border-style: solid;
		text-align: left;
	}
	
	.el-table /deep/ .el-table__header-wrapper thead tr th .cell {
		padding: 0 10px;
		word-wrap: normal;
		word-break: break-all;
		white-space: normal;
		font-weight: bold;
		display: inline-block;
		vertical-align: middle;
		width: 100%;
		line-height: 24px;
		position: relative;
		text-overflow: ellipsis;
	}
	
	
	.el-table /deep/ .el-table__body-wrapper tbody {
		width: 100%;
	}
	
	.el-table /deep/ .el-table__body-wrapper tbody tr {
		background: #fff;
	}
	
	.el-table /deep/ .el-table__body-wrapper tbody tr td {
		padding: 12px 0;
		color: #666;
		background: #fff;
		border-color: #eee;
		border-width: 0 1px 1px 0;
		border-style: solid;
		text-align: left;
	}
	
	
	.el-table /deep/ .el-table__body-wrapper tbody tr:hover td {
		padding: 12px 0;
		color: #333;
		background: rgba(64, 158, 255, .1);
		border-color: #eee;
		border-width: 0 1px 1px 0;
		border-style: solid;
		text-align: left;
	}
	
	.el-table /deep/ .el-table__body-wrapper tbody tr td {
		padding: 12px 0;
		color: #666;
		background: #fff;
		border-color: #eee;
		border-width: 0 1px 1px 0;
		border-style: solid;
		text-align: left;
	}
	
	.el-table /deep/ .el-table__body-wrapper tbody tr td .cell {
		padding: 0 10px;
		overflow: hidden;
		word-break: break-all;
		white-space: normal;
		line-height: 24px;
		text-overflow: ellipsis;
	}
</style>
