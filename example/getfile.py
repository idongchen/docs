#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from flask import Flask
from flask import request
from flask import json
# 解决跨域问题
from flask_cors import CORS

# 或者io，使用哪种包无所谓
import codecs




app = Flask(__name__)
# 解决跨域问题，以下两种CORS写法都可以
# CORS(app, supports_credentials=True)
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(app, resources=r'/*')


@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return json.dumps({'content': '','resCode':2000})
    else:
        return '<h1>只接受post请求！</h1>'



# 接收参数并响应def，ajax可以访问哦
@app.route('/getdata/md', methods=['post'])
def ajax_test_add():
    # print(request)
    params = request.get_json()
    print(params.get('title'))
    childPath = params.get('title')
    if(params.get('title') == None):
        print('未传title字段！')
        return json.dumps({'resCode':'4001','msg':'参数错误title为必传'})
    else:
        path = childPath + '.md'
        print(path)
        try:
            f_name = open(path, 'r', encoding='UTF-8').read()
            print(f_name)
            return json.dumps({'content':f_name,'resCode':2000})

        except OSError as reason:
            print('文件出错了T_T')
            print('出错原因是%s' % str(reason))
        return json.dumps({'err': str(reason),'resCode':5000})



if __name__ =='__main__':
    # app.run(debug=True)
    # host = '0.0.0.0', port = 9001 设置网络主机、端口号，不然flask框架默认为 127.0.0.1:5000
    app.run(host = '0.0.0.0', port = 9001, debug = True)