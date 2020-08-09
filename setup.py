import setuptools
import bilibili_api

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    fh.close()

setuptools.setup(
    name='bilibili_api',
    version=bilibili_api.META_VERSION,
    url='https://github.com/Passkou/bilibili_api',
    license='MIT License',
    author='Passkou',
    author_email='psk116@outlook.com',
    description='哔哩哔哩的各种API调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=[
        "bilibili",
        "api"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.8"
    ],
    install_requires=[
        "requests",
        "websockets",
        "beautifulsoup4",
        "aiohttp",
        "cssutils"
    ],
    package_data={
        'bilibili_api': [
            "data/*.*",
            "tools/*.*"
        ]
    }
)
