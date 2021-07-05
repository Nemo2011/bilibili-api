import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("bilibili_api/requirements.txt", "r", encoding="utf8") as f:
    requires = f.read()

setuptools.setup(
    name='bilibili-api',
    version='6.0.0',
    license='GPLv3+',
    author='Passkou',
    description='哔哩哔哩的各种API调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    keywords=[
        "bilibili",
        "api",
        "spider"
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    package_data={
        "": [
            "data/**/*.*",
            "requirements.txt",
            "data/*.*"
        ]
    },
    install_requires=requires.splitlines(),
    url="https://github.com/Passkou/bilibili-api",
    python_requires=">=3.8"
)
