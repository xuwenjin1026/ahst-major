import urllib.request
import json

print("=== 测试前端完整功能 ===")
print()

# 测试 index.html
try:
    r = urllib.request.urlopen('http://localhost:5173/index.html')
    data = r.read().decode('utf-8')
    if '<div id="app">' in data and '<script' in data:
        print('[OK] index.html 正常，包含 Vue 应用挂载点')
    else:
        print('[WARN] index.html 内容可能不完整')
except Exception as e:
    print(f'[ERROR] index.html: {e}')

# 测试 /api/ 代理
try:
    r = urllib.request.urlopen('http://localhost:5173/api/campuses/')
    data = json.loads(r.read())
    if data.get('code') == 200:
        print('[OK] API 代理正常')
except Exception as e:
    print(f'[ERROR] API: {e}')

# 测试推荐
try:
    body = json.dumps({'score': 490, 'subject_type': 'physics'}).encode()
    req = urllib.request.Request('http://localhost:5173/api/recommend/', data=body, headers={'Content-Type': 'application/json'})
    r = urllib.request.urlopen(req)
    data = json.loads(r.read())
    majors = data.get('data', {}).get('chong', []) + data.get('data', {}).get('wen', []) + data.get('data', {}).get('bao', [])
    if len(majors) > 0:
        print(f'[OK] 推荐功能正常，共 {len(majors)} 个专业')
except Exception as e:
    print(f'[ERROR] recommend: {e}')

print()
print("="*50)
print("请在浏览器中打开:")
print("  http://localhost:5173/index.html")
print()
print("如果这个地址能正常加载，说明应用就能使用")
print("可能遇到的问题: 根路径 '/' 显示 404，但直接访问 index.html 正常")
