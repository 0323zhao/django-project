# fill_blogger_profiles.py
# 功能：
# 1. 从 bloginfo 聚合每个博主的平均转发/评论/点赞数，写入 blogger_profile
# 2. 从微博 API 抓取每个博主的粉丝数、关注数、微博数等，写入 blogger_profile
# 运行方式：python fill_blogger_profiles.py

import sys, os, time, json
import requests
import re
import pandas as pd

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2.settings')
import django
django.setup()

from main.models import bloginfo, blogger_profile
from main.config_model import config


def parse_cookie_string(cookie_str):
    """安全解析 Cookie 字符串，兼容 ';' 和 '; ' 分隔符"""
    cookies = {}
    if not cookie_str:
        return cookies
    for item in cookie_str.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key.strip()] = value.strip()
    return cookies


def get_headers_and_cookies():
    headers = {}
    cookies = {}
    try:
        obj = config.objects.filter(name='weibo_request_headers').first()
        if obj and obj.value:
            headers = json.loads(obj.value)
    except:
        pass
    try:
        obj = config.objects.filter(name='weibo_full_cookie').first()
        if obj and obj.value:
            cookies = parse_cookie_string(obj.value)
    except:
        pass
    return headers, cookies


# ============ 聚合平均互动数据 ============
def update_avg_stats():
    print('=' * 60)
    print('开始聚合博主平均互动数据...')

    all_blogs = bloginfo.objects.all().values(
        'screenname', 'repostscount', 'commentscount', 'attitudescount'
    )
    df_blogs = pd.DataFrame(list(all_blogs))
    if df_blogs.empty:
        print('bloginfo 表无数据，跳过')
        return

    for col in ['repostscount', 'commentscount', 'attitudescount']:
        df_blogs[col] = pd.to_numeric(df_blogs[col], errors='coerce')

    agg_df = df_blogs.groupby('screenname').agg(
        avg_reposts=('repostscount', 'mean'),
        avg_comments=('commentscount', 'mean'),
        avg_attitudes=('attitudescount', 'mean')
    ).reset_index()

    created, updated = 0, 0
    for _, row in agg_df.iterrows():
        name = row['screenname']
        if pd.isna(name):
            continue
        _, is_new = blogger_profile.objects.update_or_create(
            screenname=name,
            defaults={
                'avg_reposts': 0.0 if pd.isna(row['avg_reposts']) else row['avg_reposts'],
                'avg_comments': 0.0 if pd.isna(row['avg_comments']) else row['avg_comments'],
                'avg_attitudes': 0.0 if pd.isna(row['avg_attitudes']) else row['avg_attitudes'],
            }
        )
        if is_new: created += 1
        else: updated += 1
    print(f'聚合完成。新增: {created} 条，更新: {updated} 条')


# ============ 微博 API 相关函数 ============
def extract_uid_from_url(userurl):
    if not userurl:
        return None
    match = re.search(r'(?:/u/|weibo\.com/)(\d+)', userurl)
    return match.group(1) if match else None


def parse_count(value):
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    if not isinstance(value, str):
        return 0
    value = value.strip()
    if value == '':
        return 0
    try:
        if '万' in value:
            return int(float(value.replace('万', '')) * 10000)
        elif '亿' in value:
            return int(float(value.replace('亿', '')) * 100000000)
        else:
            return int(float(value))
    except:
        return 0


def fetch_profile_by_uid(session, uid, screenname):
    try:
        resp = session.get(
            f'https://m.weibo.cn/api/container/getIndex?containerid=100505{uid}',
            timeout=10
        )
        data = resp.json()
    except Exception as e:
        print(f'  [!] {screenname}: UID {uid} 请求失败 ({e})')
        return None

    user_info = data.get('data', {}).get('userInfo', {})
    if not user_info:
        print(f'  [!] {screenname}: UID {uid} 无用户信息')
        return None
    print('userInfo keys:', list(user_info.keys()))
    return {
        'screenname': screenname,
        'followers_count': parse_count(user_info.get('followers_count', 0)),
        'friends_count': parse_count(user_info.get('follow_count', 0)),
        'statuses_count': parse_count(user_info.get('statuses_count', 0)),
        'verified': 1 if user_info.get('verified') else 0,
        'verified_reason': user_info.get('verified_reason', ''),
    }


