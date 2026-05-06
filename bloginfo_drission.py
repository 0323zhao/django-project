# bloginfo_drission.py
# 使用 DrissionPage 抓取博主主页博文，存入 bloginfo 表

import sys, os, time, json, re
from datetime import datetime

# Django 环境初始化
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2.settings')
import django

django.setup()

from main.models import bloginfo
from DrissionPage import ChromiumPage


# ============ 工具函数 ============
def extract_uid_from_url(userurl):
    if not userurl:
        return None
    match = re.search(r'(?:weibo\.com/|/u/)(\d+)', userurl)
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


# ============ 主抓取逻辑 ============
def fetch_bloginfo_for_uid(page, uid):
    """抓取指定 UID 的博主主页博文，返回博文列表（字典）"""
    blog_list = []
    # 博主主页 API 接口（DrissionPage 可以直接监听响应）
    for page_num in range(1, 11):  # 抓前10页
        url = f'https://m.weibo.cn/api/container/getIndex?containerid=107603{uid}&page={page_num}'
        page.get(url)
        time.sleep(2)  # 等待加载，模拟用户停留

        # 获取页面返回的 JSON 文本
        resp_text = page.html
        try:
            data = json.loads(resp_text)
        except:
            continue

        # 如果触发验证码，提示用户手动处理
        if data.get('ok') == -100:
            print(f'UID {uid} 触发验证码，请在浏览器中手动滑动验证，完成后按 Enter 继续...')
            input()
            page.get(url)  # 重新请求
            time.sleep(2)
            try:
                data = json.loads(page.html)
            except:
                continue

        cards = data.get('data', {}).get('cards', [])
        if not cards:
            break

        for card in cards:
            mblog = card.get('mblog')
            if not mblog:
                continue

            blog = {}
            try:
                blog['screenname'] = mblog['user']['screen_name']
            except:
                pass
            try:
                blog['mblogtext'] = mblog['text']
            except:
                pass
            try:
                blog['commentscount'] = int(mblog.get('comments_count', 0))
            except:
                pass
            try:
                blog['attitudescount'] = int(mblog.get('attitudes_count', 0))
            except:
                pass
            try:
                blog['repostscount'] = int(mblog.get('reposts_count', 0))
            except:
                pass
            try:
                blog['fbtime'] = mblog.get('created_at', '')
            except:
                pass
            try:
                blog['medias'] = mblog.get('source', '')
            except:
                pass
            try:
                blog['userurl'] = f'https://weibo.com/{mblog["user"]["id"]}'
            except:
                pass
            try:
                blog['weibo_id'] = int(mblog['id'])
            except:
                pass

            blog_list.append(blog)

        # 如果该页博文数少于 10，说明没有下一页了
        if len(cards) < 10:
            break

    return blog_list


def main():
    print("即将打开 Chrome 浏览器，请手动登录 m.weibo.cn")
    page = ChromiumPage()
    page.get('https://m.weibo.cn/')
    input("登录完成后按 Enter 继续...")

    # 获取所有已有博主的 UID（去重，且该博主尚未抓取过博文）
    import pandas as pd
    all_info = bloginfo.objects.exclude(userurl__isnull=True).exclude(userurl='').values('screenname',
                                                                                         'userurl').distinct()

    uid_set = set()
    for info in all_info:
        uid = extract_uid_from_url(info['userurl'])
        if uid:
            uid_set.add(uid)

    print(f'共 {len(uid_set)} 位博主待抓取')
    total_saved = 0

    for idx, uid in enumerate(uid_set, 1):
        print(f'正在抓取第 {idx}/{len(uid_set)} 位博主 (UID: {uid})...')
        blogs = fetch_bloginfo_for_uid(page, uid)

        # 写入数据库（避免重复）
        for blog in blogs:
            # 简单去重：检查 weibo_id 是否存在
            if not bloginfo.objects.filter(weibo_id=blog.get('weibo_id')).exists():
                bloginfo.objects.create(**blog)
                total_saved += 1

        print(f'  本博主保存 {len(blogs)} 条，累计 {total_saved} 条')
        time.sleep(3)  # 控制频率

    page.quit()
    print(f'所有博主抓取完成，共新增博文 {total_saved} 条。')


if __name__ == '__main__':
    main()