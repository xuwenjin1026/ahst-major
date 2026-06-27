# -*- coding: utf-8 -*-
import urllib.request
import json

data = json.dumps({'score': 510, 'subject_type': 'physics'}).encode()
req = urllib.request.Request('http://localhost:8000/api/recommend/', data=data, headers={'Content-Type': 'application/json'})
try:
    r = urllib.request.urlopen(req)
    result = json.loads(r.read())
    print('Keys:', list(result.keys()))
    if 'code' in result:
        print('code:', result['code'])
        print('message:', result.get('message', ''))
        if 'data' in result:
            data = result['data']
            print('data keys:', list(data.keys()))
            if 'statistics' in data:
                print('statistics:', data['statistics'])
            if 'chong' in data:
                print('chong count:', len(data['chong']))
                print('wen count:', len(data['wen']))
                print('bao count:', len(data['bao']))
except Exception as e:
    print('Error:', e)
