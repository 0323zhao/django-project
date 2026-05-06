#coding:utf-8
from django.db import models

from .model import BaseModel

from datetime import datetime



class bloginfo(BaseModel):
    __doc__ = u'''bloginfo'''
    __tablename__ = 'bloginfo'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='是'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='用协'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='是'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    screenname=models.CharField ( max_length=255, null=True, unique=False, verbose_name='博主' )
    mblogtext=models.TextField   (  null=True, unique=False, verbose_name='博文' )
    commentscount=models.IntegerField  (  null=True, unique=False, verbose_name='评论数' )
    repostscount=models.IntegerField  (  null=True, unique=False, verbose_name='转发数' )
    attitudescount=models.IntegerField  (  null=True, unique=False, verbose_name='点赞数' )
    fbtime=models.CharField ( max_length=255, null=True, unique=False, verbose_name='发布时间' )
    medias=models.CharField ( max_length=255, null=True, unique=False, verbose_name='媒体' )
    userurl=models.TextField   (  null=True, unique=False, verbose_name='主页地址' )
    thumbsupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='赞' )
    crazilynum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='踩' )
    clicktime=models.DateTimeField  (auto_now=True,  null=True, unique=False, verbose_name='最近点击时间' )
    clicknum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='点击次数' )
    discussnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='评论数' )
    storeupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='收藏数' )
    sentiment = models.CharField(max_length=10, null=True, verbose_name='情感倾向')
    sentiment_score = models.FloatField(null=True, verbose_name='情感置信度')
    has_image = models.BooleanField(default=False, verbose_name='是否含图')
    has_video = models.BooleanField(default=False, verbose_name='是否含视频')
    has_link = models.BooleanField(default=False, verbose_name='是否含链接')
    has_topic = models.BooleanField(default=False, verbose_name='是否含话题')
    has_mention = models.BooleanField(default=False, verbose_name='是否@人')
    publish_hour = models.IntegerField(null=True, verbose_name='发布小时')
    publish_weekday = models.IntegerField(null=True, verbose_name='发布星期')
    weibo_id = models.BigIntegerField(null=True, verbose_name='微博博文ID')
    '''
    screenname=VARCHAR
    mblogtext=Text
    commentscount=Integer
    repostscount=Integer
    attitudescount=Integer
    fbtime=VARCHAR
    medias=VARCHAR
    userurl=Text
    thumbsupnum=Integer
    crazilynum=Integer
    clicktime=DateTime
    clicknum=Integer
    discussnum=Integer
    storeupnum=Integer
    '''
    class Meta:
        db_table = 'bloginfo'
        verbose_name = verbose_name_plural = '博文信息'
class blogcomment(BaseModel):
    __doc__ = u'''blogcomment'''
    __tablename__ = 'blogcomment'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='是'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='是'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    detailurl=models.TextField   (  null=True, unique=False, verbose_name='详情地址' )
    pluser=models.CharField ( max_length=255, null=True, unique=False, verbose_name='评论人' )
    plcontent=models.TextField   (  null=True, unique=False, verbose_name='评论内容' )
    likecount=models.IntegerField  (  null=True, unique=False, verbose_name='支持数' )
    fbplace=models.CharField ( max_length=255, null=True, unique=False, verbose_name='发布地' )
    pltime=models.CharField ( max_length=255, null=True, unique=False, verbose_name='评论时间' )
    thumbsupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='赞' )
    crazilynum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='踩' )
    clicknum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='点击次数' )
    discussnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='评论数' )
    storeupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='收藏数' )
    blog_id = models.BigIntegerField(null=True, verbose_name='关联博文ID')
    sentiment = models.CharField(max_length=10, null=True, verbose_name='情感倾向')
    sentiment_score = models.FloatField(null=True, verbose_name='情感置信度')
    '''
    detailurl=Text
    pluser=VARCHAR
    plcontent=Text
    likecount=Integer
    fbplace=VARCHAR
    pltime=VARCHAR
    thumbsupnum=Integer
    crazilynum=Integer
    clicknum=Integer
    discussnum=Integer
    storeupnum=Integer
    '''
    class Meta:
        db_table = 'blogcomment'
        verbose_name = verbose_name_plural = '博文评论'
