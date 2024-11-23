from flask import Flask, request, Response
from flask_cors import CORS
import requests
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return 'Missing URL parameter', 400
    
    logger.info(f"Proxying request to: {url}")
    
    try:
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # 发送请求
        response = requests.get(url, headers=headers, timeout=10)
        logger.info(f"Response status code: {response.status_code}")
        
        # 获取内容类型
        content_type = response.headers.get('content-type', 'text/html')
        logger.info(f"Content type: {content_type}")
        
        # 创建响应
        proxy_response = Response(
            response.content,
            status=response.status_code
        )
        
        # 设置基本headers
        proxy_response.headers['Content-Type'] = content_type
        proxy_response.headers['Access-Control-Allow-Origin'] = '*'
        proxy_response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        proxy_response.headers['Access-Control-Allow-Headers'] = '*'
        proxy_response.headers['X-Frame-Options'] = 'ALLOWALL'
        
        logger.info("Successfully proxied request")
        return proxy_response
        
    except requests.Timeout:
        logger.error("Request timed out")
        return 'Request timed out', 504
    except requests.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return f'Error fetching URL: {str(e)}', 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f'Unexpected error: {str(e)}', 500

if __name__ == '__main__':
    app.run(port=5000, debug=True) 