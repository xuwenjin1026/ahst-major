import urllib.request
import http.client

conn = http.client.HTTPConnection('localhost', 5173, timeout=5)

# 测试根路径
conn.request('GET', '/')
resp = conn.getresponse()
data = resp.read()
print(f'GET / : {resp.status}')
print(f'Headers: {dict(resp.getheaders())}')
print(f'Body (first 300): {data[:300]}')
print()

# 测试 /index.html
conn.request('GET', '/index.html')
resp = conn.getresponse()
data = resp.read()
print(f'GET /index.html : {resp.status}')
print(f'Body: {data[:300]}')
print()

# 测试 /src/main.js
conn.request('GET', '/src/main.js')
resp = conn.getresponse()
data = resp.read()
print(f'GET /src/main.js : {resp.status}')
print(f'Body: {data[:200]}')

conn.close()
