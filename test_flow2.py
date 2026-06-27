# -*- coding: utf-8 -*-
"""测试完整流程"""
import os
import sys

# 添加libs路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'libs'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahst_project.settings')

import django
django.setup()

from api.models import Major, MajorScore
from api.algorithms import MajorRecommender

print("=" * 60)
print("【测试1：数据完整性检查】")
print("=" * 60)

for subject_type in ['physics', 'history']:
    print("\n%s 类：" % subject_type)
    years = MajorScore.objects.filter(subject_type=subject_type).values_list('year', flat=True).distinct()
    print("  有数据的年份: %s" % sorted(list(set(years))))
    majors = Major.objects.filter(subject_type=subject_type)
    print("  专业数量: %s" % majors.count())
    for m in majors[:10]:
        s = MajorScore.objects.filter(major=m, subject_type=subject_type).order_by('-year').first()
        if s:
            print("    %s: %s最低分=%s, 位次=%s" % (m.name[:20], s.year, s.min_score, s.min_rank))

print("\n" + "=" * 60)
print("【测试2：推荐算法】")
print("=" * 60)

r = MajorRecommender()

for score in [460, 480, 500, 520]:
    result = r.recommend(score=score, subject_type='physics')
    recs = result.get('recommendations', [])
    print("\n  分数 %s 分：推荐 %s 个专业" % (score, len(recs)))
    levels = {}
    for rec in recs:
        lv = rec.get('level', 'unknown')
        levels[lv] = levels.get(lv, 0) + 1
    print("    分层统计: %s" % levels)
    if recs:
        for rec in recs[:3]:
            print("    - %s: 最低分=%s, 概率=%s%%, level=%s" % (
                rec['major_name'][:20], rec.get('min_score'), rec.get('probability'), rec.get('level')))

print("\n【测试完成】")
