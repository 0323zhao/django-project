# train_content_strategy.py
import os, sys, django
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib, warnings
warnings.filterwarnings('ignore')

# ---------- 配置 Django 环境 ----------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2.settings')
django.setup()

from main.models import bloginfo, blogger_profile

# ---------- 1. 构建训练特征矩阵 ----------
print("开始构建训练数据集...")
qs = bloginfo.objects.all().values(
    'screenname', 'commentscount', 'attitudescount',
    'sentiment', 'sentiment_score',
    'has_image', 'has_video', 'has_link', 'has_topic', 'has_mention',
    'publish_hour', 'publish_weekday', 'medias',
    'repostscount'
)
data = pd.DataFrame(list(qs))

# 清理数值列
for col in ['commentscount', 'attitudescount', 'repostscount']:
    data[col] = pd.to_numeric(data[col], errors='coerce')
data = data.dropna(subset=['repostscount'])

if len(data) < 10:
    print("数据量不足（至少需要10条），请补充数据。")
    sys.exit(0)
print(f"可用数据行数: {len(data)}")

# ---------- 特征工程 ----------
# 情感编码
le = LabelEncoder()
data['sentiment'] = data['sentiment'].fillna('中性')
data['sentiment_enc'] = le.fit_transform(data['sentiment'])
data['sentiment_score'] = pd.to_numeric(data['sentiment_score'], errors='coerce').fillna(0.5)

# 布尔特征
bool_cols = ['has_image', 'has_video', 'has_link', 'has_topic', 'has_mention']
for col in bool_cols:
    data[col] = data[col].fillna(0).astype(int)

# 时间特征
data['publish_hour'] = pd.to_numeric(data['publish_hour'], errors='coerce').fillna(-1).astype(int)
data['publish_weekday'] = pd.to_numeric(data['publish_weekday'], errors='coerce').fillna(-1).astype(int)

# 媒体编码
data['medias'] = data['medias'].fillna('未知').astype(str)
data['medias_enc'] = LabelEncoder().fit_transform(data['medias'])

# ---------- 2. 合并博主画像表 ----------
profile_df = pd.DataFrame(list(blogger_profile.objects.all().values(
    'screenname', 'avg_reposts', 'avg_comments', 'avg_attitudes',
    'followers_count', 'friends_count'
)))
data = data.merge(profile_df, on='screenname', how='left')

# 填充缺失的博主画像（用中位数或0）
for col in ['avg_reposts', 'avg_comments', 'avg_attitudes', 'followers_count', 'friends_count']:
    if data[col].notna().sum() == 0:
        data[col] = 0
    else:
        data[col] = data[col].fillna(data[col].median())

# ---------- 3. 定义特征列表 ----------
feature_cols = [
    'commentscount', 'attitudescount',
    'sentiment_enc', 'sentiment_score',
    'has_image', 'has_video', 'has_link', 'has_topic', 'has_mention',
    'publish_hour', 'publish_weekday',
    'medias_enc',
    'avg_reposts', 'avg_comments', 'avg_attitudes',
    'followers_count', 'friends_count'
]

# 预留：评论综合情绪特征（后续可在此处添加）
# 例如：comment_positive_ratio, comment_negative_ratio, comment_avg_sentiment

X = data[feature_cols].values
y = data['repostscount'].values

# 安全处理
X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)

# ---------- 4. 训练模型 ----------
print("\n开始训练随机森林模型...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"模型训练完成。测试集 MAE: {mae:.2f}, R²: {r2:.3f}")

# 保存模型
model_file = os.path.join(os.path.dirname(__file__), 'content_strategy_model.pkl')
joblib.dump(model, model_file)
print(f"模型已保存至: {model_file}")

# ---------- 5. 特征重要性 ----------
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

print("\n" + "=" * 60)
print("特征重要性排名 (Top 10):")
for i in range(min(10, len(feature_cols))):
    idx = indices[i]
    print(f"  {i+1}. {feature_cols[idx]:20s} -> {importances[idx]:.4f}")

# ---------- 6. 策略建议 ----------
print("\n" + "=" * 60)
print("【内容策略建议（基于特征重要性）】")
print("以下特征对转发量的影响最大：\n")

for i in range(min(5, len(feature_cols))):
    idx = indices[i]
    feat = feature_cols[idx]
    if feat == 'followers_count':
        print("🔹 粉丝数：粉丝基数越大，转发量越高。可重点关注高粉丝量博主。")
    elif feat == 'friends_count':
        print("🔹 关注数：博主的社交活跃度影响传播。")
    elif feat == 'avg_reposts':
        print("🔹 历史平均转发量：博主长期影响力指标。")
    elif feat == 'avg_comments':
        print("🔹 历史平均评论数：粉丝互动深度。")
    elif feat == 'commentscount':
        print("🔹 当前博文评论数：评论越多，转发越高。")
    elif feat == 'attitudescount':
        print("🔹 当前博文点赞数：点赞是转发的先行指标。")
    elif feat == 'sentiment_enc':
        print("🔹 情感倾向：正向情感博文传播力更强。")
    elif feat == 'sentiment_score':
        print("🔹 情感强度：情绪表达越强烈，转发越高。")
    elif feat == 'has_image':
        print("🔹 配图：含图片的博文转发率更高。")
    elif feat == 'publish_hour':
        print("🔹 发布小时：晚间高峰时段发文更易传播。")
    else:
        print(f"🔸 {feat}: 重要性 {importances[idx]:.4f}，需结合业务分析。")

print("\n💡 综合建议：")
top_feat = feature_cols[indices[0]]
if top_feat in ['followers_count', 'avg_reposts', 'avg_comments']:
    print("- 优先与高粉丝、高互动率博主合作，他们的内容更容易被放大传播。")
elif top_feat in ['has_image', 'has_video']:
    print("- 极为重视视觉内容，每条博文必须配图或视频。")
elif top_feat in ['sentiment_enc', 'sentiment_score']:
    print("- 强化情绪表达，用鲜明情感驱动转发。")
else:
    print("- 结合发布时段和平台特点，通过实验找到最优组合。")

print("\n" + "=" * 60)
print("分析完成。可将 content_strategy_model.pkl 用于 Django 视图，向用户提供策略建议。")