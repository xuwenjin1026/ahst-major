import urllib.request
import urllib.parse
import json

print("="*60)
print("  安徽科技工程大学 - 专业推荐系统 - 最终验证")
print("="*60)
print()

results = []

def test(name, url, method='GET', body=None):
    try:
        headers = {}
        data = None
        if body:
            data = json.dumps(body).encode()
            headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        r = urllib.request.urlopen(req, timeout=10)
        if r.status == 200:
            results.append((name, True, None))
            print(f"[OK]   {name}")
        else:
            results.append((name, False, f"status={r.status}"))
            print(f"[WARN] {name}")
    except Exception as e:
        results.append((name, False, str(e)))
        print(f"[FAIL] {name}")

test("前端根路径 /", "http://localhost:5173/")
test("前端页面 /index.html", "http://localhost:5173/index.html")
test("API 代理 /api/campuses/", "http://localhost:5173/api/campuses/")
test("专业列表 /api/majors/", "http://localhost:5173/api/majors/")
test("物理类推荐 - 450分", "http://localhost:5173/api/recommend/", 'POST', {'score': 450, 'subject_type': 'physics'})
test("历史类推荐 - 500分", "http://localhost:5173/api/recommend/", 'POST', {'score': 500, 'subject_type': 'history'})
test("分数换位次 - 物理 490", "http://localhost:5173/api/rank/query/?score=490&subject_type=physics")
test("分数换位次 - 历史 510", "http://localhost:5173/api/rank/query/?score=510&subject_type=history")
test("统计数据", "http://localhost:5173/api/statistics/")

total = len(results)
passed = sum(1 for _, ok, _ in results if ok)
print()
print("="*60)
print(f"  结果: {passed}/{total} 通过")
if passed == total:
    print("  ✓ 全部正常！")
    print()
    print("  请在浏览器中打开:")
    print("    http://localhost:5173/")
    print()
    print("  使用说明:")
    print("    1. 输入高考分数 (0-750)")
    print("    2. 选择 物理 / 历史")
    print("    3. 点击 '开始推荐'")
    print("    4. 查看冲/稳/保三个梯队的专业推荐")
    print()
    print("  当前服务运行状态:")
    print("    - 前端开发服务器: http://localhost:5173/ (Vite + Vue3)")
    print("    - Django后端:    http://localhost:8000/")
    print("    - 数据库:         SQLite (backend/db.sqlite3)")
else:
    print("  ✗ 有部分失败")
    print("  请检查:")
    print("    - 后端 Django 服务是否在运行 (cd backend && python manage.py runserver 8000)")
    for name, ok, err in results:
        if not ok:
            print(f"    - {name}: {err}")
print("="*60)
