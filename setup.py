import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    fh.close()

setuptools.setup(
    name='bilibili_api',
    version='2.0.0',
    url='https://github.com/Passkou/bilibili_api',
    license='MIT License',
    author='Passkou',
    author_email='psk116@outlook.com',
    description='哔哩哔哩的API调用模块',
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
        "websockets"
    ],
    package_data={
        'bilibili_api.src': [
            "api.json"
        ]
    }
)
