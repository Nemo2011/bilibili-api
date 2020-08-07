# 更新日志
+ **V2.0.0**
    + 改写整体架构，使API调用更简单
    + 需要循环获取的内容（评论，转发等）低层级API分离，可根据需要调用获取总数量
    + 循环获取的函数增加回调机制（callback），每次获取一页会自动将该页内容作为参数调用回调函数（比如可以一边获取一边写入文件）
    + 源代码增加详细的注释说明
    + 增加了一堆新模块
    + 改的东西太多了懒的说明了...具体去看开发文档吧（逃
    
+ V1.4.0 2020/06/22
    + 添加了番剧相关的3个API
    + 修正了aid2bvid会报错的bug
    
+ V1.3.5 2020/06/01
    + 修复获取动态评论时会少获取一页的BUG
    + 将bvid和aid互转的方法加入了video模块（bvid2aid(bvid), aid2bvid(aid)）
    + **儿童节快乐**
    
+ V1.3.4 2020/05/22
    + 修复获取用户动态有时候报错的bug
    + 修复获取用户视频较少时报错的bug
    
+ V1.3.3 2020/04/07
    + 修复不能收藏的问题（b站的收藏API还在使用aid，服了）
    + 从知乎大佬那嫖了bvid和aid互相转换的代码过来（滑稽）[原出处](https://www.zhihu.com/question/381784377/answer/1099438784)
    
+ V1.3.2 2020/03/24
    + 修复get_playurl()返回值不是Python对象的bug，并对bvid做了支持
    + 把全部抛出异常改为了bilibiliApiException

+ V1.3.1 2020/03/23
    + 修复无法获取仅限注册会员观看的视频地址

+ V1.3.0 2020/03/23
    + 重大更新，b站正在把视频标识从av逐渐改为bv，本模块已进行更新video模块中的各类可传入bvid参数
    + 修复无法获取弹幕的bug
    + 将verify用于视频信息获取验证，用于获取部分只有注册会员才能看的视频的信息
    
+ V1.2.5 2020/03/20
    + 修复User模块中UserInfo的get_video()出错的bug
    
+ V1.2.4 2020/03/17
    + VideoInfo中少写一对括号导致返回值不正确，修了修了QAQ

+ V1.2.2 2020/02/28
    + 部分获取内容补上limit参数
    + 修正不能发送动态的BUG
  
+ V1.2.1 2020/01/31
    + 部分获取内容补上limit参数
    + 部分类的方法更改了参数名字和类型
    + OperateDynamic 类新增 repost 方法（转发）
    
+ V1.2.0 2020/01/31
    + 重写验证方式，新增 [Verify](https://github.com/Passkou/bilibili_api/wiki/Verify%E7%B1%BB) 类（写法稍微变了一下，具体看教程）
    + 减少 `video` 模块冗余请求代码，集合到了一个类中（减少了150行左右）
    + 新增 `user` 模块（[Wiki](https://github.com/Passkou/bilibili_api/wiki)）
    + 新增 `dynamic` 模块（[Wiki](https://github.com/Passkou/bilibili_api/wiki)）
    + [VideoInfo.get_comments()](https://github.com/Passkou/bilibili_api/wiki/VideoInfo%E7%B1%BB#get_comments) 新增limit参数，可限制获取的数量
    + 改写 `__init__` ，使导入结构更清楚（免得显示其他你们用不上的东西太乱）
    + 所有模块传参强制变量类型
    + 修改 [VideoInfo.get_playurl()](https://github.com/Passkou/bilibili_api/wiki/VideoInfo%E7%B1%BB#get_playurl) 用正则表达式获取链接信息，
      用不着为了这个去多装一个依赖库
    + 加了一个小彩蛋(=・ω・=)
  
+ V1.1.1 2020/01/28
    + 补上了漏掉的sessdata值判断
    + [Danmaku](https://github.com/Passkou/bilibili_api/wiki/Danmaku%E7%B1%BB) 类的映射表改为私有

+ V1.1.0 2020/01/27
    + 修正一些BUG（语法错误太丢人了）
    + [VideoInfo.get_playurl()](https://github.com/Passkou/bilibili_api/wiki/VideoInfo%E7%B1%BB#get_playurl) 重写，现在能获得高清的下载链接了
    + 一天三次更新我哭了QAQ

+ V1.0.1 2020/01/27
    + 修正README文档错误

+ V1.0.0 2020/01/27
    + 发布第一版本，只能操作用户上传视频，后续会慢慢更新其他功能233。