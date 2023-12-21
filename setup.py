import os

import setuptools

import bilibili_api

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = f.read()

cfg = [bilibili_api.BILIBILI_API_VERSION, "main"]
if os.path.exists("github.txt"):
    with open("github.txt", "r", encoding="utf-8") as f:
        cfg = f.read().split("|")

setuptools.setup(
    name="bilibili-api-python" if "dev" not in cfg[1] else "bilibili-api-dev",
    version=cfg[0],
    license="GPLv3+",
    author="Nemo2011",
    author_email="yimoxia@outlook.com",
    maintainer="MoyuScript, Nemo2011",
    description="The fork of module bilibili-api. 哔哩哔哩的各种 API 调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "bilibili_api",
        "bilibili_api.utils",
        "bilibili_api.exceptions",
        "bilibili_api.errors",
        "bilibili_api.tools",
        "bilibili_api.tools.opendocs",
        "bilibili_api.tools.ivitools",
        "bilibili_api.tools.parser",
        "bilibili_api._pyinstaller",
    ],
    keywords=["bilibili", "api", "spider"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_data={
        "": [
            "data/**/*.*",
            "py.typed",
            "requirements.txt",
            "data/*.*",
            "data/article/*.*",
            "data/geetest/*.*",
            "data/corerespond/*.*",
        ]
    },
    install_requires=requires.splitlines(),
    url="https://github.com/nemo2011/bilibili-api",
    python_requires=">=3.8",
    entry_points={
        "pyinstaller40": [
            "hook-dirs = bilibili_api._pyinstaller.entry_points:get_hook_dirs"
        ],
        "console_scripts": [
            "bilibili-api-docs = bilibili_api.tools.opendocs.__main__:main",
            "ivitools = bilibili_api.tools.ivitools.__main__:main",
        ],
    },
)
