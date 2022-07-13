**欢迎对代码进行贡献！ヾ(ﾟ∀ﾟゞ)**

请在发起 PR 前仔细阅读本贡献指南，否则你的 PR 可能不会被合并。

**请务必转到 github 上 PR，gitee 仓库只是一个官方的镜像，设置为强制同步 github 仓库。**

# 开发流程

1. 使用 `git clone git@github.com:Nemo2011/bilibili_api.git` 将本仓库拉取到本地。
2. 使用 `cd bilibili-api` 切换到仓库位置。
3. 使用 `pip3 install -r requirements.txt` 安装相关依赖。
4. **使用 `python install.py` 进行初始化**，该项非常重要，将会初始化 Git Hooks。
5. 使用 `git checkout dev && git checkout -b {分支名}` 从 dev 分支切换到一个新的分支再进行编码。
6. 开发完毕后，使用 `git push -u origin {分支名}` 将分支推送到你 fork 的仓库。
7. **向 `dev` 分支**发起 [Pull Requests](https://github.com/Nemo2011/bilibili_api/pulls)。

# 代码风格、格式规范

代码风格遵循 [Google Python Style](https://google.github.io/styleguide/pyguide.html)（[中文版](https://google-styleguide.readthedocs.io/zh_CN/latest/google-python-styleguide/contents.html)）

代码格式请遵循 [PEP8]，可以用自动格式化工具(如 `black`)

请务必严格遵循该规范，特别是命名、空格的正确使用。在提交前，会自动运行代码检查工具，检查代码中存在的明显问题。

另外就是，文档中的英文和中文混用时，英文与中文之间需要使用半角空格隔开，例如：

```
# Wrong

Python是世界上最好的语言。

# OK

Python 是世界上最好的语言
```

# 提交规范

## 提交描述

本项目采用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 规范，请严格遵守。

在提交前会自动检测是否符合该规范，如果不符合将会拒绝提交，**请勿强行提交**。

## 提交内容

建议尽量将一个大提交拆分为几个小提交，比如如果同时修复了一个 bug 和增加了一个新功能，应该拆开为两次提交。

如果你有破坏性修改（修改方法名、增加方法必需参数等），请在提交信息中的尾注部分写上 `BREAKING CHANGE: 说明`。例如：

```
fix: 给 method() 增加了一个必需参数

可选的其他描述...

BREAKING CHANGE: 给 method() 增加了一个必需参数
```

或者是在第一行冒号前加一个英文感叹号也行：

```
fix!: 给 method() 增加了一个必需参数

可选的其他描述...
```

非必要尽量不要有破坏性修改，比如如果只是新增一个参数，可以考虑一下这个参数是不是能设置个默认值。


# 开发规范

1. 如果你增加了一个新功能，请在对应位置补充文档（docs/）。
2. 尽量复用现有代码。

# 附录

附 1：Git 使用参考

[Pro Git](https://progit.cn/)

