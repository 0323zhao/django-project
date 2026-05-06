# compare_config.py
import os, sys, json

# Django 初始化
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2.settings')
import django
django.setup()

from main.config_model import config

# ========== A 版本硬编码的 Headers ==========
hardcoded_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/0.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'referer': 'https://m.weibo.cn/',
}

# ========== A 版本硬编码的 Cookie 字符串 ==========
hardcoded_cookie_str = (
    "_T_WM=99812392567; "
    "gdxidpyhxdE=cDRXkOgfdSKnDCXom2E6jxeni%5C58Zeq1%2FfB%2B7amTSxbalptLE7GQAOJW63zSh2nX6zBUa%5CBfBcoCadGM%2B8ftTvJVIHxPC8YRI4hYfwALbYo4LvDJJpc2layD52CD5H3RE0EMEfM%5CU7kEm8%5Cg1waysR5J%2BY25T6EgO%2BgaRDXD2njwEfxa%3A1777961552690; "
    "WEIBOCN_FROM=1110006030; "
    "SCF=AmbAoIRBBWgh55_zcL_M6P4-7YnIIj2xx34-A49B9KLHshD6GwhjavZQCn4KVw3dzByfu_9kJmDsjnAmnvZS1GM.; "
    "SUB=_2A25E_e5kDeRhGeFL6loT9CfIyjyIHXVkc2-srDV6PUJbktANLVDkkW1NQnQVgBUmPOV2eOU5mBUBMiG4yjzqaDmx; "
    "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWMMv.4k14AX3.o2NLs1.xD5NHD95QNSK2ReoB4Sh27Ws4Dqcj_i--4i-8FiK.Ri--RiKn7iKn0i--fi-isiKn0i--Ni-2EiKy8i--NiK.Xi-zN; "
    "SSOLoginState=1777966644; "
    "ALF=1780558644; "
    "MLOGIN=1; "
    "XSRF-TOKEN=2a2be6; "
    "mweibo_short_token=5bc11e0405; "
    "M_WEIBOCN_PARAMS=fid%3D1076031989772455%26uicode%3D10000011"
)

# ========== 从数据库读取 ==========
db_headers = {}
try:
    obj = config.objects.filter(name='weibo_request_headers').first()
    if obj and obj.value:
        db_headers = json.loads(obj.value)
except Exception as e:
    print(f"读取 weibo_request_headers 失败: {e}")

db_cookie_str = ''
try:
    obj = config.objects.filter(name='weibo_full_cookie').first()
    if obj and obj.value:
        db_cookie_str = obj.value.strip()
except Exception as e:
    print(f"读取 weibo_full_cookie 失败: {e}")

# ========== 输出对比 ==========
print("=" * 60)
print("【A 版本硬编码 Headers】")
for k, v in hardcoded_headers.items():
    print(f"  {k}: {v}")

print("\n【数据库 weibo_request_headers】")
if db_headers:
    for k, v in db_headers.items():
        print(f"  {k}: {v}")

print("\n【Head 差异】")
# 检查 Key 差异
hard_keys = set(hardcoded_headers.keys())
db_keys = set(db_headers.keys()) if db_headers else set()
missing_in_db = hard_keys - db_keys
extra_in_db = db_keys - hard_keys
common_keys = hard_keys & db_keys

if missing_in_db:
    print(f"  数据库缺少的字段: {missing_in_db}")
if extra_in_db:
    print(f"  数据库额外多出的字段: {extra_in_db}")
for k in common_keys:
    hv = hardcoded_headers[k]
    dv = db_headers[k]
    if hv != dv:
        print(f"  字段 {k} 不同:")
        print(f"    A版本: {hv}")
        print(f"    数据库: {dv}")

print("\n" + "=" * 60)
print("【A 版本硬编码 Cookie 字符串（已解析为字典）】")
hardcoded_cookies = {}
for part in hardcoded_cookie_str.split(';'):
    part = part.strip()
    if '=' in part:
        k, v = part.split('=', 1)
        hardcoded_cookies[k.strip()] = v.strip()
for k, v in hardcoded_cookies.items():
    print(f"  {k}: {v}")

print("\n【数据库 weibo_full_cookie（已解析）】")
db_cookies = {}
if db_cookie_str:
    for part in db_cookie_str.split(';'):
        part = part.strip()
        if '=' in part:
            k, v = part.split('=', 1)
            db_cookies[k.strip()] = v.strip()
    for k, v in db_cookies.items():
        print(f"  {k}: {v}")

print("\n【Cookie 差异】")
hard_cookie_keys = set(hardcoded_cookies.keys())
db_cookie_keys = set(db_cookies.keys())
missing_in_db_c = hard_cookie_keys - db_cookie_keys
extra_in_db_c = db_cookie_keys - hard_cookie_keys
if missing_in_db_c:
    print(f"  数据库缺少的 Cookie 字段: {missing_in_db_c}")
if extra_in_db_c:
    print(f"  数据库额外多出的 Cookie 字段: {extra_in_db_c}")
common_c = hard_cookie_keys & db_cookie_keys
for k in common_c:
    hv = hardcoded_cookies[k]
    dv = db_cookies[k]
    if hv != dv:
        print(f"  Cookie {k} 不同:")
        print(f"    A版本: {hv}")
        print(f"    数据库: {dv}")

print("\n比较完成。")