class yonghu(BaseModel):
    __doc__ = u'''yonghu'''
    __tablename__ = 'yonghu'

    __loginUser__='yonghuzhanghao'


    __authTables__={}
    __authPeople__='是'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __loginUserColumn__='yonghuzhanghao'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    yonghuzhanghao=models.CharField ( max_length=255,null=False,unique=True, verbose_name='用户账号' )
    mima=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码' )
    yonghuxingming=models.CharField ( max_length=255,null=False, unique=False, verbose_name='用户姓名' )
    touxiang=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    xingbie=models.CharField ( max_length=255, null=True, unique=False, verbose_name='性别' )
    mobile=models.CharField ( max_length=255, null=True, unique=False, verbose_name='手机号' )
    status=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='状态' )
    '''
    yonghuzhanghao=VARCHAR
    mima=VARCHAR
    yonghuxingming=VARCHAR
    touxiang=Text
    xingbie=VARCHAR
    mobile=VARCHAR
    status=Integer
    '''
    class Meta:
        db_table = 'yonghu'
        verbose_name = verbose_name_plural = '用户'
class bloginfoforecast(BaseModel):
    __doc__ = u'''bloginfoforecast'''
    __tablename__ = 'bloginfoforecast'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    screenname=models.CharField ( max_length=255, null=True, unique=False, verbose_name='博主' )
    commentscount=models.IntegerField  (  null=True, unique=False, verbose_name='评论数' )
    medias=models.CharField ( max_length=255, null=True, unique=False, verbose_name='媒体' )
    repostscount=models.IntegerField  (  null=True, unique=False, verbose_name='转发数' )
    '''
    screenname=VARCHAR
    commentscount=Integer
    medias=VARCHAR
    repostscount=Integer
    '''
    class Meta:
        db_table = 'bloginfoforecast'
        verbose_name = verbose_name_plural = '转发预测'
class pinglunfenxi(BaseModel):
    __doc__ = u'''pinglunfenxi'''
    __tablename__ = 'pinglunfenxi'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    plcontent=models.TextField   (  null=True, unique=False, verbose_name='评论内容' )
    qingganfenxi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='情感分析' )
    '''
    plcontent=Text
    qingganfenxi=VARCHAR
    '''
    class Meta:
        db_table = 'pinglunfenxi'
        verbose_name = verbose_name_plural = '评论分析'
class xitonggonggao(BaseModel):
    __doc__ = u'''xitonggonggao'''
    __tablename__ = 'xitonggonggao'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='是'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    gonggaobiaoti=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公告标题' )
    gonggaofenlei=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公告分类' )
    fengmian=models.TextField   (  null=True, unique=False, verbose_name='封面' )
    fabushijian=models.DateTimeField  (  null=True, unique=False, verbose_name='发布时间' )
    jianjie=models.TextField   (  null=True, unique=False, verbose_name='简介' )
    gonggaoneirong=models.TextField   (  null=True, unique=False, verbose_name='公告内容' )
    thumbsupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='赞' )
    crazilynum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='踩' )
    storeupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='收藏数' )
    '''
    gonggaobiaoti=VARCHAR
    gonggaofenlei=VARCHAR
    fengmian=Text
    fabushijian=DateTime
    jianjie=Text
    gonggaoneirong=Text
    thumbsupnum=Integer
    crazilynum=Integer
    storeupnum=Integer
    '''
    class Meta:
        db_table = 'xitonggonggao'
        verbose_name = verbose_name_plural = '系统公告'
