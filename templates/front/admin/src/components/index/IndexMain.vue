<template>
	<div style="height: 100%;">
		<el-main :style='"horizontal" == "vertical" ? (2 == 1 ? {"minHeight":"100%","padding":"0","margin":"0 0 0 210px","position":"relative","display":"block"} : (2 == 2 ? (isCollapse ? {"minHeight":"100%","padding":"0 0 0 140px","margin":"0","position":"relative","background":"#fafafe","display":"block"} : {"minHeight":"100%","padding":"0","margin":"0 0 0 230px","position":"relative","background":"url(http://codegen.caihongy.cn/20250826/9c566af26d2e4baca85799a2893fb657.png) no-repeat center center / 100% 100%","display":"block"}) : "")) : {"minHeight":"100%","margin":"0","position":"relative"}'>
			<!-- top -->
			<index-header :style='{"padding":"0 30px","margin":"0 auto","alignItems":"center","color":"#333","background":"url(http://codegen.caihongy.cn/20250914/1ff7e58330814edd82aff3df8135ae0d.png) no-repeat center center / 100% 100%","display":"flex","width":"100%","fontSize":"16px","position":"relative","justifyContent":"space-between","zIndex":"9","height":"80px"}'></index-header>
			
			<!-- menu -->
			<template v-if="'horizontal' == 'vertical'">
			  <template v-if="2 == 1">
				<index-aside :style='{"boxShadow":"1px 0 6px  rgba(64, 158, 255, .3)","overflow":"hidden","top":"0","left":"0","background":"#304156","bottom":"0","width":"210px","fontSize":"0px","position":"fixed","height":"100%","zIndex":"1001"}'></index-aside>
			  </template>
			  <template v-if="2 == 2">
				<index-aside :is-collapse="isCollapse" @oncollapsechange="collapseChange" :style='isCollapse ? {"boxShadow":"1px 0 0px  #e7e8fc","overflow":"hidden","top":"81px","left":"0","background":"#fff","bottom":"0","width":"140px","position":"fixed","transition":"width 0.3s","height":"100%","zIndex":"1001"} : {"boxShadow":"0px 0 0px  #ddd","padding":"0px 0 0 0","bottom":"0","transition":"width 0.3s","overflow":"hidden","top":"0","borderRadius":"0","left":"0","background":"#DCEAF7","width":"230px","position":"fixed","height":"100%","zIndex":"1001"}'></index-aside>
			  </template>
			</template>
			<template v-if="'horizontal' == 'horizontal'">
			  <template v-if="2 == 1">
				<index-aside :style='{"width":"100%","borderColor":"#efefef","borderStyle":"solid","background":"#304156","borderWidth":"0 0 1px 0","height":"auto"}'></index-aside>
			  </template>
			  <template v-if="2 == 2">
				<index-aside :style='{"padding":"0 20px","borderColor":"#efefef","flexWrap":"wrap","background":"#DCEAF7","borderWidth":"0","display":"flex","width":"100%","borderStyle":"solid","height":"auto"}'></index-aside>
			  </template>
			</template>
			
			<!-- breadcrumb -->
			<bread-crumbs :title="title" :style='{"padding":"14px 30px","margin":"0","borderColor":"#DCEAF7","background":"#F0F7FD","borderWidth":"0 30px 0 30px","width":"calc(100% - 60px)","borderStyle":"solid"}' class="bread-crumbs"></bread-crumbs>
			
			<!-- TagsView -->
			<tags-view />
			<router-view class="router-view"></router-view>
		</el-main>
	</div>
</template>

<script>
	import IndexAside from '@/components/index/IndexAsideStatic'
	import IndexHeader from '@/components/index/IndexHeader'
	import TagsView from '@/components/index/TagsView'
	import menu from "@/utils/menu";
	export default {
		components: {
			IndexAside,
			IndexHeader,
			TagsView
		},
		data() {
			return {
				menuList: [],
				role: "",
				currentIndex: -2,
				itemMenu: [],
				title: '',
				isCollapse: false,
			};
		},
		mounted() {
			let menus = menu.list();
			this.menuList = menus;
			this.role = this.$storage.get("role");
		},
		created() {
			this.init();
		},
		methods: {
			init(){
				this.$nextTick(()=>{
					
				})
			},
			collapseChange(collapse) {
				this.isCollapse = collapse
			},
			menuHandler(menu) {
				this.$router.push({
					name: menu.tableName
				});
				this.title = menu.menu;
			},
			titleChange(index, menus) {
				this.currentIndex = index
				this.itemMenu = menus;
			},
			homeChange(index) {
				this.itemMenu = [];
				this.title = ""
				this.currentIndex = index
				this.$router.push({
					name: 'home'
				});
			},
			centerChange(index) {
				this.itemMenu = [{
					"buttons": ["新增", "查看", "修改", "删除"],
					"menu": "修改密码",
					"tableName": "updatePassword"
				}, {
					"buttons": ["新增", "查看", "修改", "删除"],
					"menu": "个人信息",
					"tableName": "center"
				}];
				this.title = ""
				this.currentIndex = index
				this.$router.push({
					name: 'home'
				});
				
			}
		}
	};
</script>
<style lang="scss" scoped>
	a {
		text-decoration: none;
		color: #555;
	}

	a:hover {
		background: #00c292;
	}
	
	.el-main {
		padding: 0;
		display: block;
	}

	.nav-list {
		width: 100%;
		margin: 0 auto;
		text-align: left;
		margin-top: 20px;

		.nav-title {
			display: inline-block;
			font-size: 15px;
			color: #333;
			padding: 15px 25px;
			border: none;
		}

		.nav-title.active {
			color: #555;
			cursor: default;
			background-color: #fff;
		}
	}

	.nav-item {
		margin-top: 20px;
		background: #FFFFFF;
		padding: 15px 0;

		.menu {
			padding: 15px 25px;
		}
	}
	
	.detail-form-content {
	    background: transparent;
	}
</style>
