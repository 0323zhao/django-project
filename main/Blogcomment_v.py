#coding:utf-8
import base64, copy, logging, os, sys, time, xlrd, json, datetime, configparser
from django.http import JsonResponse
from django.apps import apps
import numbers
from collections import defaultdict
import math
from django.db.models.aggregates import Count,Sum
from django.db.models import Case, When, IntegerField, F
from .models import storeup
from django.forms import model_to_dict
import requests
from util.CustomJSONEncoder import CustomJsonEncoder
from .models import blogcomment
from util.codes import *
from urllib.parse import unquote
from util.auth import Auth
from util.common import Common
import util.message as mes
from django.db import connection
import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q
from util.baidubce_api import BaiDuBce
from .config_model import config
import pandas as pd


def blogcomment_default(request):

    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        req_dict.update({"isdefault":"是"})
        data=blogcomment.getbyparams(blogcomment, blogcomment, req_dict)
        if len(data)>0:
            msg['data']  = data[0]
        else:
            msg['data']  = {}
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_page(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        global blogcomment
        #当前登录用户信息
        tablename = Auth().getTokenInfo(request).get('tablename')

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  =blogcomment.page(blogcomment, blogcomment,req_dict, request)
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_autoSort(request):
    '''
    ．智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
主要信息列表（如商品列表，新闻列表）中使用，显示最近点击的或最新添加的5条记录就行
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        if "clicknum"  in blogcomment.getallcolumn(blogcomment,blogcomment):
            req_dict['sort']='clicknum'
        elif "browseduration"  in blogcomment.getallcolumn(blogcomment,blogcomment):
            req_dict['sort']='browseduration'
        else:
            req_dict['sort']='clicktime'
        req_dict['order']='desc'
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = blogcomment.page(blogcomment,blogcomment, req_dict)

        return JsonResponse(msg, encoder=CustomJsonEncoder)

#分类列表
def blogcomment_lists(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":[]}
        msg['data'],_,_,_,_  = blogcomment.page(blogcomment, blogcomment, {})
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_query(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        try:
            query_result = blogcomment.objects.filter(**request.session.get("req_dict")).values()
            msg['data'] = query_result[0]
        except Exception as e:

            msg['code'] = crud_error_code
            msg['msg'] = f"发生错误：{e}"
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_list(request):
    '''
    前台分页
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        #获取全部列名
        columns=  blogcomment.getallcolumn( blogcomment, blogcomment)
        if "vipread" in req_dict and "vipread" not in columns:
          del req_dict["vipread"]
        #表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
        try:
            __foreEndList__=blogcomment.__foreEndList__
        except:
            __foreEndList__=None
        try:
            __foreEndListAuth__=blogcomment.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        #authSeparate
        try:
            __authSeparate__=blogcomment.__authSeparate__
        except:
            __authSeparate__=None

        if __foreEndListAuth__ =="是" and __authSeparate__=="是":
            tablename=Auth().getTokenInfo(request).get('tablename')
            if tablename!="users" and Auth().getTokenInfo(request).get('params') is not None:
                req_dict['userid']=Auth().getTokenInfo(request).get('params').get("id")

        tablename = Auth().getTokenInfo(request).get('tablename')
        if tablename == "users" and req_dict.get("userid") != None:#判断是否存在userid列名
            del req_dict["userid"]
        else:
            __isAdmin__ = None

            allModels = apps.get_app_config('main').get_models()
            for m in allModels:
                if m.__tablename__==tablename:

                    try:
                        __isAdmin__ = m.__isAdmin__
                    except:
                        __isAdmin__ = None
                    break

            if __isAdmin__ == "是":
                if req_dict.get("userid"):
        # del req_dict["userid"]
                    pass
            else:
    #非管理员权限的表,判断当前表字段名是否有userid
                if "userid" in columns:
                    try:
                        pass
                    except:
                        pass
        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为”是”，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=blogcomment.__authTables__
        except:
            __authTables__=None

        if __authTables__!=None and  __authTables__!={} and __foreEndListAuth__=="是":
            for authColumn,authTable in __authTables__.items():
                if authTable==tablename:
                    try:
                        del req_dict['userid']
                    except:
                        pass
                    params = Auth().getTokenInfo(request).get('params')
                    req_dict[authColumn]=params.get(authColumn)
                    username=params.get(authColumn)
                    break
        
        if blogcomment.__tablename__[:7]=="discuss":
            try:
                del req_dict['userid']
            except:
                pass

        q = Q()
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = blogcomment.page(blogcomment, blogcomment, req_dict, request, q)
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_save(request):
    '''
    后台新增
    '''
    request.funname = __name__+"."+blogcomment_save.__name__
    request.operation = "新增博文评论"
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if 'clicktime' in req_dict.keys():
            del req_dict['clicktime']
        tablename=Auth().getTokenInfo(request).get('tablename')
        __isAdmin__ = None
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__==tablename:

                try:
                    __isAdmin__ = m.__isAdmin__
                except:
                    __isAdmin__ = None
                break

        #获取全部列名
        columns=  blogcomment.getallcolumn( blogcomment, blogcomment)
        if tablename!='users' and req_dict.get("userid")==None and 'userid' in columns  and __isAdmin__!='是':
            params=Auth().getTokenInfo(request).get('params')
            req_dict['userid']=params.get('id')


        if 'addtime' in req_dict.keys():
            del req_dict['addtime']

        idOrErr= blogcomment.createbyreq(blogcomment,blogcomment, req_dict)
        if idOrErr is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = idOrErr
        else:
            msg['data'] = idOrErr

        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_add(request):
    '''
    前台新增
    '''
    request.funname = __name__+"."+blogcomment_add.__name__
    request.operation = "新增博文评论"
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        tablename=Auth().getTokenInfo(request).get('tablename')

        #获取全部列名
        columns=  blogcomment.getallcolumn( blogcomment, blogcomment)
        try:
            __authSeparate__=blogcomment.__authSeparate__
        except:
            __authSeparate__=None

        if __authSeparate__=="是" and 'userid' not in req_dict.keys():
            tablename=Auth().getTokenInfo(request).get('tablename')
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=Auth().getTokenInfo(request).get('params').get("id")
                except:
                    pass

        try:
            __foreEndListAuth__=blogcomment.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        if __foreEndListAuth__ and __foreEndListAuth__!="否" and 'userid' not in req_dict.keys():
            tablename=Auth().getTokenInfo(request).get('tablename')
            if tablename!="users":
                req_dict['userid']=Auth().getTokenInfo(request).get('params').get("id")


        if 'addtime' in req_dict.keys():
            del req_dict['addtime']
        error= blogcomment.createbyreq(blogcomment,blogcomment, req_dict)
        if error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
        else:
            msg['data'] = error
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_thumbsup(request,id_):
    '''
     点赞：表属性thumbsUp[是/否]，刷表新增thumbsupnum赞和crazilynum踩字段，
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        rets=blogcomment.getbyid(blogcomment,blogcomment,id_)

        update_dict={
        "id":id_,
        }
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        error = blogcomment.updatebyparams(blogcomment,blogcomment, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg, encoder=CustomJsonEncoder)


def blogcomment_info(request,id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = blogcomment.getbyid(blogcomment,blogcomment, int(id_))
        if len(data)>0:
            msg['data']=data[0]
            if msg['data'].__contains__("reversetime"):
                if isinstance(msg['data']['reversetime'], datetime.datetime):
                    msg['data']['reversetime'] = msg['data']['reversetime'].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    if msg['data']['reversetime'] != None:
                        reversetime = datetime.datetime.strptime(msg['data']['reversetime'], '%Y-%m-%d %H:%M:%S')
                        msg['data']['reversetime'] = reversetime.strftime("%Y-%m-%d %H:%M:%S")

        #浏览点击次数
        try:
            __browseClick__= blogcomment.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"  and  "clicknum"  in blogcomment.getallcolumn(blogcomment,blogcomment):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum,"clicktime":datetime.datetime.now()}
            ret=blogcomment.updatebyparams(blogcomment,blogcomment,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_detail(request,id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data =blogcomment.getbyid(blogcomment,blogcomment, int(id_))
        if len(data)>0:
            msg['data']=data[0]
            if msg['data'].__contains__("reversetime"):
                if isinstance(msg['data']['reversetime'], datetime.datetime):
                    msg['data']['reversetime'] = msg['data']['reversetime'].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    if msg['data']['reversetime'] != None:
                        reversetime = datetime.datetime.strptime(msg['data']['reversetime'], '%Y-%m-%d %H:%M:%S')
                        msg['data']['reversetime'] = reversetime.strftime("%Y-%m-%d %H:%M:%S")

        #浏览点击次数
        try:
            __browseClick__= blogcomment.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"   and  "clicknum"  in blogcomment.getallcolumn(blogcomment,blogcomment):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum,"clicktime":datetime.datetime.now()}

            ret=blogcomment.updatebyparams(blogcomment,blogcomment,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_update(request):
    '''
    '''
    request.funname = __name__+"."+blogcomment_update.__name__
    request.operation = "更新博文评论"
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if 'clicktime' in req_dict.keys() and req_dict['clicktime']=="None":
            del req_dict['clicktime']
        if req_dict.get("mima") and "mima" not in blogcomment.getallcolumn(blogcomment,blogcomment) :
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in blogcomment.getallcolumn(blogcomment,blogcomment) :
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass


        error = blogcomment.updatebyparams(blogcomment, blogcomment, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return JsonResponse(msg)


def blogcomment_delete(request):
    '''
    批量删除
    '''
    request.funname = __name__+"."+blogcomment_delete.__name__
    request.operation = "删除博文评论"
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        error=blogcomment.deletes(blogcomment,
            blogcomment,
             req_dict.get("ids")
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def blogcomment_vote(request,id_):
    '''
    浏览点击次数（表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1）
统计商品或新闻的点击次数；提供新闻的投票功能
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}


        data= blogcomment.getbyid(blogcomment, blogcomment, int(id_))
        for i in data:
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=blogcomment.updatebyparams(blogcomment,blogcomment,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return JsonResponse(msg)

def blogcomment_importExcel(request):
    request.funname = __name__+"."+blogcomment_importExcel.__name__
    request.operation = "导入博文评论"
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}

        excel_file = request.FILES.get("file", "")
        if excel_file.size > 100 * 1024 * 1024:  # 限制为 100MB
            msg['code'] = 400
            msg["msg"] = '文件大小不能超过100MB'
            return JsonResponse(msg)

        file_type = excel_file.name.split('.')[1]
        
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
            table = data.sheets()[0]
            rows = table.nrows
            
            try:
                for row in range(1, rows):
                    row_values = table.row_values(row)
                    req_dict = {}
                    blogcomment.createbyreq(blogcomment, blogcomment, req_dict)
                    
            except:
                pass
                
        else:
            msg = {
                "msg": "文件类型错误",
                "code": 500
            }
                
        return JsonResponse(msg)

