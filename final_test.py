import urllib.request
import urllib.parse
import json
import sys

print("="*60)
print("  安徽科技工程大学 - 专业推荐系统 - 最终验证")
print("="*60)
print()

all_ok = True

def test(name, url, method='GET', body=None, check=None):
    global all_ok
    try:
        headers = {}
        data = None
        if body:
            data = json.dumps(body).encode()
            headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        r = urllib.request.urlopen(req, timeout=10)
        result = json.loads(r.read())
        if check and not check(result):
            print(f"[FAIL] {name}")
            all_ok = False
            return
        print(f"[OK]   {name}")
    except Exception as e:
        print(f"[FAIL] {name} - {e}")
        all_ok = False

test("前端页面 /  (http://localhost:5173/)")
test("前端页面 /index.html (http://localhost:5173/index.html)")
test("校区列表 API (http://localhost:5173/api/campuses/)")
test("物理类推荐 - 450分",
     'http://localhost:5173/api/recommend/',
     'POST', {'score': 450, 'subject_type': 'physics'})
test("历史类推荐 - 500分",
     'http://localhost:5173/api/recommend/',
     'POST', {'score': 500, 'subject_type': 'history'})
test("分数换位次 (http://localhost:5173/api/rank/by-score/490/?subject_type=physics)")

print()
print("="*60)
if all_ok:
    print("  全部测试通过！")
    print()
    print("  使用方法:")
    print("    1. 在浏览器中打开 http://localhost:5173/")
    print("    2. 输入高考分数 (0-750)")
    print("    3. 选择物理/历史")
    print("    4. 点击推荐")
    print()
else:
    print("  部分测试失败，请检查后端服务是否启动")
    print("  启动命令: cd backend && python manage.py runserver 8000")
print("="*60)
