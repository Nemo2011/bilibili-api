import setuptools
import json

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("./bilibili_api/about.json", encoding="utf8") as f:
    about = json.loads(f.read())

setuptools.setup(
    name='bilibili_api',
    version=about["version"],
    license='GPLv3+',
    author='Passkou',
    author_email='psk116@outlook.com',
    description='哔哩哔哩的各种API调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=[
        "bilibili",
        "api",
        "spider"
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    install_requires=[
        "requests >= 2.24.0",
        "websockets >= 8.1",
        "beautifulsoup4 >= 4.9.1",
        "aiohttp >= 3.6.2",
        "cssutils >= 1.0.2"
    ],
    package_data={
        'bilibili_api': [
            "data/*.*",
            "tools/*.*",
            "about.json"
        ]
    },
    url="https://passkou.com/bilibili_api",
    project_urls={
        "Source": "https://github.com/Passkou/bilibili_api",
        "Homepage": "https://passkou.com/bilibili_api",
        "Documentation": "https://passkou.com/docs/bilibili_api"
    },
    python_requires=">=3.8"
)
