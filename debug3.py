import http.client

conn = http.client.HTTPConnection('localhost', 5173, timeout=5)

for path in ['/', '/index.html']:
    conn.request('GET', path)
    resp = conn.getresponse()
    data = resp.read()
    print(f'GET {path}: {resp.status}')
    print(f'  Body (first 200): {data[:200]}')
    print()

conn.close()
