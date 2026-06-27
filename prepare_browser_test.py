# -*- coding: utf-8 -*-
"""获取专业列表和详情数据，用于浏览器验证"""
import urllib.request
import json
import sys

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("【后端API验证】")
print("=" * 70)

# 1. 获取推荐
url = 'http://localhost:8000/api/recommend/'
data = json.dumps({'score': 500, 'subject_type': 'physics'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req, timeout=10)
result = json.loads(resp.read().decode('utf-8'))

# 展示冲稳保各专业及其ID
for group_name, group_key in [('【冲】', 'chong'), ('【稳】', 'wen'), ('【保】', 'bao')]:
    print(f"\n{group_name} 专业列表:")
    for m in result['data'][group_key]:
        score_info = m.get('score_info', {})
        print(f"  ID={m['major_id']:<3} | {m['major_name'][:15]:<15} | 最低分={score_info.get('min_score')} | 概率={m.get('probability')}%")

# 2. 获取第一个冲专业的详情
first_major = result['data']['chong'][0] if result['data']['chong'] else result['data']['bao'][0]
major_id = first_major['major_id']

print(f"\n" + "=" * 70)
print(f"【前端验证URL】")
print("=" * 70)
print(f"主页面:        http://localhost:5173")
print(f"专业详情示例:  http://localhost:5173/major/{major_id}?subject_type=physics")
print(f"                (专业: {first_major['major_name']}, ID={major_id})")

print(f"\n" + "=" * 70)
print(f"【该专业历年分数线数据预览】")
print("=" * 70)
detail_url = f'http://localhost:8000/api/majors/{major_id}/?subject_type=physics'
req2 = urllib.request.Request(detail_url)
resp2 = urllib.request.urlopen(req2, timeout=10)
detail = json.loads(resp2.read().decode('utf-8'))
hs = detail['data']['history_scores']
print(f"\n  {'年份':<8} {'最低分':<10} {'最高分':<10} {'平均分':<10} {'最低位次':<12} {'最高位次':<12}")
print(f"  {'-'*8} {'-'*10} {'-'*10} {'-'*10} {'-'*12} {'-'*12}")
for s in hs:
    print(f"  {s['year']:<8} {s['min_score']:<10.1f} {s['max_score']:<10.1f} {s['avg_score']:<10.1f} {s['min_rank']:<12} {s['max_rank']:<12}")

print(f"\n【请在浏览器中操作验证】:")
print(f"  1. 访问 http://localhost:5173")
print(f"  2. 输入分数 500，选择物理类，点击获取推荐")
print(f"  3. 点击任意专业卡片，查看详情页底部的历年分数线趋势图表")
print(f"  4. 验证是否显示5年数据(2021-2025)和双Y轴(分数线+位次)")
