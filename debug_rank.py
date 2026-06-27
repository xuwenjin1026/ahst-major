import urllib.request
import json

# 测试不同的路由格式
test_urls = [
    "http://localhost:8000/api/rank/by-score/490/?subject_type=physics",
    "http://localhost:8000/api/rank/?score=490&subject_type=physics",
    "http://localhost:8000/api/rank/",
]

for url in test_urls:
    try:
        r = urllib.request.urlopen(url, timeout=10)
        data = r.read()
        print(f"[OK] {url}")
        print(f"   Response: {data[:200]}")
    except Exception as e:
        print(f"[FAIL] {url}")
        print(f"   Error: {e}")
    print()
