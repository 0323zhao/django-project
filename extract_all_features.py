# extract_all_features.py
# 一次性提取时间特征 + 内容形式特征，写入 bloginfo 表
import os, sys, re, django
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2.settings')
django.setup()

from main.models import bloginfo

# =================== 时间解析相关 ===================
TIME_FORMATS = [
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y-%m-%d %H:%M',
    '%Y-%m-%d',
    '%Y年%m月%d日 %H:%M:%S',
    '%Y年%m月%d日 %H:%M',
    '%Y年%m月%d日',
]

DEFAULT_YEAR = 2025


def parse_time(time_str):
    if not time_str or not isinstance(time_str, str):
        return None
    time_str = time_str.strip()

    # 新增：处理 "Mon Aug 21 07:17:42 +0800 2023" 这种格式
    # 去掉时区符号（+0800之类），仅保留日期时间
    tz_match = re.search(r'([A-Za-z]{3}\s+[A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+\+\d{4}\s+(\d{4})', time_str)
    if tz_match:
        datetime_part = tz_match.group(1) + ' ' + tz_match.group(2)
        try:
            return datetime.strptime(datetime_part, '%a %b %d %H:%M:%S %Y')
        except:
            pass

    # 1. 标准格式
    for fmt in TIME_FORMATS:
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue

    # 2. 无年份的“月日+时间”格式
    match = re.search(r'(\d{1,2})月(\d{1,2})日\s+(\d{1,2}):(\d{2})', time_str)
    if match:
        month, day, hour, minute = map(int, match.groups())
        return datetime(DEFAULT_YEAR, month, day, hour, minute)

    # 3. 相对时间处理
    now = datetime.now()
    relative_match = re.search(r'(今天|昨天|前天)\s*(\d{1,2}):(\d{2})', time_str)
    if relative_match:
        relative_day, hour, minute = relative_match.groups()
        hour, minute = int(hour), int(minute)
        if relative_day == '今天':
            target_date = now
        elif relative_day == '昨天':
            target_date = now - timedelta(days=1)
        elif relative_day == '前天':
            target_date = now - timedelta(days=2)
        else:
            target_date = now
        return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

    return None


# =================== 特征提取函数 ===================

def extract_time_features():
    """提取时间特征：publish_hour 和 publish_weekday"""
    print('=' * 60)
    print('开始提取时间特征...')

    rows = bloginfo.objects.filter(
        fbtime__isnull=False
    ).exclude(
        fbtime=''
    ).filter(
        publish_hour__isnull=True
    )

    total = rows.count()
    print(f'找到 {total} 条待处理记录。')
    if total == 0:
        print('没有需要更新的数据。')
        return

    success = 0
    fail = 0

    for idx, row in enumerate(rows, start=1):
        dt = parse_time(row.fbtime)
        if dt is None:
            print(f'[{idx}/{total}] 无法解析: {row.fbtime}')
            fail += 1
            continue

        row.publish_hour = dt.hour
        row.publish_weekday = dt.weekday()
        row.save(update_fields=['publish_hour', 'publish_weekday'])

        success += 1
        if idx % 20 == 0 or idx == total:
            print(f'[{idx}/{total}] 完成。当前成功: {success}, 失败: {fail}')

    print(f'时间特征处理完毕。成功: {success} 条，失败: {fail} 条\n')


def extract_content_features():
    """提取内容形式特征：has_image, has_video, has_link, has_topic, has_mention"""
    print('=' * 60)
    print('开始提取内容形式特征...')

    rows = bloginfo.objects.filter(mblogtext__isnull=False).exclude(mblogtext='')
    total = rows.count()
    print(f'待处理记录: {total}')
    if total == 0:
        return

    updated = 0
    for idx, row in enumerate(rows, start=1):
        text = row.mblogtext.strip()
        if not text:
            continue

        has_image = bool(re.search(r'\[图片\]|【图片】|查看图片', text))
        has_video = bool(re.search(r'\[视频\]|【视频】|视频直播', text))
        has_link = bool(re.search(r'https?://', text))
        has_topic = bool(re.search(r'#[^#]+#', text))
        has_mention = bool(re.search(r'@[\w\u4e00-\u9fff\-_]+', text))

        update_fields = []
        if row.has_image != has_image:
            row.has_image = has_image
            update_fields.append('has_image')
        if row.has_video != has_video:
            row.has_video = has_video
            update_fields.append('has_video')
        if row.has_link != has_link:
            row.has_link = has_link
            update_fields.append('has_link')
        if row.has_topic != has_topic:
            row.has_topic = has_topic
            update_fields.append('has_topic')
        if row.has_mention != has_mention:
            row.has_mention = has_mention
            update_fields.append('has_mention')

        if update_fields:
            row.save(update_fields=update_fields)
            updated += 1
            print(f'[{idx}/{total}] 更新: {update_fields}')

    print(f'内容形式特征处理完毕。总计更新了 {updated} 条记录\n')


# =================== 主流程 ===================
if __name__ == '__main__':
    extract_time_features()
    extract_content_features()
    print('全部特征提取完成！')