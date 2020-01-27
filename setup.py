import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    fh.close()

setuptools.setup(
    name='bilibili_api',
    version='1.0.0',
    url='https://github.com/Passkou/bilibili_api',
    license='MIT License',
    author='Passkou',
    author_email='psk116@outlook.com',
    description='哔哩哔哩的API调用模块',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.8"
    ],
    install_requires=[
        "requests"
    ],
    package_data={
        'bilibili_api':[
            "api.json"
        ]
    }
)
