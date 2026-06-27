# -*- coding: utf-8 -*-
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

libs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahst_project.settings')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

import django
django.setup()

from api.algorithms import ScoreRankConverter, MajorRecommender

print("=" * 70)
print("  推荐算法测试")
print("=" * 70)
print()

recommender = MajorRecommender()

test_cases = [
    (510, 'physics', '物理类 510分'),
    (540, 'history', '历史类 540分'),
    (550, 'physics', '物理类 550分(高分)'),
    (460, 'physics', '物理类 460分(低分)'),
    (525, 'physics', '物理类 525分(中等)'),
    (490, 'history', '历史类 490分(低分)'),
]

for score, subject_type, desc in test_cases:
    print("【", desc, "】")
    
    # 获取位次信息
    rank_info = ScoreRankConverter.get_rank_by_score(score, subject_type)
    if rank_info:
        user_rank = (rank_info.get('min_rank', 0) + rank_info.get('max_rank', 0)) // 2
        print("  位次:", user_rank, "(位次表:", rank_info.get('min_rank'), "-", rank_info.get('max_rank'), ")")
    else:
        print("  位次: 无数据")
    
    result = recommender.recommend(score, subject_type)
    
    if result:
        chong = result.get('chong', [])
        wen = result.get('wen', [])
        bao = result.get('bao', [])
        total = len(chong) + len(wen) + len(bao)
        
        print("  推荐总数:", total, "个专业")
        print("    冲:", len(chong), "个")
        for item in chong[:2]:
            print("      -", item.get('major_name', ''), ": 概率=", item.get('probability', 0), "%, 分差=", item.get('score_diff', 0), "分")
        
        print("    稳:", len(wen), "个")
        for item in wen[:2]:
            print("      -", item.get('major_name', ''), ": 概率=", item.get('probability', 0), "%, 分差=", item.get('score_diff', 0), "分")
        
        print("    保:", len(bao), "个")
        for item in bao[:2]:
            print("      -", item.get('major_name', ''), ": 概率=", item.get('probability', 0), "%, 分差=", item.get('score_diff', 0), "分")
        
        stats = result.get('statistics', {})
        print("  分数差范围:", stats.get('min_score_diff', 0), "到", stats.get('max_score_diff', 0), "分")
    
    print()

print("=" * 70)
print("  测试完成")
print("=" * 70)
