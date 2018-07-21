# python 读取文件并返回给前端

> 常规的python web开发是在服务器端根据url动态生成`html`<br>
> 这里还是采取前后端分离思想，通过python读取文件数据，通过接口给前端调用。<br>

`注意事项`<br>
- 确保python版本为3.x

---

*框架选型：*

- Django：全能型Web框架；

- Flask：轻量实用的Web框架；

- web.py：一个小巧的Web框架；

- Bottle：和Flask类似的Web框架；

- Tornado：Facebook的开源异步Web框架。

*只是实现一个小工具实用Flask就好*


*安装方式*<br>
```
pip install flask
```

## 初衷和思路
博客的文章管理方式大体分两种：静态html、动态加载。动态加载文章一般通过数据库存取，为了简化此过程，就想通过直接加载文件的方式。
markdown语法在写文章上很受开发者青睐，因此直接加载md文件就比较便于维护。
现行方案中
github采用的后端加载方式，已有的一种前端直接加载md文件的方式是[vue-markdown-loader](https://github.com/QingWei-Li/vue-markdown-loader)
对此方式感兴趣可以直接采用这种loader方式，以下内容就可以忽略了。
之所以采取python读取文档并返回给前端而不是其他语言主要是因为python比较火热，应用面广。作为一枚小前端果断选择python来研究学习，这个小项目也是用来练练手。
<br>
注：md文章放在项目`./static`下就好
* 1.注册接口，绑定处理函数
* 2.接收前端传递的参数（文件名）
* 3.读取文件，返回到前端

## 代码如下：
python代码就是简洁
```python
@app.route('/getdata/md', methods=['post'])
def ajax_test_add():
    params = request.get_json()
    childPath = params.get('title')
    if(params.get('title') == None):
        print('未传title字段！')
        return json.dumps({'resCode':'4001','msg':'参数错误title为必传'})
    else:
        path = './static' + childPath + '.md'
        try:
            f_name = open(path, 'r', encoding='UTF-8').read()
            print(f_name)
            # 成功获取到md文件内容啦
            return json.dumps({'content':f_name,'resCode':2000})
        except OSError as reason:
            print('读取文件出错了T_T')
            print('出错原因是%s' % str(reason))
        return json.dumps({'err': str(reason),'resCode':5000})
```

`问题总结`
- 跨域问题<br>
`from flask_cors import CORS`<br>
`CORS(app, resources=r'/*')`<br>
r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求

- 主机端口号设置<br>
`app.run(host = '0.0.0.0', port = 9001, debug = True)`

# 前端代码
```html
<article class="post post-1" repeat="blogData.data">
    <header class="entry-header">
        <h1 class="entry-title">
            <a href="javascript:;" data-id="{{item.key}}" onclick="showArticle(this)" >{{item.title}}</a>
        </h1>
        <div class="entry-meta">
            <span class="post-category"><a href="#">{{item.category}}</a></span>
            <span class="post-date"><a href="#">
                <time class="entry-date">{{item.updateAt}}</time>
            </a></span>
            <span class="post-author"><a href="#">{{item.author}}</a></span>
            <span class="comments-link"><a href="#">{{item.segs}} 评论</a></span>
            <span class="views-count"><a href="#">{{item.count}} 阅读</a></span>
        </div>
    </header>
    <div class="entry-content clearfix">
        <p>{{item.content}}</p>
        <div class="read-more cl-effect-14">
            <a href="#" class="more-link">继续阅读<span class="meta-nav">→</span></a>
        </div>
    </div>
</article>
```

在点击文章标题是，获取data-id属性的值，该值即为传给后端的文件名。<br>
前端调用的接口地址：`http://hostname:9001/getdata/md`
请求方式：POST<br>
必传参数：{"title": 文章名(不用加后缀)},该文章要放在python项目的`./static`目录下<br>

[完整代码链接](https://github.com/MOBUED/docs/blob/master/example/getdata.py)

>献丑了，小弟初学python，还忘各位大佬多多指教！