class forum(BaseModel):
    __doc__ = u'''forum'''
    __tablename__ = 'forum'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='是'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='是'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    content=models.TextField   ( null=False, unique=False, verbose_name='帖子内容' )
    parentid=models.BigIntegerField  (  null=True, unique=False, verbose_name='父节点id' )
    username=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户名' )
    avatarurl=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    isdone=models.CharField ( max_length=255, null=True, unique=False, verbose_name='状态' )
    istop=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='是否置顶' )
    toptime=models.DateTimeField  (  null=True, unique=False, verbose_name='置顶时间' )
    cover=models.TextField   (  null=True, unique=False, verbose_name='封面' )
    isanon=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='是否匿名' )
    delflag=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='是否删除' )
    title=models.CharField ( max_length=255, null=True, unique=False, verbose_name='帖子标题' )
    userid=models.BigIntegerField  (  null=True, unique=False, verbose_name='用户id' )
    '''
    content=Text
    parentid=BigInteger
    username=VARCHAR
    avatarurl=Text
    isdone=VARCHAR
    istop=Integer
    toptime=DateTime
    cover=Text
    isanon=Integer
    delflag=Integer
    title=VARCHAR
    userid=BigInteger
    '''
    class Meta:
        db_table = 'forum'
        verbose_name = verbose_name_plural = '论坛'
class syslog(BaseModel):
    __doc__ = u'''syslog'''
    __tablename__ = 'syslog'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    username=models.CharField ( max_length=255,null=False, unique=False, verbose_name='用户名' )
    operation=models.CharField ( max_length=255,null=False, unique=False, verbose_name='用户操作' )
    method=models.CharField ( max_length=255, null=True, unique=False, verbose_name='请求方法' )
    params=models.TextField   (  null=True, unique=False, verbose_name='请求参数' )
    time=models.BigIntegerField  (  null=True, unique=False, verbose_name='请求时长(毫秒)' )
    ip=models.CharField ( max_length=255, null=True, unique=False, verbose_name='IP地址' )
    '''
    username=VARCHAR
    operation=VARCHAR
    method=VARCHAR
    params=Text
    time=BigInteger
    ip=VARCHAR
    '''
    class Meta:
        db_table = 'syslog'
        verbose_name = verbose_name_plural = '系统日志'
class storeup(BaseModel):
    __doc__ = u'''storeup'''
    __tablename__ = 'storeup'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户id' )
    refid=models.BigIntegerField  (  null=True, unique=False, verbose_name='商品id' )
    tablename=models.CharField ( max_length=255, null=True, unique=False, verbose_name='表名' )
    name=models.CharField ( max_length=255,null=False, unique=False, verbose_name='名称' )
    picture=models.TextField   (  null=True, unique=False, verbose_name='图片' )
    type=models.CharField ( max_length=255, null=True, unique=False,default='1', verbose_name='类型' )
    inteltype=models.CharField ( max_length=255, null=True, unique=False, verbose_name='推荐类型' )
    remark=models.CharField ( max_length=255, null=True, unique=False, verbose_name='备注' )
    '''
    userid=BigInteger
    refid=BigInteger
    tablename=VARCHAR
    name=VARCHAR
    picture=Text
    type=VARCHAR
    inteltype=VARCHAR
    remark=VARCHAR
    '''
    class Meta:
        db_table = 'storeup'
        verbose_name = verbose_name_plural = '收藏表'
class smsregistercode(BaseModel):
    __doc__ = u'''smsregistercode'''
    __tablename__ = 'smsregistercode'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    mobile=models.CharField ( max_length=255,null=False, unique=False, verbose_name='手机' )
    role=models.CharField ( max_length=255,null=False, unique=False, verbose_name='角色' )
    code=models.CharField ( max_length=255,null=False, unique=False, verbose_name='验证码' )
    '''
    mobile=VARCHAR
    role=VARCHAR
    code=VARCHAR
    '''
    class Meta:
        db_table = 'smsregistercode'
        verbose_name = verbose_name_plural = '短信验证码'
