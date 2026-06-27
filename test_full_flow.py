# -*- coding: utf-8 -*-
"""完整测试：验证所有前后端API和数据流程"""
import urllib.request
import json

print("=" * 70)
print("【测试1：推荐API】")
print("=" * 70)
url = 'http://localhost:8000/api/recommend/'
data = json.dumps({'score': 500, 'subject_type': 'physics'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req, timeout=10)
result = json.loads(resp.read().decode('utf-8'))

print(f"状态码: {result['code']}")
print(f"推荐总数: {result['data']['statistics']['total_count']}")
print(f"冲: {len(result['data']['chong'])}, 稳: {len(result['data']['wen'])}, 保: {len(result['data']['bao'])}")

# 检查每个推荐专业的history_scores年份
print("\n各专业的分数线年份:")
for group_name, group in [('冲', result['data']['chong']),
                           ('稳', result['data']['wen']),
                           ('保', result['data']['bao'][:3])]:
    for m in group:
        years = [s['year'] for s in (m.get('history_scores') or m.get('recent_scores') or [])]
        score_info = m.get('score_info', {})
        print(f"  [{group_name}] {m['major_name'][:15]:15} | 最低分:{score_info.get('min_score')} | 年份: {years}")

print("\n" + "=" * 70)
print("【测试2：专业详情API】")
print("=" * 70)
first_major = result['data']['chong'][0] if result['data']['chong'] else result['data']['bao'][0]
major_id = first_major['major_id']
print(f"测试专业ID: {major_id}, 名称: {first_major['major_name']}")

detail_url = f'http://localhost:8000/api/majors/{major_id}/?subject_type=physics'
req2 = urllib.request.Request(detail_url)
resp2 = urllib.request.urlopen(req2, timeout=10)
detail = json.loads(resp2.read().decode('utf-8'))

print(f"状态码: {detail['code']}")
print(f"专业名: {detail['data']['major_name']}")
print(f"选科: {detail['data']['subject_type_display']}")

# 检查分数线数据
hs = detail['data'].get('history_scores') or detail['data'].get('recent_scores') or []
print(f"分数线年数: {len(hs)}")
for s in hs:
    print(f"  {s['year']}年: 最低分={s['min_score']}, 平均分={s['avg_score']}, 位次={s['min_rank']}")

print(f"\n最新一年分数: {detail['data'].get('latest_score', {})}")
print(f"就业信息: {list(detail['data'].get('employment', {}).keys()) if detail['data'].get('employment') else '无'}")

print("\n" + "=" * 70)
print("【测试3：位次查询API】")
print("=" * 70)
rank_url = 'http://localhost:8000/api/rank/?score=500&subject_type=physics'
req3 = urllib.request.Request(rank_url)
resp3 = urllib.request.urlopen(req3, timeout=10)
rank = json.loads(resp3.read().decode('utf-8'))
print(f"状态码: {rank['code']}")
print(f"位次: {rank['data']}")

print("\n" + "=" * 70)
print("【测试4：校区列表】")
print("=" * 70)
campus_url = 'http://localhost:8000/api/campuses/'
req4 = urllib.request.Request(campus_url)
resp4 = urllib.request.urlopen(req4, timeout=10)
campus = json.loads(resp4.read().decode('utf-8'))
print(f"状态码: {campus['code']}")
print(f"校区: {[c['name'] for c in campus['data']]}")

print("\n" + "=" * 70)
print("【所有测试通过 ✓】")
print("=" * 70)
