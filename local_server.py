#!/usr/bin/env python3
"""
本地開發服務器
同時提供靜態頁面和 API 代理到 Vercel
"""
import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os

PORT = 8080
VERCEL_API_URL = "https://likuiming-name-agent.vercel.app"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """處理 API 請求"""
        if self.path.startswith('/api/'):
            # 轉發到 Vercel
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                vercel_url = VERCEL_API_URL + self.path
                req = urllib.request.Request(
                    vercel_url,
                    data=post_data,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0'
                    },
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    response_data = response.read().decode('utf-8')
                    self.send_response(response.status)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response_data.encode('utf-8'))
                    
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(error_body.encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_resp = json.dumps({'success': False, 'error': str(e)})
                self.wfile.write(error_resp.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """處理 CORS 預檢請求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    os.chdir('templates')
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"✓ 本地服務器運行中: http://localhost:{PORT}")
        print(f"✓ API 將轉發到: {VERCEL_API_URL}")
        print(f"✓ 按 Ctrl+C 停止服務器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✓ 服務器已停止")
