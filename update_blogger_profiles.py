# update_blogger_profiles.py
import time, json, sys, os
from DrissionPage import ChromiumPage

# Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2.settings')
import django
django.setup()
from main.models import bloginfo, blogger_profile

def get_all_screennames():
    names = bloginfo.objects.values_list('screenname', flat=True).distinct()
    return [n for n in names if n]

def fetch_profile(page, screenname):
    # 搜索用户
    search_url = f'https://m.weibo.cn/api/container/getIndex?containerid=100103type=3&q={screenname}&t=0'
    page.get(search_url)
    time.sleep(2)
    text = page.html
    try:
        data = json.loads(text)
    except:
        print(f'{screenname}: JSON 解析失败')
        return None

    cards = data.get('data', {}).get('cards', [])
    if not cards:
        print(f'{screenname}: 无搜索结果')
        return None

    # 获取用户 UID
    uid = None
    for card in cards:
        for item in card.get('card_group', []):
            if 'user' in item:
                uid = item['user'].get('id')
                break
        if uid:
            break
    if not uid:
        print(f'{screenname}: 无法获取 UID')
        return None

    # 获取用户详细信息
    info_url = f'https://m.weibo.cn/api/container/getIndex?containerid=100505{uid}'
    page.get(info_url)
    time.sleep(2)
    text = page.html
    try:
        data = json.loads(text)
    except:
        print(f'{screenname}: 主页 JSON 解析失败')
        return None

    user_info = data.get('data', {}).get('userInfo', {})
    if not user_info:
        print(f'{screenname}: 无用户信息')
        return None

    return {
        'screenname': screenname,
        'followers_count': user_info.get('followers_count', 0),
        'friends_count': user_info.get('friends_count', 0),
        'statuses_count': user_info.get('statuses_count', 0),
        'verified': 1 if user_info.get('verified') else 0,
        'verified_reason': user_info.get('verified_reason', ''),
    }

def main():
    page = ChromiumPage()
    page.get('https://m.weibo.cn/')
    input('请在弹出的浏览器中手动登录微博，登录完成后按回车继续...')

    names = get_all_screennames()
    print(f'共 {len(names)} 个博主待抓取')

    for idx, name in enumerate(names, 1):
        print(f'[{idx}/{len(names)}] 正在抓取 {name} ...')
        profile = fetch_profile(page, name)
        if profile:
            blogger_profile.objects.update_or_create(screenname=name, defaults=profile)
            print(f'  -> 粉丝:{profile["followers_count"]}, 关注:{profile["friends_count"]}')
        time.sleep(2)

    page.quit()
    print('全部完成')

if __name__ == '__main__':
    main()