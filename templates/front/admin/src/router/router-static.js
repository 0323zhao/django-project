	import Vue from 'vue';
//配置路由
	import VueRouter from 'vue-router'
	Vue.use(VueRouter);
//1.创建组件
	import Index from '@/views/index'
	import Home from '@/views/home'
	import Board from '@/views/board'
	import Login from '@/views/login'
	import NotFound from '@/views/404'
	import UpdatePassword from '@/views/update-password'
	import pay from '@/views/pay'
	import register from '@/views/register'
	import center from '@/views/center'
	import bloginfo from '@/views/modules/bloginfo/list'
	import blogcomment from '@/views/modules/blogcomment/list'
	import yonghu from '@/views/modules/yonghu/list'
	import bloginfoforecast from '@/views/modules/bloginfoforecast/list'
	import pinglunfenxi from '@/views/modules/pinglunfenxi/list'
	import xitonggonggao from '@/views/modules/xitonggonggao/list'
	import forum from '@/views/modules/forum/list'
	import syslog from '@/views/modules/syslog/list'
	import smsregistercode from '@/views/modules/smsregistercode/list'
	import users from '@/views/modules/users/list'
	import discussbloginfo from '@/views/modules/discussbloginfo/list'
	import discussblogcomment from '@/views/modules/discussblogcomment/list'
import config from '@/views/modules/config/list'

//2.配置路由   注意：名字
export const routes = [{
	path: '/',
	name: '系统首页',
	component: Index,
	children: [{
		// 这里不设置值，是把main作为默认页面
		path: '/',
		name: '系统首页',
		component: Home,
		meta: {icon:'', title:'center', affix: true}
	}, {
		path: '/updatePassword',
		name: '修改密码',
		component: UpdatePassword,
		meta: {icon:'', title:'updatePassword'}
	}, {
		path: '/pay',
		name: '支付',
		component: pay,
		meta: {icon:'', title:'pay'}
	}, {
		path: '/center',
		name: '个人信息',
		component: center,
		meta: {icon:'', title:'center'}
	}
	,{
		path: '/bloginfo',
		name: '博文信息',
		component: bloginfo
	}
	,{
		path: '/bloginfostat',
		name: '博文信息统计',
		component: bloginfo
	}
	,{
		path: '/blogcomment',
		name: '博文评论',
		component: blogcomment
	}
	,{
		path: '/blogcommentstat',
		name: '博文评论统计',
		component: blogcomment
	}
	,{
		path: '/yonghu',
		name: '用户',
		component: yonghu
	}
	,{
		path: '/bloginfoforecast',
		name: '转发预测',
		component: bloginfoforecast
	}
	,{
		path: '/pinglunfenxi',
		name: '评论分析',
		component: pinglunfenxi
	}
	,{
		path: '/pinglunfenxistat',
		name: '评论分析统计',
		component: pinglunfenxi
	}
	,{
		path: '/xitonggonggao',
		name: '系统公告',
		component: xitonggonggao
	}
	,{
		path: '/forum',
		name: '论坛',
		component: forum
	}
	,{
		path: '/syslog',
		name: '系统日志',
		component: syslog
	}
	,{
		path: '/smsregistercode',
		name: '短信验证码',
		component: smsregistercode
	}
	,{
		path: '/users',
		name: '管理员',
		component: users
	}
	,{
		path: '/discussbloginfo',
		name: '博文信息',
		component: discussbloginfo
	}
	,{
		path: '/discussblogcomment',
		name: '博文评论',
		component: discussblogcomment
	}
	,{
		path: '/config/:type',
		name: '配置管理',
		component: config
	}
	]
	},
	{
		path: '/login',
		name: 'login',
		component: Login,
		meta: {icon:'', title:'login'}
	},
	{
		path: '/board',
		name: 'board',
		component: Board,
		meta: {icon:'', title:'board'}
	},
	{
		path: '/register',
		name: 'register',
		component: register,
		meta: {icon:'', title:'register'}
	},
	{
		path: '*',
		component: NotFound
	}
]
//3.实例化VueRouter  注意：名字
const router = new VueRouter({
	mode: 'hash',
	/*hash模式改为history*/
	routes // （缩写）相当于 routes: routes
})
const originalPush = VueRouter.prototype.push
//修改原型对象中的push方法
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}
export default router;
