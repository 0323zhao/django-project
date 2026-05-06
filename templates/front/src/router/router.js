import VueRouter from 'vue-router'
//引入组件
import Index from '../pages'
import Home from '../pages/home/home'
import Login from '../pages/login/login'
import Register from '../pages/register/register'
import Center from '../pages/center/center'
import Storeup from '../pages/storeup/list'
import payList from '../pages/pay'

import bloginfoList from '../pages/bloginfo/list'
import bloginfoDetail from '../pages/bloginfo/detail'
import bloginfoAdd from '../pages/bloginfo/add'
import blogcommentList from '../pages/blogcomment/list'
import blogcommentDetail from '../pages/blogcomment/detail'
import blogcommentAdd from '../pages/blogcomment/add'
import yonghuList from '../pages/yonghu/list'
import yonghuDetail from '../pages/yonghu/detail'
import yonghuAdd from '../pages/yonghu/add'
import bloginfoforecastList from '../pages/bloginfoforecast/list'
import bloginfoforecastDetail from '../pages/bloginfoforecast/detail'
import bloginfoforecastAdd from '../pages/bloginfoforecast/add'
import pinglunfenxiList from '../pages/pinglunfenxi/list'
import pinglunfenxiDetail from '../pages/pinglunfenxi/detail'
import pinglunfenxiAdd from '../pages/pinglunfenxi/add'
import xitonggonggaoList from '../pages/xitonggonggao/list'
import xitonggonggaoDetail from '../pages/xitonggonggao/detail'
import xitonggonggaoAdd from '../pages/xitonggonggao/add'
import Forum from '../pages/forum/list'
import ForumAdd from '../pages/forum/add'
import ForumDetail from '../pages/forum/detail'
import MyForumList from '../pages/forum/myForumList'
import smsregistercodeList from '../pages/smsregistercode/list'
import smsregistercodeDetail from '../pages/smsregistercode/detail'
import smsregistercodeAdd from '../pages/smsregistercode/add'
import discussbloginfoList from '../pages/discussbloginfo/list'
import discussbloginfoDetail from '../pages/discussbloginfo/detail'
import discussbloginfoAdd from '../pages/discussbloginfo/add'
import discussblogcommentList from '../pages/discussblogcomment/list'
import discussblogcommentDetail from '../pages/discussblogcomment/detail'
import discussblogcommentAdd from '../pages/discussblogcomment/add'

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}

//配置路由
export default new VueRouter({
	routes:[
		{
      path: '/',
      redirect: '/index/home'
    },
		{
			path: '/index',
			component: Index,
			children:[
				{
					path: 'home',
					component: Home
				},
				{
					path: 'center',
					component: Center,
				},
				{
					path: 'pay',
					component: payList,
				},
				{
					path: 'storeup',
					component: Storeup
				},
				{
					path: 'bloginfo',
					component: bloginfoList
				},
				{
					path: 'bloginfoDetail',
					component: bloginfoDetail
				},
				{
					path: 'bloginfoAdd',
					component: bloginfoAdd
				},
				{
					path: 'blogcomment',
					component: blogcommentList
				},
				{
					path: 'blogcommentDetail',
					component: blogcommentDetail
				},
				{
					path: 'blogcommentAdd',
					component: blogcommentAdd
				},
				{
					path: 'yonghu',
					component: yonghuList
				},
				{
					path: 'yonghuDetail',
					component: yonghuDetail
				},
				{
					path: 'yonghuAdd',
					component: yonghuAdd
				},
				{
					path: 'bloginfoforecast',
					component: bloginfoforecastList
				},
				{
					path: 'bloginfoforecastDetail',
					component: bloginfoforecastDetail
				},
				{
					path: 'bloginfoforecastAdd',
					component: bloginfoforecastAdd
				},
				{
					path: 'pinglunfenxi',
					component: pinglunfenxiList
				},
				{
					path: 'pinglunfenxiDetail',
					component: pinglunfenxiDetail
				},
				{
					path: 'pinglunfenxiAdd',
					component: pinglunfenxiAdd
				},
				{
					path: 'xitonggonggao',
					component: xitonggonggaoList
				},
				{
					path: 'xitonggonggaoDetail',
					component: xitonggonggaoDetail
				},
				{
					path: 'xitonggonggaoAdd',
					component: xitonggonggaoAdd
				},
				{
					path: 'forum',
					component: Forum
				},
				{
					path: 'forumAdd',
					component: ForumAdd
				},
				{
					path: 'forumDetail',
					component: ForumDetail
				},
				{
					path: 'myForumList',
					component: MyForumList
				},
				{
					path: 'smsregistercode',
					component: smsregistercodeList
				},
				{
					path: 'smsregistercodeDetail',
					component: smsregistercodeDetail
				},
				{
					path: 'smsregistercodeAdd',
					component: smsregistercodeAdd
				},
				{
					path: 'discussbloginfo',
					component: discussbloginfoList
				},
				{
					path: 'discussbloginfoDetail',
					component: discussbloginfoDetail
				},
				{
					path: 'discussbloginfoAdd',
					component: discussbloginfoAdd
				},
				{
					path: 'discussblogcomment',
					component: discussblogcommentList
				},
				{
					path: 'discussblogcommentDetail',
					component: discussblogcommentDetail
				},
				{
					path: 'discussblogcommentAdd',
					component: discussblogcommentAdd
				},
			]
		},
		{
			path: '/login',
			component: Login
		},
		{
			path: '/register',
			component: Register
		},
	]
})
