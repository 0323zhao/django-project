<template>
	<div class="home-preview">




		<!-- 商品推荐 -->
		<div id="animate_recommendbloginfo" class="recommend animate__animated">
			<div class="recommend_title_box">
				<span class="recommend_title">博文信息推荐</span>
				<span class="recommend_subhead">{{'bloginfo'.toUpperCase()}} RECOMMEND</span>
			</div>
			<!-- 样式六 -->
			<div class="list list6 index-pv1">
				<div class="list-body-left">
					<div v-if="bloginfoRecommend.length>0" @click="toDetail('bloginfoDetail', bloginfoRecommend[0])" class="list-item1 animation-box">
						<div class="infoBox">
							<div class="name">{{bloginfoRecommend[0].screenname}}</div>
							<div class="name">评论数:{{bloginfoRecommend[0].commentscount}}</div>
							<div class="name">转发数:{{bloginfoRecommend[0].repostscount}}</div>
							<div class="name">点赞数:{{bloginfoRecommend[0].attitudescount}}</div>
							<div class="name">{{bloginfoRecommend[0].fbtime}}</div>
							<div class="name">{{bloginfoRecommend[0].medias}}</div>
							<div class="time_item">
								<span class="icon iconfont icon-shijian21"></span>
								<span class="label">发布时间：</span>
								<span class="text">{{bloginfoRecommend[0].addtime.split(' ')[0]}}</span>
							</div>
							<div class="like_item">
								<span class="icon iconfont icon-zan10"></span>
								<span class="label">点赞数：</span>
								<span class="text">{{bloginfoRecommend[0].thumbsupnum}}</span>
							</div>
							<div class="collect_item">
								<span class="icon iconfont icon-shoucang10"></span>
								<span class="label">收藏量：</span>
								<span class="text">{{bloginfoRecommend[0].storeupnum}}</span>
							</div>
							<div class="view_item">
								<span class="icon iconfont icon-chakan2"></span>
								<span class="label">点击量：</span>
								<span class="text">{{bloginfoRecommend[0].clicknum}}</span>
							</div>
						</div>
					</div>
					<div v-if="bloginfoRecommend.length>1" @click="toDetail('bloginfoDetail', bloginfoRecommend[1])" class="list-item2 animation-box">
						<div class="infoBox">
							<div class="name">{{bloginfoRecommend[1].screenname}}</div>
							<div class="name">评论数:{{bloginfoRecommend[1].commentscount}}</div>
							<div class="name">转发数:{{bloginfoRecommend[1].repostscount}}</div>
							<div class="name">点赞数:{{bloginfoRecommend[1].attitudescount}}</div>
							<div class="name">{{bloginfoRecommend[1].fbtime}}</div>
							<div class="name">{{bloginfoRecommend[1].medias}}</div>
							<div class="time_item">
								<span class="icon iconfont icon-shijian21"></span>
								<span class="label">发布时间：</span>
								<span class="text">{{bloginfoRecommend[1].addtime.split(' ')[0]}}</span>
							</div>
							<div class="like_item">
								<span class="icon iconfont icon-zan10"></span>
								<span class="label">点赞数：</span>
								<span class="text">{{bloginfoRecommend[1].thumbsupnum}}</span>
							</div>
							<div class="collect_item">
								<span class="icon iconfont icon-shoucang10"></span>
								<span class="label">收藏量：</span>
								<span class="text">{{bloginfoRecommend[1].storeupnum}}</span>
							</div>
							<div class="view_item">
								<span class="icon iconfont icon-chakan2"></span>
								<span class="label">点击量：</span>
								<span class="text">{{bloginfoRecommend[1].clicknum}}</span>
							</div>
						</div>
					</div>
				</div>
				<div v-if="bloginfoRecommend.length>2" class="list-item3 animation-box" @click="toDetail('bloginfoDetail', bloginfoRecommend[2])">
					<div class="infoBox">
						<div class="name">{{bloginfoRecommend[2].screenname}}</div>
						<div class="name">评论数:{{bloginfoRecommend[2].commentscount}}</div>
						<div class="name">转发数:{{bloginfoRecommend[2].repostscount}}</div>
						<div class="name">点赞数:{{bloginfoRecommend[2].attitudescount}}</div>
						<div class="name">{{bloginfoRecommend[2].fbtime}}</div>
						<div class="name">{{bloginfoRecommend[2].medias}}</div>
						<div class="time_item">
							<span class="icon iconfont icon-shijian21"></span>
							<span class="label">发布时间：</span>
							<span class="text">{{bloginfoRecommend[2].addtime.split(' ')[0]}}</span>
						</div>
						<div class="like_item">
							<span class="icon iconfont icon-zan10"></span>
							<span class="label">点赞数：</span>
							<span class="text">{{bloginfoRecommend[2].thumbsupnum}}</span>
						</div>
						<div class="collect_item">
							<span class="icon iconfont icon-shoucang10"></span>
							<span class="label">收藏量：</span>
							<span class="text">{{bloginfoRecommend[2].storeupnum}}</span>
						</div>
						<div class="view_item">
							<span class="icon iconfont icon-chakan2"></span>
							<span class="label">点击量：</span>
							<span class="text">{{bloginfoRecommend[2].clicknum}}</span>
						</div>
					</div>
				</div>
				<div class="list-body-right">
					<div v-if="bloginfoRecommend.length>3" @click="toDetail('bloginfoDetail', bloginfoRecommend[3])" class="list-item1 animation-box">
						<div class="infoBox">
							<div class="name">{{bloginfoRecommend[3].screenname}}</div>
							<div class="name">评论数:{{bloginfoRecommend[3].commentscount}}</div>
							<div class="name">转发数:{{bloginfoRecommend[3].repostscount}}</div>
							<div class="name">点赞数:{{bloginfoRecommend[3].attitudescount}}</div>
							<div class="name">{{bloginfoRecommend[3].fbtime}}</div>
							<div class="name">{{bloginfoRecommend[3].medias}}</div>
							<div class="time_item">
								<span class="icon iconfont icon-shijian21"></span>
								<span class="label">发布时间：</span>
								<span class="text">{{bloginfoRecommend[3].addtime.split(' ')[0]}}</span>
							</div>
							<div class="like_item">
								<span class="icon iconfont icon-zan10"></span>
								<span class="label">点赞数：</span>
								<span class="text">{{bloginfoRecommend[3].thumbsupnum}}</span>
							</div>
							<div class="collect_item">
								<span class="icon iconfont icon-shoucang10"></span>
								<span class="label">收藏量：</span>
								<span class="text">{{bloginfoRecommend[3].storeupnum}}</span>
							</div>
							<div class="view_item">
								<span class="icon iconfont icon-chakan2"></span>
								<span class="label">点击量：</span>
								<span class="text">{{bloginfoRecommend[3].clicknum}}</span>
							</div>
						</div>
					</div>
					<div v-if="bloginfoRecommend.length>4" @click="toDetail('bloginfoDetail', bloginfoRecommend[4])" class="list-item2 animation-box">
						<div class="infoBox">
							<div class="name">{{bloginfoRecommend[4].screenname}}</div>
							<div class="name">评论数:{{bloginfoRecommend[4].commentscount}}</div>
							<div class="name">转发数:{{bloginfoRecommend[4].repostscount}}</div>
							<div class="name">点赞数:{{bloginfoRecommend[4].attitudescount}}</div>
							<div class="name">{{bloginfoRecommend[4].fbtime}}</div>
							<div class="name">{{bloginfoRecommend[4].medias}}</div>
							<div class="time_item">
								<span class="icon iconfont icon-shijian21"></span>
								<span class="label">发布时间：</span>
								<span class="text">{{bloginfoRecommend[4].addtime.split(' ')[0]}}</span>
							</div>
							<div class="like_item">
								<span class="icon iconfont icon-zan10"></span>
								<span class="label">点赞数：</span>
								<span class="text">{{bloginfoRecommend[4].thumbsupnum}}</span>
							</div>
							<div class="collect_item">
								<span class="icon iconfont icon-shoucang10"></span>
								<span class="label">收藏量：</span>
								<span class="text">{{bloginfoRecommend[4].storeupnum}}</span>
							</div>
							<div class="view_item">
								<span class="icon iconfont icon-chakan2"></span>
								<span class="label">点击量：</span>
								<span class="text">{{bloginfoRecommend[4].clicknum}}</span>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="moreBtn" @click="moreBtn('bloginfo')">
				<span class="text">查看更多</span>
				<i class="icon iconfont icon-gengduo1"></i>
			</div>
		</div>
		<!-- 商品推荐 -->
		<!-- 特价商品 -->
		<div id="animate_listxitonggonggao" class="lists animate__animated">
			<div class="list_title_box">
				<span class="list_title">系统公告展示</span>
				<span class="list_subhead">{{'xitonggonggao'.toUpperCase()}} SHOW</span>
			</div>
			<div class="list list22 index-pv1">
				<div class="list-body-left">
					<div class="list-item1" v-if="xitonggonggaoList.length>0" @click="toDetail('xitonggonggaoDetail', xitonggonggaoList[0])">
						<img v-if="preHttp(xitonggonggaoList[0].fengmian)" :src="xitonggonggaoList[0].fengmian.split(',')[0]" alt="" />
						<img v-else :src="baseUrl + (xitonggonggaoList[0].fengmian?xitonggonggaoList[0].fengmian.split(',')[0]:'')" alt="" />
						<div class="name">{{xitonggonggaoList[0].gonggaobiaoti}}</div>
						<div class="name">{{xitonggonggaoList[0].gonggaofenlei}}</div>
					</div>
					<div class="list-item2" v-if="xitonggonggaoList.length>1" @click="toDetail('xitonggonggaoDetail', xitonggonggaoList[1])">
						<div class="img">
							<img v-if="preHttp(xitonggonggaoList[1].fengmian)" :src="xitonggonggaoList[1].fengmian.split(',')[0]" alt="" />
							<img v-else :src="baseUrl + (xitonggonggaoList[1].fengmian?xitonggonggaoList[1].fengmian.split(',')[0]:'')" alt="" />
						</div>
						<div class="infoBox">
							<div class="name">{{xitonggonggaoList[1].gonggaobiaoti}}</div>
							<div class="name">{{xitonggonggaoList[1].gonggaofenlei}}</div>
							<div class="desc ql-snow ql-editor" v-html="xitonggonggaoList[1].jianjie"></div>

							<div class="bottom">
								<div class="time">{{xitonggonggaoList[1].addtime.split(' ')[0]}}</div>
							</div>
							<div class="jian"></div>
					  </div>
					</div>
				</div>
				<div class="list-body-right">
					<div class="list-item1" v-if="xitonggonggaoList.length>2" @click="toDetail('xitonggonggaoDetail', xitonggonggaoList[2])">
						<div class="img">
							<img v-if="preHttp(xitonggonggaoList[2].fengmian)" :src="xitonggonggaoList[2].fengmian.split(',')[0]" alt="" />
							<img v-else :src="baseUrl + (xitonggonggaoList[2].fengmian?xitonggonggaoList[2].fengmian.split(',')[0]:'')" alt="" />
						</div>
						<div class="infoBox">
							<div class="name" >{{xitonggonggaoList[2].gonggaobiaoti}}</div>
							<div class="name" >{{xitonggonggaoList[2].gonggaofenlei}}</div>
							<div class="desc ql-snow ql-editor" v-html="xitonggonggaoList[2].jianjie"></div>

							<div class="bottom">
								<div class="time">{{xitonggonggaoList[2].addtime.split(' ')[0]}}</div>
							</div>
							<div class="jian"></div>
						</div>
					</div>
					<div class="list-item2" v-if="xitonggonggaoList.length>3" @click="toDetail('xitonggonggaoDetail', xitonggonggaoList[3])">
						<div class="infoBox">
							<div class="name">{{xitonggonggaoList[3].gonggaobiaoti}}</div>
							<div class="name">{{xitonggonggaoList[3].gonggaofenlei}}</div>
							<div class="desc ql-snow ql-editor" v-html="xitonggonggaoList[3].jianjie"></div>

							<div class="bottom">
								<div class="time">{{xitonggonggaoList[3].addtime.split(' ')[0]}}</div>
							</div>
							<div class="jian"></div>
						</div>
						<div class="img">
							<img v-if="preHttp(xitonggonggaoList[3].fengmian)" :src="xitonggonggaoList[3].fengmian.split(',')[0]" alt="" />
							<img v-else :src="baseUrl + (xitonggonggaoList[3].fengmian?xitonggonggaoList[3].fengmian.split(',')[0]:'')" alt="" />
						</div>
					</div>
					<div class="list-item3" v-if="xitonggonggaoList.length>4" @click="toDetail('xitonggonggaoDetail', xitonggonggaoList[4])">
						<div class="img">
							<img v-if="preHttp(xitonggonggaoList[4].fengmian)" :src="xitonggonggaoList[4].fengmian.split(',')[0]" alt="" />
							<img v-else :src="baseUrl + (xitonggonggaoList[4].fengmian?xitonggonggaoList[4].fengmian.split(',')[0]:'')" alt="" />
						</div>
						<div class="infoBox">
							<div class="name">{{xitonggonggaoList[4].gonggaobiaoti}}</div>
							<div class="name">{{xitonggonggaoList[4].gonggaofenlei}}</div>
							<div class="desc ql-snow ql-editor" v-html="xitonggonggaoList[4].jianjie"></div>

							<div class="bottom">
								<div class="time">{{xitonggonggaoList[4].addtime.split(' ')[0]}}</div>
							</div>
							<div class="jian"></div>
						</div>
					</div>
				</div>
			</div>
			<div class="moreBtn" @click="moreBtn('xitonggonggao')">
				<span class="text">查看更多</span>
				<i class="icon iconfont icon-jiantou25"></i>
			</div>
	

		</div>
		<!-- 特价商品 -->
	</div>
