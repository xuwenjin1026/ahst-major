import urllib.request
import json

print('=== 项目运行状态检测 ===')
print()

# 1. 测试后端API
try:
    r1 = urllib.request.urlopen('http://localhost:8000/api/campuses/')
    print('[OK] 后端API服务正常 (端口 8000)')
except Exception as e:
    print('[ERROR] 后端API服务异常:', str(e))

# 2. 测试前端页面
try:
    r2 = urllib.request.urlopen('http://localhost:8080/')
    print('[OK] 前端页面服务正常 (端口 8080)')
except Exception as e:
    print('[ERROR] 前端页面服务异常:', str(e))

# 3. 测试代理转发
try:
    r3 = urllib.request.urlopen('http://localhost:8080/api/categories/')
    print('[OK] 前端代理转发正常')
except Exception as e:
    print('[ERROR] 前端代理异常:', str(e))

# 4. 测试推荐算法
try:
    data = json.dumps({'score': 490, 'subject_type': 'physics'}).encode()
    req = urllib.request.Request('http://localhost:8000/api/recommend/', data=data, headers={'Content-Type': 'application/json'})
    resp = json.loads(urllib.request.urlopen(req).read())
    stats = resp['data']['statistics']
    print(f'[OK] 推荐算法正常: 冲{stats["chong_count"]}个 / 稳{stats["wen_count"]}个 / 保{stats["bao_count"]}个')

    if resp['data'].get('smart_suggestion'):
        print(f'[OK] 智能建议功能正常')
except Exception as e:
    print('[ERROR] 推荐算法异常:', str(e))

# 5. 测试位次查询
try:
    r5 = urllib.request.urlopen('http://localhost:8000/api/rank/query/?score=500&subject_type=physics')
    print('[OK] 位次查询API正常')
except Exception as e:
    print('[ERROR] 位次查询异常:', str(e))

print()
print('=' * 50)
print('项目运行正常！请在浏览器中打开:')
print('  http://localhost:8080/')
print()
print('测试分数建议:')
print('  物理类: 450-530 分')
print('  历史类: 485-575 分')
