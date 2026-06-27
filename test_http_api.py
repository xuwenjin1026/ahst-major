# -*- coding: utf-8 -*-
"""测试完整的HTTP API接口"""
import urllib.request
import urllib.parse
import json

url = 'http://localhost:8000/api/recommend/'
data = json.dumps({'score': 500, 'subject_type': 'physics'}).encode('utf-8')

req = urllib.request.Request(
    url,
    data=data,
    headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
)

try:
    resp = urllib.request.urlopen(req, timeout=10)
    result = json.loads(resp.read().decode('utf-8'))
    print("状态码:", result.get('code'))
    print()
    print("data字段:", list(result.get('data', {}).keys()))
    print()
    d = result.get('data', {})
    print("statistics:", d.get('statistics'))
    print("chong 数量:", len(d.get('chong', [])))
    print("wen 数量:", len(d.get('wen', [])))
    print("bao 数量:", len(d.get('bao', [])))
    if d.get('chong'):
        print("\n第一个冲专业:")
        first = d['chong'][0]
        print("  major_name:", first.get('major_name'))
        print("  min_score:", first.get('score_info', {}).get('min_score'))
        print("  probability:", first.get('probability'))
        print("  level:", first.get('level'))
        print("  recent_scores年份:", [s.get('year') for s in (first.get('history_scores') or first.get('recent_scores') or [])])
except Exception as e:
    print("错误:", e)
    import traceback
    traceback.print_exc()
