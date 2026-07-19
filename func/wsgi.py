import sys
import os
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()


def handler(event, context):
    http_event = event.get('httpEvent', event.get('http', {}))
    method = http_event.get('method', 'GET')
    path = http_event.get('path', '/')
    headers = dict(http_event.get('headers', {}))
    body = http_event.get('body', '') or ''
    query_string = http_event.get('queryString', '') or ''
    
    wsgi_env = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_LENGTH': str(len(body)),
        'wsgi.input': body.encode('utf-8'),
        'wsgi.url_scheme': 'https',
        'SERVER_NAME': 'example.com',
        'SERVER_PORT': '443',
    }
    
    for key, value in headers.items():
        wsgi_key = f'HTTP_{key.upper().replace("-", "_")}'
        if wsgi_key not in wsgi_env:
            wsgi_env[wsgi_key] = value
    
    response_data = {'status': '', 'headers': [], 'body': b''}
    
    def start_response(status, response_headers, exc_info=None):
        response_data['status'] = status
        response_data['headers'] = response_headers
        if exc_info:
            raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])
    
    from mysite.wsgi import application
    app_iter = application(wsgi_env, start_response)
    
    for chunk in app_iter:
        if isinstance(chunk, str):
            chunk = chunk.encode('utf-8')
        response_data['body'] += chunk
    
    body_str = response_data['body'].decode('utf-8', errors='replace')
    
    return {
        'statusCode': int(response_data['status'].split()[0]),
        'headers': {k: v for k, v in response_data['headers']},
        'body': body_str,
        'isBase64Encoded': False
    }