</template>

<script>
import 'animate.css'
import Swiper from "swiper";

	export default {
		//数据集合
		data() {
			return {
				baseUrl: '',
				newsList: [],
				bloginfoRecommend: [],

				xitonggonggaoList: [],




			}
		},
		created() {
			this.baseUrl = this.$config.baseUrl;
			this.getList();
		},
		mounted() {
			window.addEventListener('scroll', this.handleScroll)
			setTimeout(()=>{
				this.handleScroll()
			},100)
			
			this.swiperChanges()
		},
		beforeDestroy() {
			window.removeEventListener('scroll', this.handleScroll)
		},
		computed: {
			username() {
				return localStorage.getItem('username')
			}
		},
		//方法集合
		methods: {
			swiperChanges() {
				setTimeout(()=>{
				},750)
			},


			handleScroll() {
				let arr = [
					{id:'about',css:'animate__'},
					{id:'system',css:'animate__'},
					{id:'animate_recommendbloginfo',css:'animate__'},
					{id:'animate_listxitonggonggao',css:'animate__'},
				]
			
				for (let i in arr) {
					let doc = document.getElementById(arr[i].id)
					if (doc) {
						let top = doc.offsetTop
						let win_top = window.innerHeight + window.pageYOffset
						// console.log(top,win_top)
						if (win_top > top && doc.classList.value.indexOf(arr[i].css) < 0) {
							// console.log(doc)
							doc.classList.add(arr[i].css)
						}
					}
				}
			},
			preHttp(str) {
				return str && str.substr(0,4)=='http';
			},
			preHttp2(str) {
				return str && str.split(',w').length>1;
			},
			getList() {
				let autoSortUrl = "";
				let data = {}
				autoSortUrl = "bloginfo/autoSort";
				if(localStorage.getItem('frontToken')) {
					autoSortUrl = "bloginfo/autoSort2";
				}
				data = {
					page: 1,
					limit: 5,
				}
				this.$http.get(autoSortUrl, {params: data}).then(res => {
					if (res.data.code == 0) {
						this.bloginfoRecommend = res.data.data.list;
					}
				});
			
				data = {
					page: 1,
					limit: 5,
				}

				this.$http.get('xitonggonggao/list', {params: data}).then(res => {
					if (res.data.code == 0) {
						this.xitonggonggaoList = res.data.data.list;
					}
				});
			},
			toDetail(path, item) {
				this.$router.push({path: '/index/' + path, query: {id: item.id, storeupType: 1}});
			},
			moreBtn(path) {
				this.$router.push({path: '/index/' + path});
			}
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.home-preview {
		padding: 0;
		margin: 0 auto;
		overflow: hidden;
		display: flex;
		width: 100%;
		justify-content: space-between;
		flex-wrap: wrap;
		.recommend {
			padding: 0 10% 60px;
			margin: 0 auto 0;
			background: none;
			width: 100%;
			position: relative;
			order: 1;
			.recommend_title_box {
				margin: 20px auto;
				background: none;
				display: flex;
				width: 100%;
				justify-content: center;
				flex-wrap: wrap;
				.recommend_title {
					padding: 0 0 16px;
					color: #000;
					background: url(http://codegen.caihongy.cn/20251205/71e1fc1f994a476bac2b5c5561524981.png) no-repeat bottom center;
					font-weight: 600;
					display: block;
					width: 100%;
					font-size: 30px;
					line-height: 1.5;
					text-align: center;
				}
				.recommend_subhead {
					margin: 0;
					color: #2b2b2b;
					font-weight: 500;
					display: block;
					width: auto;
					font-size: 18px;
					line-height: 30px;
					text-align: left;
				}
			}
			.index-pv1 .animation-box {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				z-index: initial;
			}
			
			.index-pv1 .animation-box:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, -4px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
				z-index: 1;
			}
			
			.index-pv1 .animation-box img {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
			}
			
			.index-pv1 .animation-box img:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
			}
			.list6 {
				padding: 10px 0;
				color: #fff;
				background: none;
				display: flex;
				width: 100%;
				font-size: 14px;
				height: auto;
				.list-body-left {
					margin: 0 10px 0 0;
					width: calc(33% - 10px);
					height: 275px;
					.list-item1 {
						cursor: pointer;
						margin: 0 0 20px;
						width: 100%;
						position: relative;
						height: 275px;
						img {
							object-fit: cover;
							width: 100%;
							float: left;
							height: 100%;
						}
						.infoBox {
							padding: 10px 0;
							align-content: center;
							left: 0;
							bottom: 0;
							background: rgba(0,0,0,.3);
							display: flex;
							width: 100%;
							align-items: center;
							position: absolute;
							flex-wrap: wrap;
							.name {
								padding: 0 10px;
								overflow: hidden;
								color: #fff;
								white-space: nowrap;
								width: 100%;
								font-size: 15px;
								line-height: 26px;
								text-overflow: ellipsis;
							}
							.price {
								padding: 0 10px;
								color: #f00;
								width: 100%;
								font-size: 16px;
								line-height: 1.5;
							}
							.time_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.publisher_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.like_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.collect_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.view_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
						}
					}
					.list-item2 {
						cursor: pointer;
						margin: 20px 0 0;
						width: 100%;
						position: relative;
						height: 275px;
						img {
							object-fit: cover;
							width: 100%;
							float: left;
							height: 100%;
						}
						.infoBox {
							padding: 10px 0;
							align-content: center;
							left: 0;
							bottom: 0;
							background: rgba(0,0,0,.3);
							display: flex;
							width: 100%;
							align-items: center;
							position: absolute;
							flex-wrap: wrap;
							.name {
								padding: 0 10px;
								overflow: hidden;
								color: #fff;
								white-space: nowrap;
								width: 100%;
								font-size: 15px;
								line-height: 26px;
								text-overflow: ellipsis;
							}
							.price {
								padding: 0 10px;
								color: #f00;
								width: 100%;
								font-size: 16px;
								line-height: 1.5;
							}
							.time_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.publisher_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.like_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.collect_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.view_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
						}
					}
				}
				.list-item3 {
					cursor: pointer;
					margin: 0 10px;
					width: calc(34% - 20px);
					position: relative;
					height: 570px;
					img {
						object-fit: cover;
						width: 100%;
						float: left;
						height: 100%;
					}
					.infoBox {
						padding: 10px 0;
						align-content: center;
						left: 0;
						bottom: 0;
						background: rgba(0,0,0,.3);
						display: flex;
						width: 100%;
						align-items: center;
						position: absolute;
						flex-wrap: wrap;
						.name {
							padding: 0 10px;
							overflow: hidden;
							color: #fff;
							white-space: nowrap;
							width: 100%;
							font-size: 15px;
							line-height: 26px;
							text-overflow: ellipsis;
						}
						.price {
							padding: 0 10px;
							color: #f00;
							width: 100%;
							font-size: 16px;
							line-height: 1.5;
						}
						.time_item {
							padding: 0 10px;
							.icon {
								margin: 0 2px 0 0;
								line-height: 1.5;
							}
							.label {
								line-height: 1.5;
							}
							.text {
								line-height: 1.5;
							}
						}
						.publisher_item {
							padding: 0 10px;
							.icon {
								margin: 0 2px 0 0;
								line-height: 1.5;
							}
							.label {
								line-height: 1.5;
							}
							.text {
								line-height: 1.5;
							}
						}
						.like_item {
							padding: 0 10px;
							.icon {
								margin: 0 2px 0 0;
								line-height: 1.5;
							}
							.label {
								line-height: 1.5;
							}
							.text {
								line-height: 1.5;
							}
						}
						.collect_item {
							padding: 0 10px;
							.icon {
								margin: 0 2px 0 0;
								line-height: 1.5;
							}
							.label {
								line-height: 1.5;
							}
							.text {
								line-height: 1.5;
							}
						}
						.view_item {
							padding: 0 10px;
							.icon {
								margin: 0 2px 0 0;
								line-height: 1.5;
							}
							.label {
								line-height: 1.5;
							}
							.text {
								line-height: 1.5;
							}
						}
					}
				}
				.list-body-right {
					margin: 0 0 0 10px;
					width: calc(33% - 10px);
					height: 275px;
					.list-item1 {
						cursor: pointer;
						margin: 0 0 20px;
						width: 100%;
						position: relative;
						height: 275px;
						img {
							object-fit: cover;
							width: 100%;
							float: left;
							height: 100%;
						}
						.infoBox {
							padding: 10px 0;
							align-content: center;
							left: 0;
							bottom: 0;
							background: rgba(0,0,0,.3);
							display: flex;
							width: 100%;
							align-items: center;
							position: absolute;
							flex-wrap: wrap;
							.name {
								padding: 0 10px;
								overflow: hidden;
								color: #fff;
								white-space: nowrap;
								width: 100%;
								font-size: 15px;
								line-height: 26px;
								text-overflow: ellipsis;
							}
							.price {
								padding: 0 10px;
								color: #f00;
								width: 100%;
								font-size: 16px;
								line-height: 1.5;
							}
							.time_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.publisher_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.like_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.collect_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.view_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
						}
					}
					.list-item2 {
						cursor: pointer;
						margin: 20px 0 0;
						width: 100%;
						position: relative;
						height: 275px;
						img {
							object-fit: cover;
							width: 100%;
							float: left;
							height: 100%;
						}
						.infoBox {
							padding: 10px 0;
							align-content: center;
							left: 0;
							bottom: 0;
							background: rgba(0,0,0,.3);
							display: flex;
							width: 100%;
							align-items: center;
							position: absolute;
							flex-wrap: wrap;
							.name {
								padding: 0 10px;
								overflow: hidden;
								color: #fff;
								white-space: nowrap;
								width: 100%;
								font-size: 15px;
								line-height: 26px;
								text-overflow: ellipsis;
							}
							.price {
								padding: 0 10px;
								color: #f00;
								width: 100%;
								font-size: 16px;
								line-height: 1.5;
							}
							.time_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.publisher_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.like_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.collect_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.view_item {
								padding: 0 10px;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
						}
					}
				}
			}
			.moreBtn {
				border: 0px solid #ddd;
				cursor: pointer;
				border-radius: 0px;
				margin: 0px auto 0;
				top: 0;
				background: #6aac5a;
				display: none;
				width: 120px;
				line-height: 40px;
				justify-content: center;
				position: absolute;
				right: 7%;
				.text {
					margin: 0 5px 0 0;
					color: #fff;
					font-size: 16px;
					order: 2;
				}
				.icon {
					margin: 0 10px 0 0;
					color: #fff;
					display: none;
					width: auto;
					font-size: 18px;
					height: 7px;
				}
			}
		}
		.lists {
			padding: 30px 10% 40px;
			margin: 0 auto;
			background: none;
			width: 100%;
			position: relative;
			order: 4;
			.list_title_box {
				margin: 20px auto;
				background: none;
				display: flex;
				width: 100%;
				justify-content: center;
				flex-wrap: wrap;
				.list_title {
					padding: 0 0 16px;
					color: #000;
					background: url(http://codegen.caihongy.cn/20251205/71e1fc1f994a476bac2b5c5561524981.png) no-repeat bottom center;
					font-weight: 600;
					display: block;
					width: 100%;
					font-size: 30px;
					line-height: 1.5;
					text-align: center;
				}
				.list_subhead {
					margin: 0;
					color: #2b2b2b;
					font-weight: 500;
					display: block;
					width: auto;
					font-size: 16px;
					line-height: 2;
					text-align: center;
				}
			}
			.index-pv1 .animation-box {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				z-index: initial;
			}
			
			.index-pv1 .animation-box:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, -5px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
				z-index: 1;
			}
			
			.index-pv1 .animation-box img {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
			}
			
			.index-pv1 .animation-box img:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
			}
			.list22 {
				margin: 30px auto;
				overflow: hidden;
				display: block;
				width: 100%;
				justify-content: space-between;
				.list-body-left {
					margin: 0 0 20px;
					display: flex;
					width: 100%;
					justify-content: space-between;
					.list-item1 {
						cursor: pointer;
						margin: 0 10px 0 0;
						overflow: hidden;
						display: block;
						width: calc(50% - 10px);
						position: relative;
						height: auto;
						img {
							object-fit: cover;
							display: block;
							width: 100%;
							transition: all 0.3s;
							height: 400px;
						}
						.name {
							padding: 0 0 0 20px;
							z-index: 100;
							background-size: 100%;
							color: #fff;
							bottom: 0;
							display: none;
							font-size: 16px;
							line-height: 40px;
							box-sizing: border-box;
							overflow: hidden;
							left: 0;
							background: rgba(0,0,0,.2);
							width: 100%;
							position: absolute;
							height: 40px;
						}
					}
					.list-item1:hover {
						img {
							transform: scale(1.05);
						}
						.name {
						}
					}
					.list-item2 {
						cursor: pointer;
						margin: 0 0 0 10px;
						display: flex;
						width: calc(50% - 10px);
						.img {
							z-index: 50;
							overflow: hidden;
							width: 50%;
							position: relative;
							height: auto;
							img {
								object-fit: cover;
								display: block;
								width: 100%;
								transition: all 0.3s;
								height: 400px;
							}
						}
						.infoBox {
							padding: 0 11px 0 19px;
							z-index: 100;
							align-content: center;
							background: #fff;
							display: flex;
							width: 50%;
							align-items: center;
							position: relative;
							flex-wrap: wrap;
							height: 100%;
							.name {
								overflow: hidden;
								color: #404040;
								white-space: hidden;
								font-weight: 900;
								width: 100%;
								font-size: 16px;
								line-height: 30px;
								text-overflow: ellipsis;
							}
							.price {
								color: #f00;
								font-size: 16px;
								line-height: 40px;
							}
							.desc {
								padding: 0;
								overflow: hidden;
								color: #808080;
								white-space: nowrap;
								width: 100%;
								font-size: 15px;
								line-height: 30px;
								text-overflow: ellipsis;
								height: 30px;
							}
							.bottom {
								margin: 20px 0 0;
								overflow: hidden;
								display: flex;
								width: 100%;
								justify-content: space-between;
								.publisher {
									color: #747474;
									width: calc(100% - 90px);
									font-size: 12px;
								}
								.time {
									color: #747474;
									display: inline;
									width: 80px;
									font-size: 12px;
									line-height: 28px;
									text-align: right;
									height: 28px;
								}
							}
							.jian {
								margin: -7px 0 0;
								clip-path: polygon(100% 1%, 100% 100%, 0% 50%);
								top: 50%;
								left: -8px;
								background: #f6f6f6;
								width: 9px;
								position: absolute;
								height: 14px;
							}
						}
					}
					.list-item2:hover {
						.img {
							img {
								transform: scale(1.05);
							}
						}
						.infoBox {
							background: rgba(64, 158, 255,1);
							.name {
								color: #fff;
							}
							.price {
								color: #fff;
							}
							.desc {
								color: #fff;
							}
							.bottom {
								.publisher {
									color: #fff;
								}
								.time {
									color: #fff;
								}
							}
							.jian {
								background: rgba(64, 158, 255,1);
							}
						}
					}
				}
				.list-body-right {
					display: flex;
					width: 100%;
					justify-content: space-between;
					.list-item1 {
						cursor: pointer;
						margin: 0;
						display: flex;
						width: calc(33% - 10px);
						.img {
							z-index: 50;
							overflow: hidden;
							width: 50%;
							position: relative;
							height: auto;
							img {
								object-fit: cover;
								display: block;
								width: 100%;
								transition: all 0.3s;
								height: 240px;
							}
						}
						.infoBox {
							padding: 15px;
							z-index: 100;
							align-content: center;
							background: #f5f5f5;
							display: flex;
							width: 50%;
							align-items: center;
							position: relative;
							flex-wrap: wrap;
							height: 240px;
							.name {
								overflow: hidden;
								color: #333;
								white-space: nowrap;
								font-weight: 600;
								width: 100%;
								font-size: 16px;
								text-overflow: ellipsis;
							}
							.price {
								color: #f00;
								width: 100%;
								font-size: 16px;
								line-height: 30px;
							}
							.desc {
								padding: 0;
								overflow: hidden;
								color: #808080;
								white-space: nowrap;
								width: 100%;
								font-size: 15px;
								line-height: 30px;
								text-overflow: ellipsis;
								height: 30px;
							}
							.bottom {
								margin: 20px 0 0;
								overflow: hidden;
								display: flex;
								width: 100%;
								justify-content: space-between;
								.publisher {
									color: #747474;
									width: calc(100% - 90px);
									font-size: 12px;
									line-height: 30px;
								}
								.time {
									color: #747474;
									display: inline;
									width: 80px;
									font-size: 12px;
									line-height: 30px;
									text-align: right;
									height: 30px;
								}
							}
							.jian {
								margin: -7px 0 0;
								clip-path: polygon(100% 1%, 100% 100%, 0% 50%);
								top: 50%;
								left: -8px;
								background: #f6f6f6;
								width: 9px;
								position: absolute;
								height: 14px;
							}
						}
					}
					.list-item1:hover {
						.img {
							img {
								transform: scale(1.05);
							}
						}
						.infoBox {
							background: rgba(64, 158, 255,1);
							.name {
								color: #fff;
							}
							.price {
								color: #fff;
							}
							.desc {
								color: #fff;
							}
							.bottom {
								.publisher {
									color: #fff;
								}
								.time {
									color: #fff;
								}
							}
							.jian {
								background: rgba(64, 158, 255,1);
							}
						}
					}
					.list-item2 {
						cursor: pointer;
						margin: 0;
						display: flex;
						width: calc(34% - 20px);
						.img {
							z-index: 50;
							overflow: hidden;
							width: 50%;
							position: relative;
							height: auto;
							img {
								object-fit: cover;
								display: block;
								width: 100%;
								transition: all 0.3s;
								height: 240px;
							}
						}
						.infoBox {
							padding: 15px;
							z-index: 100;
							align-content: center;
							background: #f5f5f5;
							display: flex;
							width: 50%;
							align-items: center;
							position: relative;
							flex-wrap: wrap;
							height: 240px;
							order: 2;
							.name {
								overflow: hidden;
								color: #333;
								white-space: nowrap;
								font-weight: 600;
								width: 100%;
								font-size: 16px;
								text-overflow: ellipsis;
							}
							.price {
								color: #f00;
								width: 100%;
								font-size: 16px;
								line-height: 30px;
							}
							.desc {
								padding: 0;
								overflow: hidden;
								color: #808080;
								white-space: nowrap;
								width: 100%;
								font-size: 15px;
								line-height: 30px;
								text-overflow: ellipsis;
								height: 30px;
							}
							.bottom {
								margin: 20px 0 0;
								overflow: hidden;
								display: flex;
								width: 100%;
								justify-content: space-between;
								.publisher {
									color: #747474;
									width: calc(100% - 90px);
									font-size: 12px;
								}
								.time {
									color: #747474;
									display: inline;
									width: 80px;
									font-size: 12px;
									line-height: 28px;
									text-align: right;
									height: 28px;
								}
							}
							.jian {
								margin: -7px 0 0;
								clip-path: polygon(100% 1%, 100% 100%, 0% 50%);
								top: 50%;
								left: -8px;
								background: #f6f6f6;
								width: 9px;
								position: absolute;
								height: 14px;
							}
						}
					}
					.list-item2:hover {
						.img {
							img {
								transform: scale(1.05);
							}
						}
						.infoBox {
							background: rgba(64, 158, 255,1);
							.name {
								color: #fff;
							}
							.price {
								color: #fff;
							}
							.desc {
								color: #fff;
							}
							.bottom {
								.publisher {
									color: #fff;
								}
								.time {
									color: #fff;
								}
							}
							.jian {
								background: rgba(64, 158, 255,1);
							}
						}
					}
					.list-item3 {
						cursor: pointer;
						margin: 0;
						display: flex;
						width: calc(33% - 10px);
						.img {
							z-index: 50;
							overflow: hidden;
							width: 50%;
							position: relative;
							height: auto;
							img {
								object-fit: cover;
								display: block;
								width: 100%;
								transition: all 0.3s;
								height: 240px;
							}
						}
						.infoBox {
							padding: 15px;
							z-index: 100;
							align-content: center;
							background: #f5f5f5;
							display: flex;
							width: 50%;
							align-items: center;
							position: relative;
							flex-wrap: wrap;
							height: 240px;
							.name {
								overflow: hidden;
								color: #333;
								white-space: nowrap;
								font-weight: 600;
								width: 100%;
								font-size: 16px;
								text-overflow: ellipsis;
							}
							.price {
								color: #f00;
								width: 100%;
								font-size: 16px;
								line-height: 30px;
							}
							.desc {
								padding: 0;
								overflow: hidden;
								color: #808080;
								white-space: nowrap;
								width: 100%;
								font-size: 15px;
								line-height: 30px;
								text-overflow: ellipsis;
								height: 30px;
							}
							.bottom {
								margin: 20px 0 0;
								overflow: hidden;
								display: flex;
								width: 100%;
								justify-content: space-between;
								.publisher {
									color: #747474;
									width: calc(100% - 90px);
									font-size: 12px;
								}
								.time {
									color: #747474;
									display: inline;
									width: 80px;
									font-size: 12px;
									line-height: 28px;
									text-align: right;
									height: 28px;
								}
							}
							.jian {
								margin: -7px 0 0;
								clip-path: polygon(100% 1%, 100% 100%, 0% 50%);
								top: 50%;
								left: -8px;
								background: #f6f6f6;
								width: 9px;
								position: absolute;
								height: 14px;
							}
						}
					}
					.list-item3:hover {
						.img {
							img {
								transform: scale(1.05);
							}
						}
						.infoBox {
							background: rgba(64, 158, 255,1);
							.name {
								color: #fff;
							}
							.price {
								color: #fff;
							}
							.desc {
								color: #fff;
							}
							.bottom {
								.publisher {
									color: #fff;
								}
								.time {
									color: #fff;
								}
							}
							.jian {
								background: rgba(64, 158, 255,1);
							}
						}
					}
				}
			}
			.moreBtn {
				border: 0px solid #ddd;
				cursor: pointer;
				border-radius: 0px;
				margin: 0px auto;
				background: #6aac5a;
				display: none;
				width: 120px;
				line-height: 40px;
				justify-content: center;
				text-align: center;
				.text {
					margin: 0 5px 0 0;
					color: #fff;
					font-size: 16px;
					order: 2;
				}
				.icon {
					color: #999;
					background: none;
					display: none;
					width: 23px;
					font-size: 16px;
					height: 7px;
				}
			}
		}
	}
</style>
