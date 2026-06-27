# 简单可靠的前端静态文件服务器 + API 代理
# 同时提供前端静态文件和代理 /api/ 请求到 Django 后端
import http.server
import socketserver
import urllib.request
import urllib.error
import os
import sys

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
BACKEND_URL = 'http://localhost:8000'
PORT = 5173

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)
    
    def do_GET(self):
        if self.path.startswith('/api/') or self.path.startswith('/static/'):
            self.proxy_request('GET')
        else:
            # 处理根路径 / 
            if self.path == '/':
                self.path = '/index.html'
            # 对于没有扩展名的路径，返回 index.html (SPA 路由)
            _, ext = os.path.splitext(self.path)
            if not ext:
                self.path = '/index.html'
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.proxy_request('POST')
        else:
            self.send_error(405)
    
    def proxy_request(self, method):
        try:
            url = BACKEND_URL + self.path
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            
            req = urllib.request.Request(url, data=body, method=method)
            for key, value in self.headers.items():
                if key.lower() not in ['content-length', 'host']:
                    req.add_header(key, value)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                self.send_response(response.status)
                for key, value in response.headers.items():
                    if key.lower() not in ['content-length', 'transfer-encoding']:
                        self.send_header(key, value)
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_error(e.code, str(e))
        except Exception as e:
            self.send_error(502, f'Proxy Error: {str(e)}')
    
    def log_message(self, format, *args):
        pass  # 静默日志

print(f'前端服务启动于 http://localhost:{PORT}')
print(f'静态文件目录: {FRONTEND_DIR}')
print(f'API 代理到: {BACKEND_URL}')
print()
print('重要: 前端需要先构建!')
print('  cd frontend && npm run build')
print()

with socketserver.TCPServer(('0.0.0.0', PORT), ProxyHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n服务已停止')
