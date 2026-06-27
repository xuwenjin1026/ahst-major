import urllib.request
import json

print("=" * 60)
print("修复验证 - 测试各种请求场景")
print("=" * 60)
print()

test_cases = [
    ("1. 最简请求（无筛选）",
     {'score': 490, 'subject_type': 'physics'}),
    ("2. 带 campus_filter（字符串数组）",
     {'score': 490, 'subject_type': 'physics',
      'campus_filter': ['蚌埠校区', '滁州校区']}),
    ("3. 带 category_filter（字符串数组 - 修复前会 400）",
     {'score': 490, 'subject_type': 'physics',
      'category_filter': ['工学', '理学']}),
    ("4. 同时带两个 filter（字符串数组）",
     {'score': 490, 'subject_type': 'physics',
      'campus_filter': ['蚌埠校区'],
      'category_filter': ['工学']}),
    ("5. campus_filter 为 null（前端未勾选时传的值）",
     {'score': 490, 'subject_type': 'physics',
      'campus_filter': None, 'category_filter': None}),
    ("6. campus_filter 为空数组",
     {'score': 490, 'subject_type': 'physics',
      'campus_filter': [], 'category_filter': []}),
    ("7. 历史类推荐",
     {'score': 520, 'subject_type': 'history'}),
    ("8. 历史类带筛选",
     {'score': 520, 'subject_type': 'history',
      'campus_filter': ['凤阳校区'],
      'category_filter': ['文学']}),
    ("9. 边界分数 - 高难度（520）",
     {'score': 520, 'subject_type': 'physics'}),
    ("10. 边界分数 - 保底（450）",
     {'score': 450, 'subject_type': 'physics'}),
]

passed = 0
failed = 0

for name, payload in test_cases:
    try:
        req = urllib.request.Request(
            'http://localhost:8000/api/recommend/',
            data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())

        if data.get('code') == 200:
            total = data.get('data', {}).get('statistics', {}).get('total_count', 0)
            chong = data.get('data', {}).get('statistics', {}).get('chong_count', 0)
            wen = data.get('data', {}).get('statistics', {}).get('wen_count', 0)
            bao = data.get('data', {}).get('statistics', {}).get('bao_count', 0)
            print(f"  [OK]   {name}")
            print(f"         → 推荐 {total} 个专业（冲{chong}/稳{wen}/保{bao}）")
            passed += 1
        else:
            print(f"  [WARN] {name}")
            print(f"         → code={data.get('code')}, message={data.get('message')}")
            failed += 1
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err_data = json.loads(body)
            print(f"  [FAIL] {name}")
            print(f"         → HTTP {e.code}: {err_data.get('message')}")
            if err_data.get('errors'):
                print(f"         → 详细错误: {err_data['errors']}")
        except:
            print(f"  [FAIL] {name}: HTTP {e.code} - {body[:100]}")
        failed += 1
    except Exception as e:
        print(f"  [ERR]  {name}: {e}")
        failed += 1
    print()

print("=" * 60)
print(f"结果: {passed}/{passed + failed} 通过")
if failed == 0:
    print("✅ 全部通过！")
else:
    print(f"❌ 有 {failed} 个失败")
print("=" * 60)