def fetch_profile(session, screenname):
    search_url = f'https://m.weibo.cn/api/container/getIndex?containerid=100103type=3&q={screenname}&t=0'
    try:
        resp = session.get(search_url, timeout=10)
        data = resp.json()
    except Exception as e:
        print(f'  [!] {screenname}: 搜索请求失败 ({e})')
        return None

    cards = data.get('data', {}).get('cards', [])
    if not cards:
        return None

    uid = None
    for card in cards:
        card_group = card.get('card_group', [])
        for item in card_group:
            user = item.get('user')
            if user and user.get('screen_name', '').strip() == screenname.strip():
                uid = user.get('id')
                break
        if uid:
            break

    if not uid:
        return None
    return fetch_profile_by_uid(session, uid, screenname)


# ============ 主抓取流程 ============
def update_profiles_from_weibo():
    print('=' * 60)
    print('开始从微博抓取博主粉丝/关注数据...')

    headers, cookies = get_headers_and_cookies()
    if not cookies:
        print('Cookie 为空，请更新 config 表中的 weibo_full_cookie')
        return

    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update(headers)

    # # 验证登录状态（用需要登录的接口检测）
    try:
        # 用桂视网的UID做测试，也可以换成任意一个存在的UID
        test_uid = '1989772455'
        resp = session.get(
            f'https://m.weibo.cn/api/container/getIndex?containerid=100505{test_uid}',
            headers=headers,
            timeout=10
        )
        if resp.status_code == 200 and resp.json().get('data', {}).get('userInfo'):
            print('登录状态正常，开始抓取...')
        else:
            print('警告：Cookie可能已过期，请重新获取完整Cookie并更新config表。')
            return
    except Exception as e:
        print(f'验证登录状态失败: {e}')
        return

    # 获取博主列表
    bloggers = bloginfo.objects.exclude(userurl__isnull=True).exclude(userurl='').values(
        'screenname', 'userurl'
    ).distinct()
    total = bloggers.count()
    print(f'共 {total} 个博主待抓取')

    for idx, blogger in enumerate(bloggers, 1):
        name = blogger['screenname']
        url = blogger['userurl']
        if not name:
            continue

        uid = extract_uid_from_url(url)
        if uid:
            profile = fetch_profile_by_uid(session, uid, name)
            if profile:
                blogger_profile.objects.update_or_create(
                    screenname=name,
                    defaults={
                        'followers_count': profile['followers_count'],
                        'friends_count': profile['friends_count'],
                        'statuses_count': profile['statuses_count'],
                        'verified': profile['verified'],
                        'verified_reason': profile['verified_reason'],
                    }
                )
                print(f'[{idx}/{total}] {name} -> 粉丝:{profile["followers_count"]}, 关注:{profile["friends_count"]}')
            else:
                print(f'[{idx}/{total}] {name} -> UID {uid} 抓取失败')
        else:
            print(f'[{idx}/{total}] {name} 未提取到 UID，尝试昵称搜索...')
            profile = fetch_profile(session, name)
            if profile:
                blogger_profile.objects.update_or_create(
                    screenname=name,
                    defaults={
                        'followers_count': profile['followers_count'],
                        'friends_count': profile['friends_count'],
                        'statuses_count': profile['statuses_count'],
                        'verified': profile['verified'],
                        'verified_reason': profile['verified_reason'],
                    }
                )
                print(f'  昵称搜索成功 -> 粉丝:{profile["followers_count"]}')
            else:
                print(f'  昵称搜索失败，跳过')

        time.sleep(1.5)

    print('微博数据抓取完成')


# ============ 主流程 ============
def main():
    update_avg_stats()
    update_profiles_from_weibo()
    print('=' * 60)
    print('✨ 全部完成！blogger_profile 表已完整填充。')

if __name__ == '__main__':
    main()