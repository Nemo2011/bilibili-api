import setuptools
import sys

if __name__ == '__main__':
    with open("./version.txt") as f:
        version = f.read()
    if 'sdist' in sys.argv:
        # 自动生成readme
        print("动态生成README.md")
        with open("README.template.md", 'r', encoding='utf8') as f:
            content = f.read()
            # 替换版本号
            content = content.replace('%version%', version)
            long_description = content
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)
    else:
        with open("README.md", "r", encoding="utf-8") as f:
            long_description = f.read()

    setuptools.setup(
        name='bilibili_api',
        version=version,
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
            "Programming Language :: Python :: 3.8"
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
                "tools/*.*"
            ]
        },
        url="https://passkou.com/bilibili_api",
        project_urls={
            "Source": "https://github.com/Passkou/bilibili_api",
            "Homepage": "https://passkou.com/bilibili_api",
            "Documentation": "https://passkou.com/docs/bilibili_api"
        },
        python_requires=">=3.8",
        data_files=[
            ("", ["./LICENSE.md", "./CHANGELOG.md", "./version.txt", "./README.template.md"])
        ]
    )