class users(BaseModel):
    __doc__ = u'''users'''
    __tablename__ = 'users'



    __authTables__={}
    __authPeople__ = '是'
    __isAdmin__ = '是'
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    username=models.CharField ( max_length=255,null=False, unique=False, verbose_name='用户名' )
    password=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码' )
    role=models.CharField ( max_length=255, null=True, unique=False,default='管理员', verbose_name='角色' )
    image=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    '''
    username=VARCHAR
    password=VARCHAR
    role=VARCHAR
    image=Text
    '''
    class Meta:
        db_table = 'users'
        verbose_name = verbose_name_plural = '管理员'
class discussbloginfo(BaseModel):
    __doc__ = u'''discussbloginfo'''
    __tablename__ = 'discussbloginfo'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    refid=models.BigIntegerField  ( null=False, unique=False, verbose_name='关联表id' )
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户id' )
    avatarurl=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    nickname=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户名' )
    content=models.TextField   ( null=False, unique=False, verbose_name='评论内容' )
    reply=models.TextField   (  null=True, unique=False, verbose_name='回复内容' )
    thumbsupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='赞' )
    crazilynum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='踩' )
    istop=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='置顶(1:置顶,0:非置顶)' )
    tuserids=models.TextField   (  null=True, unique=False, verbose_name='赞用户ids' )
    cuserids=models.TextField   (  null=True, unique=False, verbose_name='踩用户ids' )
    '''
    refid=BigInteger
    userid=BigInteger
    avatarurl=Text
    nickname=VARCHAR
    content=Text
    reply=Text
    thumbsupnum=Integer
    crazilynum=Integer
    istop=Integer
    tuserids=Text
    cuserids=Text
    '''
    class Meta:
        db_table = 'discussbloginfo'
        verbose_name = verbose_name_plural = '博文信息'
class discussblogcomment(BaseModel):
    __doc__ = u'''discussblogcomment'''
    __tablename__ = 'discussblogcomment'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    refid=models.BigIntegerField  ( null=False, unique=False, verbose_name='关联表id' )
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户id' )
    avatarurl=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    nickname=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户名' )
    content=models.TextField   ( null=False, unique=False, verbose_name='评论内容' )
    reply=models.TextField   (  null=True, unique=False, verbose_name='回复内容' )
    thumbsupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='赞' )
    crazilynum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='踩' )
    istop=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='置顶(1:置顶,0:非置顶)' )
    tuserids=models.TextField   (  null=True, unique=False, verbose_name='赞用户ids' )
    cuserids=models.TextField   (  null=True, unique=False, verbose_name='踩用户ids' )
    '''
    refid=BigInteger
    userid=BigInteger
    avatarurl=Text
    nickname=VARCHAR
    content=Text
    reply=Text
    thumbsupnum=Integer
    crazilynum=Integer
    istop=Integer
    tuserids=Text
    cuserids=Text
    '''
    class Meta:
        db_table = 'discussblogcomment'
        verbose_name = verbose_name_plural = '博文评论'


class blogger_profile(BaseModel):
    __tablename__ = 'blogger_profile'
    screenname = models.CharField(max_length=255, unique=True, verbose_name='博主名')
    followers_count = models.IntegerField(default=0, verbose_name='粉丝数')
    friends_count = models.IntegerField(default=0, verbose_name='关注数')
    statuses_count = models.IntegerField(default=0, verbose_name='微博数')
    verified = models.BooleanField(default=False, verbose_name='是否认证')
    verified_reason = models.CharField(max_length=255, null=True, verbose_name='认证信息')
    avg_reposts = models.FloatField(default=0, verbose_name='平均转发数')
    avg_comments = models.FloatField(default=0, verbose_name='平均评论数')
    avg_attitudes = models.FloatField(default=0, verbose_name='平均点赞数')

    class Meta:
        db_table = 'blogger_profile'
        verbose_name = verbose_name_plural = '博主画像'
class SeedBlogger(BaseModel):
    __tablename__ = 'seed_blogger'
    uid = models.BigIntegerField(unique=True, verbose_name='博主UID')
    screenname = models.CharField(max_length=255, null=True, verbose_name='博主昵称（可选）')
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'seed_blogger'
        verbose_name = verbose_name_plural = '种子博主'