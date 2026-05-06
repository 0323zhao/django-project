# batch_sentiment_analysis.py
# 放在 django-project/main 目录下，与 manage.py 同级（或直接在项目根目录运行）

import os
import sys
import time
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2.settings')
django.setup()

from main.models import bloginfo
from util.baidubce_api import BaiDuBce


def batch_sentiment_analysis():
    # 初始化百度 API 客户端（自动从数据库 config 表读取密钥）
    bdb = BaiDuBce()

    # 查询所有 mblogtext 不为空且 sentiment 为空的记录
    rows = bloginfo.objects.filter(
        mblogtext__isnull=False,
    ).exclude(
        mblogtext=''
    ).filter(
        sentiment__isnull=True
    )

    total = rows.count()
    print(f"找到 {total} 条待分析记录。")
    if total == 0:
        print("没有需要分析的数据。")
        return

    success_count = 0
    fail_count = 0

    for idx, row in enumerate(rows, start=1):
        text = row.mblogtext.strip()
        if not text:
            continue

        try:
            result = bdb.sentiment_classify(text)
            sentiment = result.get('sentiment')          # 正向/负向/中性
            confidence = result.get('confidence')        # 置信度（0~1 的浮点数）

            if sentiment is None:
                fail_count += 1
                continue

            # 写入结果
            row.sentiment = sentiment
            row.sentiment_score = confidence if confidence is not None else 0.0
            row.save(update_fields=['sentiment', 'sentiment_score'])

            success_count += 1
            print(f"[{idx}/{total}] 完成 → {sentiment} (置信度 {confidence})")

        except Exception as e:
            fail_count += 1
            print(f"[{idx}/{total}] 失败: {e}")

        # 控制请求频率，避免触发百度 API 限制（默认 QPS 限制为 5，此处设为 0.5s 可安全运行）
        time.sleep(0.5)

    print("\n" + "=" * 50)
    print(f"批量分析完毕。成功: {success_count} 条，失败: {fail_count} 条")


if __name__ == '__main__':
    batch_sentiment_analysis()