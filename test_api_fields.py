# -*- coding: utf-8 -*-
"""检查推荐API专业项中的history_scores字段"""
import urllib.request
import json

url = 'http://localhost:8000/api/recommend/'
data = json.dumps({'score': 500, 'subject_type': 'physics'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req, timeout=10)
result = json.loads(resp.read().decode('utf-8'))

# 检查一个专业项的字段
bao = result['data']['bao']
if bao:
    first = bao[0]
    print("推荐列表中一个专业项的字段:")
    for k in sorted(first.keys()):
        v = first[k]
        if isinstance(v, (list, dict)):
            if k == 'history_scores' or k == 'recent_scores':
                years = [item.get('year') for item in v]
                print(f"  {k}: {len(v)}项，年份: {years}")
            elif k == 'score_info':
                print(f"  {k}: {v}")
            elif isinstance(v, dict):
                print(f"  {k}: {list(v.keys())}")
            else:
                print(f"  {k}: [...]")
        else:
            print(f"  {k}: {v}")

# 检查专业详情
print("\n" + "=" * 60)
print("专业详情API:")
major_id = first['major_id']
detail_url = f'http://localhost:8000/api/majors/{major_id}/?subject_type=physics'
req2 = urllib.request.Request(detail_url)
resp2 = urllib.request.urlopen(req2, timeout=10)
detail = json.loads(resp2.read().decode('utf-8'))
print("data字段:")
for k in sorted(detail['data'].keys()):
    v = detail['data'][k]
    if k == 'recent_scores' or k == 'history_scores' or k == 'scores':
        years = [item.get('year') for item in v] if isinstance(v, list) else []
        print(f"  {k}: {len(v)}项，年份: {years}")
    elif isinstance(v, dict):
        print(f"  {k}: {list(v.keys())}")
    elif isinstance(v, list):
        print(f"  {k}: [{len(v)}项]")
    else:
        print(f"  {k}: {v}")
