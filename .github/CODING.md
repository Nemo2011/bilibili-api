**欢迎来到代码贡献指南！！！**

本指南是专门为新的贡献者编写的。当然，如果你能力足够强大，仅需翻阅部分代码就可以领悟如何编写了。

本指南所讲的写法并不是唯一的写法，如果你有更好的写法，请不要害怕，大胆地写出来！本指南也只能作为一个开发的参考。最后，**这里不会提及除了写代码以外的任何事情**，所以你在这里是找不到 `git` 是如何使用的。

那，我们就开始吧！！！

**入门示例：我要贡献一个 API !**

首先你需要写入你的 API，找到 `bilibili_api/data/api` 目录，会有许多的 `json` 文件，你需要找到对应的 `json` 文件介入你的 API。举个例子：你的 API 如果和用户有关，请写入 `user.json` 文件中。<br>
每一个 `json` 文件会根据 API 的作用大致分类，你只要找到对应的分类就可以了。一般 `json` 文件将分为两个分类：`info` (有关获取信息的 API) 和 `operate` (有关操作用户相关信息的 API)。当然有的时候部分 API 也会被归类到另外一个分类，如 `video.json` 中有一个分类就存放着有关弹幕的 API (`danmaku`)。除非有大量与某个东西相关的 API (如视频 API 有许多是和弹幕有关的)，否则千万不要创建在 `info` 和 `operate` 以外的新的分类。<br>
~~当然有的文件因为懒什么分类都没有弄，在 API 非常少的时候你可以这么做，但是不推荐。~~<br><br>
然后你就可以进行编写了。首先找到对应的文件 (如和视频相关的 API 的具体实现要写在 `video.py` 中)，然后 (在一个类里面 ( 有的时候不用写在一个类里面 )) 新建一个异步函数，一定要记得完善参数类型和返回值类型。( 建议让你的 IDE 打开检查 `typing` 的模式，就例如 `Visual Studio Code` 里面将 `python.analysis.typeCheckingMode` 设置为 `basic` 或 `strict`)。接着你需要编写注释，像下面那样子编写：

``` python
async def get_user_real_name(self, uid: int, credential: Union[Credential, None] = None) -> dict:
    """
    你的函数的用途。

    Args:
        uid        (int)                        : 你的参数的说明。
        credential (Credential | None, optional): 凭据类。

    Returns:
        dict: 调用 API 返回的结果
    """
```

首先你要写上函数的用途，然后要写好参数的说明：名称 + 类型 + 用途。其中类型如果是多个的话，那么可以用 `|` 分隔而不是用 `Union` (写代码的时候务必要用 `Union`，需要支持 `Python3.8`)，如果你的 API 需要登录的话，你要加上 `credential` 参数，类型是 `Credential | None`，描述可以用 `凭据类。`。(凭据类能传入 cookies 以保证能正常访问需要登录的 API，这里就做到了登录的作用 ) 最后要把返回值写好，一般情况下 API 返回的结果类型都是 `dict`，这个时候你的返回值说明就可以用 `调用 API 返回的结果`。<br>
然后就是函数的主体了，你可以按照下面的写法来写：

``` python
async def ...(...) -> dict:
    """
    ...
    """
    credential = credential if credential else Credential()
    api = API["info"]["realname"]
    params = {
        ...
    }
    return await request("GET", api["url"], params=params, credential=credential)
```

首先如果函数要传入凭据类，那么你要添加 `credential = credential if credential else Credential()` 以确保 `credential` 参数不会是 `None` 类型，~~当然不这么做也不会报错，但是你好歹要走个形式啊！~~。接着我们声明 `api` 变量，它是字典 `API` 的一部分，这里的字典 `API` 就是你写入 API 的那个 `json` 文件的内容。所以你的 API 也在里面，你只需要补充好字典的键值就可以了。接着就是可选的 `params` 或 `data`，如果你的 API 需要传入参数的话不要忘记创建它们。最后你只需要返回已经封装好了的函数 `request` 得到的结果就可以了。`request` 函数的第一个参数是访问 `API` 的方法，一般是 `GET`/`POST`/`PUT`/`DELETE`/`PATCH`，第二个参数是 `API` 的链接，你只需要填入 `api["url"]` 就可以了 ( 前提是你的键值没有输错 )，下面的参数最好要指定名称传参，最后不要忘记了：如果这个接口需要登录，那么你得要把凭据类传入进去！( 如果你的函数是在一个类里面，通常每一个类都有一个属性 `credential`，就是创建这个类的时候会传入的，这个时候你只需要传入 `self.credential` 就可以了。当然参数里面不用再写 `credential` 参数了！！ )<br><br>
恭喜你完成了代码的编写！你可以先进行一次新功能的提交：

``` bash
$ git commit -am "feat(user.User): 新增一个狗都不用的接口"
```

然后你还需要干两件事情：文档 & 测试。这里不详细说明了，因为这里不会提及除了写代码以外的任何事情。SO...

**恭喜你已经成功踏出了第一步！**

当然，除了这个指南举的简单 API 样例，你还可以学习更加高级的功能，例如新建一个模块、事件监听器、`protobuf` 数据等等，这里~~因为懒~~先不写了，你可以查看这些功能的样例进行学习。

所以做完功能不要忘记提交到线上仓库！ (**PR 记得向 `dev` 分之提交！！！**)

<details>
<summary>看不见我</summary>

``` bash
$ git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;git push origin dev;
```

</details>
