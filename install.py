import os
import shutil

print("初始化开发环境中...")

current_file_dir = os.path.dirname(__file__)

# 安装 pylint
os.system("pip3 install pylint")

# 初始化 Githooks
print("初始化 GitHooks 中...")
git_hooks_dir = os.path.join(current_file_dir, ".git/hooks")

hooks_path = map(
    lambda x: os.path.join(current_file_dir, ".githooks", x),
    os.listdir(os.path.join(current_file_dir, ".githooks")),
)

for hook in hooks_path:
    print(f"复制 {hook} 到 {git_hooks_dir}")
    shutil.copy(hook, git_hooks_dir)

print("初始化开发环境完成")
