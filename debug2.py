import http.client

print("=== 测试 localhost:5173 ===")
conn = http.client.HTTPConnection('localhost', 5173, timeout=5)

# 多次测试 /
for path in ['/', '/index.html', '/favicon.svg', '/src/App.vue']:
    conn.request('GET', path)
    resp = conn.getresponse()
    data = resp.read()
    headers = dict(resp.getheaders())
    print(f'\nGET {path}: {resp.status}')
    print(f'  Content-Type: {headers.get("Content-Type", "N/A")}')
    print(f'  Server: {headers.get("Server", "N/A")}')
    print(f'  X-Powered-By: {headers.get("X-Powered-By", "N/A")}')
    print(f'  Body length: {len(data)}')

conn.close()

print("\n=== 测试 localhost:8000 (后端) ===")
conn = http.client.HTTPConnection('localhost', 8000, timeout=5)
for path in ['/', '/api/campuses/']:
    conn.request('GET', path)
    resp = conn.getresponse()
    data = resp.read()
    headers = dict(resp.getheaders())
    print(f'\nGET {path}: {resp.status}')
    print(f'  Content-Type: {headers.get("Content-Type", "N/A")}')
    print(f'  Server: {headers.get("Server", "N/A")}')

conn.close()
