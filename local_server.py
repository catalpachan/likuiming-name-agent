#!/usr/bin/env python3
"""
本地開發服務器
直接使用本地 API 函數，不依賴 Vercel
"""
import http.server
import socketserver
import json
import os
import sys

# 添加 api 目錄到路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from calculate import handler as calculate_handler

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """處理 API 請求 - 直接調用本地函數"""
        if self.path == '/api/calculate':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                class LocalRequest:
                    method = 'POST'
                    json = data
                
                result = calculate_handler(LocalRequest())
                
                self.send_response(result.get('statusCode', 200))
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result['body'].encode('utf-8'))
                
            except Exception as e:
                error_resp = json.dumps({'success': False, 'error': str(e)})
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(error_resp.encode('utf-8'))
        
        elif self.path == '/api/generate-pdf':
            self.send_response(501)
            error_resp = json.dumps({'success': False, 'error': 'PDF generation not available locally'})
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(error_resp.encode('utf-8'))
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """處理靜態文件請求"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        return super().do_GET()
    
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
        print(f"✓ API: 直接調用本地函數")
        print(f"✓ 按 Ctrl+C 停止服務器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✓ 服務器已停止")
