## 前端性能优化之Lazyload

@(Mob前端)[JavaScript|技术分享|懒加载]

-------------------

[TOC]

### Lazyload 简介

> 前端工作中，界面和效果正在变得越来越狂拽炫酷，与此同时性能也是不得不提的问题。有些项目，页面长，图片多，内容丰富。像商城页面。如果同步加载时一次性加载完毕，那肯定是要等到花都谢了，loading转的人都崩溃~。今天分享的是Lazyload技术 是一种延迟加载技术。让页面加载速度快到飞起、减轻服务器压力、节约流量、提升用户体验。
 
### 一、实现思路
页面较长，屏幕的可视区域有限。
不设置页面中`img标签`的`src属性`值或者将其指向同一个占位图。
图片的实际地址存在`img标签`自定义的一个属性中，如：“data-url”。
监听`scroll`，滚动到某个位置时，动态的将url替换成实际的“data-url”。

### 二、上代码

- **html部分(简单示意下结构)**
``` html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Lazyload</title>
    <style type="text/css">
      .mob-wrap li{list-style: none;width: 100%;height: 345px;}
    </style>
  </head>
  <body>
    <ul class="mob-wrap">
      <li">
        <img class="tamp-img" alt="loading" data-src="http://mob.com/public/images/index/sharesdk-logo.jpg"><p>ShareSDK轻松实现社会化功能</p>
      </li>
      <li">
        <img class="tamp-img" alt="loading" data-src="http://mob.com/public/images/index/sms-logo.jpg"><p>短信验证码SDK</p>
      </li>
      <li">
        <img class="tamp-img" alt="loading" data-src="http://mob.com/public/images/index/rec-logo.jpg"><p>MobLink实现Web与App的无缝链接</p>
      </li>
    </ul>
  </body>
</html>
```
**简要流程**
```flow
st=>start: Start
e=>end
op=>operation: 监听滚动事件
cond=>condition: 距顶部高度<scrollTop么？
io=>inputoutput: 将url替换成data-url
st->op->cond
cond(yes)->io->e
cond(no)->op
```
- **js部分**
``` javascript
var aImg = [
  {"src":"http://mob.com/public/images/index/sharesdk-logo.jpg","txt":"ShareSDK轻松实现社会化功能"},
  {"src":"http://mob.com/public/images/index/sms-logo.jpg","txt":"短信验证码SDK"},
  {"src":"http://mob.com/public/images/index/rec-logo.jpg","txt":"MobLink实现Web与App的无缝链接"}
];
var sLi = '';
document.getElementsByClassName("mob-wrap")[0].innerHTML="";
for(let i = 0;i<10;i++){
  sLi = document.createElement("li");
  sLi.innerHTML = `<img class="tamp-img" alt="loading" src="./zwt.gif" data-src="${aImg[i%3].src}"><p>${aImg[i%3].txt}</p>`;
  document.getElementsByClassName("mob-wrap")[0].appendChild(sLi);
};

window.onscroll = function () {
  var bodyScrollHeight =  document.documentElement.scrollTop;// body滚动高度
  var windowHeight = window.innerHeight;// 视窗高度
  var imgs = document.getElementsByClassName('tamp-img');
  for (var i =0; i < imgs.length; i++) {
    var imgHeight = imgs[i].offsetTop;// 图片距离顶部高度 
    if (imgHeight  < windowHeight  + bodyScrollHeight - 340) {
       imgs[i].src = imgs[i].getAttribute('data-src');
       imgs[i].className = imgs[i].className.replace('tamp-img','');
    }
  }
};
```
.
.
.
 谢谢观看，搞定收工0.0~~~这样草草了事总是不好的

### 三、再优化
不做任何处理直接监听scroll必然导致在滚动鼠标滚轮的时候，过于频繁的触发处理函数。
如果刚巧在处理函数中有大量的操作dom等消耗性能的行为，引发大量操作，导致页面变卡变慢，
甚至浏览器崩溃无响应。
处理这种问题的思路是节流和防抖。
节流函数的概念有一个很形象的比喻：在接咖啡的时候，按了一次按钮会出咖啡，
紧跟着再按几次按钮接到的还是那一杯咖啡，相当于后面几次按的没有起作用。

<br>
常规的节流在这里就不多说了，下面介绍的是一种每隔`least`时间内至少执行一次的节流函数。

``` javascript
//节流函数
_throttle = (fn, delay, least) => {
    var timeout = null,
  startTime = new Date();
    fn();
    return function() {
    var curTime = new Date();
    clearTimeout(timeout);
    if(curTime - startTime >= least) {
        fn();
        startTime = curTime;
    }else {
        timeout = setTimeout(fn, delay);
    }
    }
}
```

**使用节流函数**
``` javascript
function compare () {
  var bodyScrollHeight =  document.documentElement.scrollTop;// body滚动高度
  console.log(bodyScrollHeight+"替换src方法")
  var windowHeight = window.innerHeight;// 视窗高度
  var imgs = document.getElementsByClassName('tamp-img');
  for (var i =0; i < imgs.length; i++) {
    var imgHeight = imgs[i].offsetTop;// 图片距离顶部高度 
    if (imgHeight < windowHeight + bodyScrollHeight - 340) {
       imgs[i].src = imgs[i].getAttribute('data-src');
       imgs[i].className = imgs[i].className.replace('tamp-img','');
    }
  }
}
window.onscroll = _throttle(compare, 350,600);
```
滚动时间`least`长于600，调用compare，否则延迟350ms执行。
这样相对于直接onscroll性能得到更进一步提升，在功能上也没有什么问题。
不同的业务场景调整一下delay和least就可以。

<br>
>  **结语：**历史潮流浩浩荡荡，前端技术的发展也是日新月异。
>  不断通过一个个小的技术点深入探究，以加深自己对js这门语言的理解。
>  温故知新，回顾旧的内容，学习新的内容和特性，更好的适应工作中的需求。