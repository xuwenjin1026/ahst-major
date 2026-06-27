import urllib.request

ports = [5173, 8080, 8081]

for port in ports:
    try:
        r = urllib.request.urlopen(f'http://localhost:{port}/', timeout=3)
        content = r.read().decode('utf-8')[:100]
        print(f'  端口 {port}: [OK] 首页, 内容包含: {content[:50]}...')
    except Exception as e:
        try:
            r2 = urllib.request.urlopen(f'http://localhost:{port}/api/campuses/', timeout=3)
            print(f'  端口 {port}: [部分OK] 首页失败但API正常: {e}')
        except Exception as e2:
            print(f'  端口 {port}: [失败] {e}')
