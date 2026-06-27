# -*- coding: utf-8 -*-
"""测试完整流程"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahst_project.settings')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
django.setup()

from api.models import Major, MajorScore
from api.algorithms import MajorRecommender

print("=" * 60)
print("【测试1：数据完整性检查】")
print("=" * 60)

# 检查各年份数据
for subject_type in ['physics', 'history']:
    print(f"\n{subject_type} 类：")
    years = MajorScore.objects.filter(subject_type=subject_type).values_list('year', flat=True).distinct()
    print(f"  有数据的年份: {sorted(list(set(years)))}")
    majors = Major.objects.filter(subject_type=subject_type)
    print(f"  专业数量: {majors.count()}")
    # 显示每个专业的2025最低分
    for m in majors[:10]:
        s = MajorScore.objects.filter(major=m, subject_type=subject_type).order_by('-year').first()
        if s:
            print(f"    {m.name[:20]}: {s.year}最低分={s.min_score}, 位次={s.min_rank}")

print("\n" + "=" * 60)
print("【测试2：推荐算法】")
print("=" * 60)

r = MajorRecommender()

for score in [460, 480, 500, 520]:
    result = r.recommend(score=score, subject_type='physics')
    recs = result.get('recommendations', [])
    print(f"\n  分数 {score} 分：推荐 {len(recs)} 个专业")
    levels = {}
    for rec in recs:
        lv = rec.get('level', 'unknown')
        levels[lv] = levels.get(lv, 0) + 1
    print(f"    分层统计: {levels}")
    if recs:
        # 显示前3个
        for rec in recs[:3]:
            print(f"    - {rec['major_name'][:20]}: 最低分={rec.get('min_score')}, 概率={rec.get('probability')}%, level={rec.get('level')}")

print("\n" + "=" * 60)
print("【测试3：详细概率计算】")
print("=" * 60)

# 测试某个分数的详细计算
test_major = Major.objects.filter(subject_type='physics').first()
if test_major:
    print(f"\n测试专业: {test_major.name}")
    scores = MajorScore.objects.filter(major=test_major, subject_type='physics').order_by('-year')
    print("历年分数线:")
    for s in scores:
        print(f"  {s.year}: 最低分={s.min_score}, 位次={s.min_rank}")

print("\n" + "=" * 60)
print("【测试完成】")
print("=" * 60)