def blogcomment_autoSort2(request):
    return JsonResponse({"code": 0, "msg": '',  "data":{}})



def blogcomment_count(request):
    '''
    总数接口
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        req_dict = request.session.get("req_dict")
        where = ' where 1 = 1 '
        for key in req_dict:
            if req_dict[key] != None:
                where = where + " and key like '{0}'".format(req_dict[key])
        
        sql = "SELECT count(*) AS count FROM blogcomment {0}".format(where)
        count = 0
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
        for online_dict in data_dict:
            count = online_dict['count']
        msg['data'] = count

        return JsonResponse(msg, encoder=CustomJsonEncoder)

#对日期进行排序
def order_time(data,type,xColumnName,rev):
    if type=="日":
        result_data = sorted(
            data,
            key=lambda x: (
                int(x[xColumnName].split("-")[0]),
                int(x[xColumnName].split("-")[1]),
                int(x[xColumnName].split("-")[2]),
            ),
            reverse=rev  # 设置排列
        )
    elif type=="月":
        result_data = sorted(
            data,
            key=lambda x: (
                int(x[xColumnName].split("-")[0]),
                int(x[xColumnName].split("-")[1])
            ),
            reverse=rev  # 设置排列
        )
    elif type=="年":
        result_data = sorted(
            data,
            key=lambda x: (
                int(x[xColumnName].split("-")[0]),  # 提取年份并转为整数
            ),
            reverse=rev  # 设置排列
        )
    else:
        result_data = sorted(data, key=lambda x: x[xColumnName], reverse=rev)
    return result_data

# （按值统计）时间统计类型
def blogcomment_value(request, xColumnName, yColumnName, timeStatType):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        #获取hadoop分析后的数据文件
        date_type = ""
        if timeStatType == '日':
            date_type = "date"
        if timeStatType == '月':
            date_type = "month"
        if timeStatType == '季':
            date_type = "quarter"
        if timeStatType == '年':
            date_type = "year"
        json_filename = f'blogcomment_value{xColumnName}{yColumnName}{date_type}.json'

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            where = ' where 1 = 1 '
            raw_query_string = request.META.get('QUERY_STRING', '')
            raw_query_string = unquote(raw_query_string)
            conditionColumn = ""
            conditionValue = ""
            if "conditionColumn=" in raw_query_string:
                conditionColumn = raw_query_string.split("conditionColumn=")[1].split("&")[0]
            if "conditionValue=" in raw_query_string:
                conditionValue = raw_query_string.split("conditionValue=")[1].split("&")[0]
            if conditionColumn != "":
                for index, value in enumerate(conditionColumn.split(";")):
                    if ',' in value:
                        where = where + f''' and {value.split(',')[0]} >= \'{conditionValue.split(";")[index].split(",")[0]}\''''
                        where = where + f''' and {value.split(',')[1]} <= \'{conditionValue.split(";")[index].split(",")[1]}\''''
                    else:
                        where = where + f''' and {value} = \'{conditionValue.split(";")[index]}\''''
            req_dict = request.session.get("req_dict")
            statistics_func = "SUM"
            func_params = req_dict.get("func")
            if func_params == "平均":
                statistics_func = "AVG"
            elif func_params == "最大":
                statistics_func = "MAX"
            elif func_params == "最小":
                statistics_func = "MIN"
            elif func_params == "总和":
                statistics_func = "COUNT"
            try:
                del req_dict["func"]
            except:
                pass
            #定义查询统计语句
            for key, value in req_dict.items():
                if key!="limit" and key!="order" and key!="orderType" and key!="conditionColumn"and key!="conditionValue":
                    where = where + " and {0} ='{1}' ".format(key,value)
            sql = ''
            if timeStatType == '日':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, ROUND({1}({2}),2) total FROM blogcomment {3} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d')".format(xColumnName, statistics_func,yColumnName, where, '%Y-%m-%d')

            if timeStatType == '月':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, ROUND({1}({2}),2) total FROM blogcomment {3} GROUP BY DATE_FORMAT({0}, '%Y-%m')".format(xColumnName, statistics_func,yColumnName, where, '%Y-%m')

            if timeStatType == '季':
                sql = "SELECT CONCAT(YEAR(MIN({0})), '-Q', QUARTER(MIN({0}))) AS {0}, {1}({2}) AS total FROM orders {3} GROUP BY YEAR({0}), QUARTER({0})".format(xColumnName,statistics_func, yColumnName, where)

            if timeStatType == '年':
                sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, ROUND({1}({2}),2) total FROM blogcomment {3} GROUP BY DATE_FORMAT({0}, '%Y')".format(xColumnName,statistics_func, yColumnName, where, '%Y')
            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime(
                            "%Y-%m-%d %H:%M:%S")
                    else:
                        pass
                L.append(online_dict)
            msg['data'] = L
        req_dict = request.session.get("req_dict")
        #对结果进行排序
        order = req_dict.get('order')
        orderType = req_dict.get('orderType')
        if orderType=='x' :
            if order == "desc":
                msg['data'] = order_time(msg['data'], timeStatType, xColumnName, True)
            else:
                msg['data'] = order_time(msg['data'], timeStatType, xColumnName, False)
        else:
            if order == "desc":
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None), key=lambda x: x['total'],
                                     reverse=True)
            else:
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None), key=lambda x: x['total'])

        if "limit" in req_dict and int(req_dict["limit"]) < len(L):
            msg['data'] = msg['data'][:int(req_dict["limit"])]
        return JsonResponse(msg, encoder=CustomJsonEncoder)

