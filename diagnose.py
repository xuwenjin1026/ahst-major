# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'libs'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahst_project.settings')
import django
django.setup()

from api.algorithms import ScoreRankConverter, MajorRecommender
from api.models import Major, MajorScore, RankTable, Campus, MajorCategory
from django.db.models import Max, Min, Avg

print("=" * 70)
print("【安徽科技工程大学专业推荐系统 - 完整诊断报告】")
print("=" * 70)

# 1. 基础数据统计
print("\n📊 【1. 数据总量统计】")
print(f"  校区数量: {Campus.objects.count()}")
print(f"  专业分类: {MajorCategory.objects.count()}")
print(f"  专业数量: {Major.objects.count()}")
print(f"  物理类专业: {Major.objects.filter(subject_type='physics').count()}")
print(f"  历史类专业: {Major.objects.filter(subject_type='history').count()}")
print(f"  分数线记录: {MajorScore.objects.count()}")
print(f"  位次对照记录: {RankTable.objects.count()}")

# 2. 各校区专业分布
print(f"\n📊 【2. 各校区专业分布】")
for campus in Campus.objects.all():
    phy_count = Major.objects.filter(campus=campus, subject_type='physics').count()
    his_count = Major.objects.filter(campus=campus, subject_type='history').count()
    print(f"  {campus.name}: 物理类{phy_count}个, 历史类{his_count}个")

# 3. 物理类专业分数范围
print(f"\n📊 【3. 物理类分数线统计】")
phy_scores = MajorScore.objects.filter(subject_type='physics', year=2023).aggregate(
    min_s=Min('min_score'), max_s=Max('min_score'), avg_s=Avg('min_score'),
    min_r=Min('min_rank'), max_r=Max('min_rank')
)
print(f"  最低分范围: {phy_scores['min_s']} ~ {phy_scores['max_s']} (平均{phy_scores['avg_s']:.1f})")
print(f"  最低位次范围: {phy_scores['min_r']} ~ {phy_scores['max_r']}")

# 4. 历史类分数范围
print(f"\n📊 【4. 历史类分数线统计】")
his_scores = MajorScore.objects.filter(subject_type='history', year=2023).aggregate(
    min_s=Min('min_score'), max_s=Max('min_score'), avg_s=Avg('min_score'),
    min_r=Min('min_rank'), max_r=Max('min_rank')
)
if his_scores['min_s']:
    print(f"  最低分范围: {his_scores['min_s']} ~ {his_scores['max_s']} (平均{his_scores['avg_s']:.1f})")
    print(f"  最低位次范围: {his_scores['min_r']} ~ {his_scores['max_r']}")
else:
    print("  ⚠️  没有历史类数据！")

# 5. 位次表测试
print(f"\n📊 【5. 位次对照表】")
for subject in ['physics', 'history']:
    latest = RankTable.objects.filter(subject_type=subject).aggregate(max_year=Max('year'))['max_year'] or 2023
    count = RankTable.objects.filter(subject_type=subject, year=latest).count()
    if count > 0:
        score_range = RankTable.objects.filter(subject_type=subject, year=latest).aggregate(
            min_s=Min('score'), max_s=Max('score')
        )
        print(f"  {subject}({latest}年): {count}条记录")
        print(f"    分数范围: {score_range['min_s']}分 ~ {score_range['max_s']}分")
    else:
        print(f"  ⚠️  {subject}: 没有位次数据！")

# 6. 专业分数线与位次表一致性检查
print(f"\n📊 【6. 位次数据一致性验证】")
converter = ScoreRankConverter()

print("  物理类专业抽样验证:")
phy_majors = MajorScore.objects.filter(subject_type='physics', year=2023).select_related('major')[:10]
for ms in phy_majors:
    # 用位次表验证该分数对应位次
    rank_info = converter.get_rank_by_score(ms.min_score, 'physics', 2023)
    table_min_rank = rank_info['min_rank'] if rank_info else -1
    diff = abs(ms.min_rank - table_min_rank) if table_min_rank > 0 else -1
    status = "✓" if diff >= 0 and diff < 5000 else "⚠️"
    print(f"    {status} {ms.major.name}: 最低分={ms.min_score}, 表中位次={table_min_rank}, 专业位次={ms.min_rank}, 差={diff}")

print("  历史类专业抽样验证:")
his_majors = MajorScore.objects.filter(subject_type='history', year=2023).select_related('major')[:10]
for ms in his_majors:
    rank_info = converter.get_rank_by_score(ms.min_score, 'history', 2023)
    table_min_rank = rank_info['min_rank'] if rank_info else -1
    diff = abs(ms.min_rank - table_min_rank) if table_min_rank > 0 else -1
    status = "✓" if diff >= 0 and diff < 3000 else "⚠️"
    print(f"    {status} {ms.major.name}: 最低分={ms.min_score}, 表中位次={table_min_rank}, 专业位次={ms.min_rank}, 差={diff}")

# 7. 推荐算法完整诊断
print(f"\n" + "=" * 70)
print("【7. 推荐算法诊断】")
print("=" * 70)

recommender = MajorRecommender()

test_cases = [
    (445, 'physics', '低分物理'),
    (470, 'physics', '中等物理'),
    (490, 'physics', '中高物理'),
    (515, 'physics', '高分物理'),
    (490, 'history', '低分历史'),
    (520, 'history', '中等历史'),
    (545, 'history', '高分历史'),
]

for score, subject, desc in test_cases:
    print(f"\n▶ {score}分-{desc}({subject})")
    result = recommender.recommend(score, subject)
    if 'error' in result:
        print(f"  ❌ 错误: {result['error']}")
        continue
    
    user_rank = result['user_info']['rank']
    stats = result['statistics']
    print(f"  用户位次: {user_rank} | 冲:{stats['chong_count']} 稳:{stats['wen_count']} 保:{stats['bao_count']}")
    
    # 显示每个分类前2个
    for level_name, level_key in [('冲刺','chong'), ('稳妥','wen'), ('保底','bao')]:
        majors = result[level_key]
        if majors:
            print(f"  ├─ {level_name}区:")
            for m in majors[:2]:
                print(f"  │  {m['major_name']}({m['campus']['name']}) | 录取概率{m['probability']}% | 分数差{m['score_diff']:+.0f} | 位次比{m['rank_ratio']:.2f}")

print("\n" + "=" * 70)
print("【诊断完毕 - 如所有✓表示数据一致性良好】")
print("=" * 70)
