# -*- coding: utf-8 -*-
"""测试专业详情API接口"""
import urllib.request
import json

# 先获取一个专业ID
url = 'http://localhost:8000/api/recommend/'
data = json.dumps({'score': 500, 'subject_type': 'physics'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req, timeout=10)
result = json.loads(resp.read().decode('utf-8'))

# 获取第一个冲专业
chong = result['data']['chong']
if chong:
    major_id = chong[0]['major_id']
    print(f"专业ID: {major_id}")
    print(f"专业名: {chong[0]['major_name']}")
    
    # 请求该专业详情
    detail_url = f'http://localhost:8000/api/majors/{major_id}/?subject_type=physics'
    req2 = urllib.request.Request(detail_url)
    resp2 = urllib.request.urlopen(req2, timeout=10)
    detail = json.loads(resp2.read().decode('utf-8'))
    
    print(f"\n专业详情状态码: {detail['code']}")
    print(f"data字段: {list(detail['data'].keys())}")
    
    recent = detail['data'].get('recent_scores', [])
    print(f"recent_scores 年数: {len(recent)}")
    for s in recent:
        print(f"  {s}")
    # 检查是否还有history_scores字段
    hs = detail['data'].get('history_scores')
    print(f"\nhistory_scores: {len(hs) if hs else '无此字段'}")
