# -*- coding: utf-8 -*-
"""测试API接口返回结构"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'libs'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahst_project.settings')
import django
django.setup()

from api.algorithms import MajorRecommender

r = MajorRecommender()
result = r.recommend(score=500, subject_type='physics')

print("API返回结构字段:", list(result.keys()))
print()
print("user_info:", result.get('user_info'))
print()
print("冲 (chong):", len(result.get('chong', [])))
print("稳 (wen):", len(result.get('wen', [])))
print("保 (bao):", len(result.get('bao', [])))
print()
print("statistics:", result.get('statistics'))
print()
print("smart_suggestion:", result.get('smart_suggestion'))

# 检查一个专业的详细计算
from api.models import Major, MajorScore, RankTable

print("\n\n" + "="*60)
print("详细计算过程")
print("="*60)

# 看看RankTable数据
rank_tables = RankTable.objects.filter(subject_type='physics').order_by('score')
print("\n物理类位次对照表数量:", rank_tables.count())
for rt in rank_tables[:5]:
    print(f"  {rt.score}分: 位次 {rt.min_rank}-{rt.max_rank}")
print("  ...")
for rt in rank_tables[-5:]:
    print(f"  {rt.score}分: 位次 {rt.min_rank}-{rt.max_rank}")

# 获取500分对应的位次
from api.algorithms import ScoreRankConverter
converter = ScoreRankConverter()
rank_info = converter.get_rank_by_score(500, 'physics')
print(f"\n500分对应的位次: {rank_info}")

# 试3个专业
print("\n各专业详细计算:")
majors = Major.objects.filter(subject_type='physics')[:5]
user_rank = rank_info['min_rank'] if rank_info else 0

for m in majors:
    s = MajorScore.objects.filter(major=m, subject_type='physics').order_by('-year').first()
    if s:
        score_diff = 500 - float(s.min_score)
        rank_ratio = user_rank / s.min_rank if s.min_rank > 0 else 0
        # 手动计算
        prob_score = r._calc_probability_by_score_diff(score_diff)
        prob_rank = r._calc_probability_by_rank_ratio(rank_ratio)
        final_prob = prob_score * 0.6 + prob_rank * 0.4
        level = r._classify_level(final_prob, score_diff, 'physics')
        print(f"  {m.name[:20]}: 专业最低分={s.min_score}, 位次={s.min_rank} | "
              f"分数差={score_diff:+.1f}, 位次比例={rank_ratio:.2f} | "
              f"概率分={prob_score:.1f}%, 概率位={prob_rank:.1f}% | "
              f"最终概率={final_prob:.1f}% | level={level}")
