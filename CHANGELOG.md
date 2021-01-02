# 更新日志

+ V3.1.7b1
    + 新增 bilibili_api.web_search, bilibili_api.web_search_by_type

+ V3.1.7b0 2021/01/02
    + 修复 channel.get_channel_info_by_tid()方法因channel.json中部分分区没有tid属性导致出错的BUG #97
    + 修复当视频弹幕关闭时程序陷入死循环的BUG #95

+ V3.1.6 2021/01/01
    + 修复获取动态列表报错的BUG

+ V3.1.5 2021/01/01
    + 更新 live.get_room_play_info
    + 关闭官网，感觉没必要放着，还浪费我服务器资源233333

+ V3.1.4 2020/12/23
    + 修复 live.connect_all_LiveDanmaku 只能连接一个房间的bug
    + 优化文档

+ V3.1.3 2020/11/20
    + 修复 live.LiveDanmaku 单房间调用 disconnect() 时报错问题

+ V3.1.2 2020/11/06
    + 修复安装时会在python目录下生成文件的bug
    + 增加获取子评论功能

+ V3.1.1 2020/11/01
    + 修复视频上传转码失败BUG

+ V3.1.0 2020/10/31
    + 更新 b站弹幕API
    + 增加 视频上传回调功能
    + 增加 视频弹幕点赞功能
    + 增加 查询视频弹幕是否点赞功能
    + 修正部分文档错误

+ V3.0.0 2020/10/22
    + live.LiveDanmaku现在可以自动重连了，详见文档
    + live.LiveDanmaku.has_connected()更改为get_connect_status，表示连接状态，0未连接，1已连接，2已正常断开，-1异常断开
    + 修改所有循环获取数据为**生成器**语法，方法名后面加了`_g`后缀便于识别
    + video模块新增视频上传功能，详见文档
    + 修复article.get_content()报错
    + 修正一些注释错误
    + 增加 video.VideoOnlineMonitor，可监控视频实时在线观看人数和实时更新弹幕，使用websocket
    + 优化 live.LiveDanmaku
    + 修改 live.connect_all_livedanmaku() 为 connect_all_LiveDanmaku()
    + 修改 live.LiveDanmaku.connect(return_task) 参数改为 return_coroutine，为True时返回一个 Coroutine 对象而不是 Task 对象
    + github自动化推送到PyPi
    + 修正changelog部分错误
    + 经检测支持Python3.9，修改README

+ V2.1.4 2020/10/06
    + 将项目主页纳入repo管理

+ V2.1.3 2020/10/04
    + user.get_videos() 增加查询条件，详见文档
    + user.get_up_info() 强制传入Verify，需要有SESSDATA（如果没有会获取不到信息）

+ V2.1.2 2020/09/26
    + 新增live.get_room_play_url（获取直播流地址）

+ V2.1.1 2020/09/13
    + 新增几个操作和获取用户关注分组的方法，详见开发文档 模块/user

+ V2.1.0 2020/09/10
    + 修复utils.request中cookies默认值初始化类型是tuple而不是dict的问题（低层级方法，不影响用户使用）
    + 优化LiveDanmaku异步调用，文档同步更新
    + LiveDanmaku现在可以同时连接多个直播间，参见开发文档 模块/live
    + **LiveDanmaku回调数据结构修改，不向下兼容，请注意**

+ V2.0.5 2020/08/31
    + 修复直播LiveDanmaku使用Verify被服务器拒绝, 优化异步
    + 优化 video.get_download_url

+ V2.0.4 2020/08/30
    + 修复utils.request若未传入params则报错的问题

+ V2.0.3 2020/08/28
    + 修复获取大航海列表少三个的问题

+ V2.0.2 2020/08/18
    + 新增接口：bangumi.get_collective_info，获取番剧全面概括信息,包括发布时间、剧集情况、stat等情况
    + 修复不能正确安装模块依赖库的bug

+ V2.0.1 2020/08/16
    + 增加开发文档
    + 增加获取用户投稿和订阅数据概览接口 user.get_overview
    + 修正注释错误
    + 新增接口：bangumi.get_episode_info，获取番剧剧集信息
    
+ V2.0.0 2020/08/12
    + 改写整体架构，使API调用更简单
    + 需要循环获取的内容（评论，转发等）低层级API分离，可根据需要调用获取总数量
    + 循环获取的函数增加回调机制（callback），每次获取一页会自动将该页内容作为参数调用回调函数（比如可以一边获取一边写入文件）
    + 源代码增加详细的注释说明
    + 增加了一堆新模块
    + **注意，开源协议从MIT更改到GPLv3**
    + 改的东西太多了懒的说明了...具体去看开发文档吧（逃

# 以下是v1版本

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