# 按值统计
def blogcomment_o_value(request, xColumnName, yColumnName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        #获取hadoop分析后的数据文件
        json_filename = f'blogcomment_value{xColumnName}{yColumnName}.json'

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            where = ' where 1 = 1 '
            raw_query_string = request.META.get('QUERY_STRING', '')
            raw_query_string = unquote(raw_query_string)
            conditionColumn = ""
            conditionValue = ""
            if "conditionColumn=" in raw_query_string:
                conditionColumn = raw_query_string.split("conditionColumn=")[1].split("&")[0]
            if "conditionValue=" in raw_query_string:
                conditionValue = raw_query_string.split("conditionValue=")[1].split("&")[0]
            if conditionColumn != "":
                for index, value in enumerate(conditionColumn.split(";")):
                    if "," in value:
                        where = where + f''' and {value.split(',')[0]} >= \'{conditionValue.split(";")[index].split(",")[0]}\''''
                        where = where + f''' and {value.split(',')[1]} <= \'{conditionValue.split(";")[index].split(",")[1]}\''''
                    else:
                        where = where + f''' and {value} = \'{conditionValue.split(";")[index]}\''''
            req_dict = request.session.get("req_dict")
            statistics_func = "SUM"
            func_params = req_dict.get("func")
            if func_params == "平均":
                statistics_func = "AVG"
            elif func_params == "最大":
                statistics_func = "MAX"
            elif func_params == "最小":
                statistics_func = "MIN"
            elif func_params == "总和":
                statistics_func = "COUNT"
            try:
                del req_dict["func"]
            except:
                pass
            sql = "SELECT {0}, ROUND({1}({2}),2) AS total FROM blogcomment {3} GROUP BY {0}".format(xColumnName,statistics_func, yColumnName, where)
            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime(
                            "%Y-%m-%d %H:%M:%S")
                    else:
                        pass
                L.append(online_dict)
            msg['data'] = L
        req_dict = request.session.get("req_dict")
        if "order" in req_dict:
            order = req_dict["order"]
            if order == "desc":
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'],reverse=True)
            else:
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'])

        if "limit" in req_dict and int(req_dict["limit"]) < len(L):
            msg['data'] = msg['data'][:int(req_dict["limit"])]
        return JsonResponse(msg, encoder=CustomJsonEncoder)

# （按值统计）时间统计类型(多)
def blogcomment_valueMul(request, xColumnName, timeStatType):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": []}
        req_dict = request.session.get("req_dict")
        #获取hadoop分析后的数据文件
        date_type = ""
        if timeStatType == '日':
            date_type = "date"
        if timeStatType == '月':
            date_type = "month"
        if timeStatType == '季':
            date_type = "quarter"
        if timeStatType == '年':
            date_type = "year"
        #获取hadoop分析后的数据文件
        json_filename = f'''blogcomment_value{xColumnName}｛req_dict['yColumnNameMul'].replace(",","")｝{date_type}.json'''

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            where = ' where 1 = 1 '
            raw_query_string = request.META.get('QUERY_STRING', '')
            raw_query_string = unquote(raw_query_string)
            conditionColumn = ""
            conditionValue = ""
            if "conditionColumn=" in raw_query_string:
                conditionColumn = raw_query_string.split("conditionColumn=")[1].split("&")[0]
            if "conditionValue=" in raw_query_string:
                conditionValue = raw_query_string.split("conditionValue=")[1].split("&")[0]
            if conditionColumn != "":
                for index, value in enumerate(conditionColumn.split(";")):
                    if "," in value:
                        where = where + f''' and {value.split(',')[0]} >= \'{conditionValue.split(";")[index].split(",")[0]}\''''
                        where = where + f''' and {value.split(',')[1]} <= \'{conditionValue.split(";")[index].split(",")[1]}\''''
                    else:
                        where = where + f''' and {value} = \'{conditionValue.split(";")[index]}\''''

            statistics_func = "SUM"
            func_params = req_dict.get("func")
            if func_params == "平均":
                statistics_func = "AVG"
            elif func_params == "最大":
                statistics_func = "MAX"
            elif func_params == "最小":
                statistics_func = "MIN"
            elif func_params == "总和":
                statistics_func = "COUNT"
            try:
                del req_dict["func"]
            except:
                pass
              # 定义查询统计语句
            for key, value in req_dict.items():
                if key != "limit" and key != "order" and key != "orderType" and key != "yColumnNameMul" and key != "conditionColumn" and key != "conditionValue":
                    where = where + " and {0} ='{1}' ".format(key, value)

            for item in req_dict['yColumnNameMul'].split(','):
                sql = ''
                if timeStatType == '日':
                    sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, ROUND({1}({2}),2) total FROM blogcomment {3} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d')".format(xColumnName, statistics_func,item, where, '%Y-%m-%d')

                if timeStatType == '月':
                    sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, ROUND({1}({2}),2) total FROM blogcomment {3} GROUP BY DATE_FORMAT({0}, '%Y-%m')".format(xColumnName,statistics_func, item, where, '%Y-%m')

                if timeStatType == '季':
                    sql = "SELECT CONCAT(YEAR(MIN({0})), '-Q', QUARTER(MIN({0}))) {0}, {1}({2}) total FROM blogcomment {3} GROUP BY YEAR({0}), QUARTER({0})".format(xColumnName, statistics_func,item, where)

                if timeStatType == '年':
                    sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, ROUND({1}({2}),2) total FROM blogcomment {3} GROUP BY DATE_FORMAT({0}, '%Y')".format(xColumnName, statistics_func,item, where, '%Y')

                L = []
                cursor = connection.cursor()
                cursor.execute(sql)
                desc = cursor.description
                data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
                for online_dict in data_dict:
                    for key in online_dict:
                        if 'datetime.datetime' in str(type(online_dict[key])):
                            online_dict[key] = online_dict[key].strftime(
                                "%Y-%m-%d %H:%M:%S")
                        else:
                            pass
                    L.append(online_dict)
                    # 结果进行排序
                    order = req_dict.get('order')
                    orderType = req_dict.get('orderType')
                    if orderType == 'x':
                        if order == "desc":
                            L = order_time(L, timeStatType, xColumnName, True)
                        else:
                            L = order_time(L, timeStatType, xColumnName, False)
                    else:
                        if order == "desc":
                            L = sorted((x for x in L if x['total'] is not None),
                                       key=lambda x: x['total'],
                                       reverse=True)
                        else:
                            L = sorted((x for x in L if x['total'] is not None),
                                       key=lambda x: x['total'])
                    # 截取列表个数
                    if "limit" in req_dict and int(req_dict["limit"]) < len(msg['data']):
                        L = L[:int(req_dict["limit"])]
                msg['data'].append(L)
        return JsonResponse(msg, encoder=CustomJsonEncoder)

# （按值统计(多)）
def blogcomment_o_valueMul(request, xColumnName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": []}

        req_dict = request.session.get("req_dict")
        #获取hadoop分析后的数据文件
        json_filename = f'''blogcomment_value{xColumnName}｛req_dict['yColumnNameMul'].replace(",","")｝.json'''

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            where = ' where 1 = 1 '
            raw_query_string = request.META.get('QUERY_STRING', '')
            raw_query_string = unquote(raw_query_string)
            conditionColumn = ""
            conditionValue = ""
            if "conditionColumn=" in raw_query_string:
                conditionColumn = raw_query_string.split("conditionColumn=")[1].split("&")[0]
            if "conditionValue=" in raw_query_string:
                conditionValue = raw_query_string.split("conditionValue=")[1].split("&")[0]
            if conditionColumn != "":
                for index, value in enumerate(conditionColumn.split(";")):
                    if "," in value:
                        where = where + f''' and {value.split(',')[0]} >= \'{conditionValue.split(";")[index].split(",")[0]}\''''
                        where = where + f''' and {value.split(',')[0]} <= \'{conditionValue.split(";")[index].split(",")[1]}\''''
                    else:
                        where = where + f''' and {value} = \'{conditionValue.split(";")[index]}\''''
            statistics_func = "SUM"
            func_params = req_dict.get("func")
            if func_params == "平均":
                statistics_func = "AVG"
            elif func_params == "最大":
                statistics_func = "MAX"
            elif func_params == "最小":
                statistics_func = "MIN"
            elif func_params == "总和":
                statistics_func = "COUNT"
            try:
                del req_dict["func"]
            except:
                pass
            for item in req_dict['yColumnNameMul'].split(','):
                sql = "SELECT {0}, ROUND({1}({2}),2) AS total FROM blogcomment {3} GROUP BY {0}".format(xColumnName, statistics_func,item, where)
                L = []
                cursor = connection.cursor()
                cursor.execute(sql)
                desc = cursor.description
                data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
                for online_dict in data_dict:
                    for key in online_dict:
                        if 'datetime.datetime' in str(type(online_dict[key])):
                            online_dict[key] = online_dict[key].strftime(
                                "%Y-%m-%d %H:%M:%S")
                        else:
                            pass
                    L.append(online_dict)
                msg['data'].append(L)
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def blogcomment_group(request, columnName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}

        #获取hadoop分析后的数据文件
        json_filename = f'blogcomment_group{columnName}.json'

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            where = ' where 1 = 1 '
            raw_query_string = request.META.get('QUERY_STRING', '')
            raw_query_string = unquote(raw_query_string)
            conditionColumn = ""
            conditionValue = ""
            if "conditionColumn=" in raw_query_string:
                conditionColumn = raw_query_string.split("conditionColumn=")[1].split("&")[0]
            if "conditionValue=" in raw_query_string:
                conditionValue = raw_query_string.split("conditionValue=")[1].split("&")[0]
            if conditionColumn != "":
                for index, value in enumerate(conditionColumn.split(";")):
                    if ',' in value:
                        where = where + f''' and {value.split(',')[0]} >= \'{conditionValue.split(";")[index].split(",")[0]}\''''
                        where = where + f''' and {value.split(',')[1]} <= \'{conditionValue.split(";")[index].split(",")[1]}\''''
                    else:
                        where = where + f''' and {value} = \'{conditionValue.split(";")[index]}\''''

            sql = "SELECT COUNT(*) AS total, " + columnName + " FROM blogcomment " + where + " GROUP BY " + columnName
            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime("%Y-%m-%d")
                    else:
                        pass
                L.append(online_dict)
            msg['data'] = L
        req_dict = request.session.get("req_dict")
        if "order" in req_dict:
            order = req_dict["order"]
            if order == "desc":
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'],reverse=True)
            else:
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'])

        if "limit" in req_dict and int(req_dict["limit"]) < len(L):
            msg['data'] = msg['data'][:int(req_dict["limit"])]
        return JsonResponse(msg, encoder=CustomJsonEncoder)






def blogcomment_cleanse(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        try:
            list, _, _, total,_ = blogcomment.page(blogcomment, blogcomment, {})
            df = pd.DataFrame(list,dtype=object)
#随机填充
            df['pluser'].replace([None, '' ], pd.NA,inplace = True)
            pluser_non_na = df['pluser'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'pluser']):
                    df.loc[i, 'pluser'] = pluser_non_na.sample(n=1,replace=True).values[0]
#随机填充
            df['fbplace'].replace([None, '' ], pd.NA,inplace = True)
            fbplace_non_na = df['fbplace'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'fbplace']):
                    df.loc[i, 'fbplace'] = fbplace_non_na.sample(n=1,replace=True).values[0]
            data_list = df.to_dict(orient='records')
            blogcomment.deletes(blogcomment,blogcomment,ids=[i["id"] for i in list])
            batchList = []
            for dl in data_list:
                filtered_data = {k: v for k, v in dl.items() if v not in [None, '', float('nan')] and (not isinstance(v, float) or not math.isnan(v))}
                batchList.append(blogcomment(**filtered_data))
            blogcomment.objects.bulk_create(batchList)
        except Exception as e:
            msg["code"] = other_code
            msg["msg"] = e.__str__()

        return JsonResponse(msg)




