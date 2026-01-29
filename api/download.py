import json
import os

def handler(request):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '''
        <html>
        <head><title>PDF Download</title></head>
        <body>
            <h1>PDF 功能說明</h1>
            <p>PDF 下載功能需要在伺服器端有檔案儲存空間。</p>
            <p>Vercel Serverless 環境不支援長時間檔案儲存。</p>
            <p>建議使用本地部署來產生 PDF 報告。</p>
            <br>
            <a href="/">返回首頁</a>
        </body>
        </html>
        '''
    }
