import urllib.request
import json

# 测试1: 最简请求（不带 filter）
print("=== 测试1: 最简请求 ===")
try:
    req = urllib.request.Request(
        'http://localhost:5173/api/recommend/',
        data=json.dumps({'score': 500, 'subject_type': 'physics'}).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"状态码: {resp.status}")
    print(f"code: {data.get('code')}, message: {data.get('message')}")
    print(f"专业数: {data.get('data', {}).get('statistics', {}).get('total_count', 0)}")
except urllib.error.HTTPError as e:
    print(f"HTTP 错误: {e.code}")
    print(f"响应体: {e.read().decode()}")
except Exception as e:
    print(f"其他错误: {e}")

print()

# 测试2: 带 campus_filter (字符串名称)
print("=== 测试2: 带 campus_filter (字符串) ===")
try:
    req = urllib.request.Request(
        'http://localhost:5173/api/recommend/',
        data=json.dumps({
            'score': 500,
            'subject_type': 'physics',
            'campus_filter': ['蚌埠校区', '滁州校区']
        }).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"状态码: {resp.status}")
    print(f"code: {data.get('code')}, message: {data.get('message')}")
except urllib.error.HTTPError as e:
    print(f"HTTP 错误: {e.code}")
    print(f"响应体: {e.read().decode()}")

print()

# 测试3: 带 category_filter (字符串名称 - 前端传的)
print("=== 测试3: 带 category_filter (字符串) ===")
try:
    req = urllib.request.Request(
        'http://localhost:5173/api/recommend/',
        data=json.dumps({
            'score': 500,
            'subject_type': 'physics',
            'category_filter': ['工学', '理学']
        }).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"状态码: {resp.status}")
    print(f"code: {data.get('code')}, message: {data.get('message')}")
except urllib.error.HTTPError as e:
    print(f"HTTP 错误: {e.code}")
    print(f"响应体: {e.read().decode()}")

print()

# 测试4: 带 category_filter (整数ID - 后端要求)
print("=== 测试4: 带 category_filter (整数) ===")
try:
    req = urllib.request.Request(
        'http://localhost:5173/api/recommend/',
        data=json.dumps({
            'score': 500,
            'subject_type': 'physics',
            'category_filter': [1, 2]
        }).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"状态码: {resp.status}")
    print(f"code: {data.get('code')}, message: {data.get('message')}")
except urllib.error.HTTPError as e:
    print(f"HTTP 错误: {e.code}")
    print(f"响应体: {e.read().decode()}")

print()

# 测试5: 分数为 null/空值
print("=== 测试5: score 为 null ===")
try:
    req = urllib.request.Request(
        'http://localhost:5173/api/recommend/',
        data=json.dumps({'score': None, 'subject_type': 'physics'}).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"状态码: {resp.status}")
except urllib.error.HTTPError as e:
    print(f"HTTP 错误: {e.code}")
    print(f"响应体: {e.read().decode()}")
