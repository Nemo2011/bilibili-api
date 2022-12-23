import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf8") as f:
    requires = f.read()

setuptools.setup(
    name="mplayer",
    version="1.0.0",
    license="GPLv3+",
    author="Nemo2011,Passkou",
    description="A Bilibili Interactive Video Player",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "mplayer"
    ],
    keywords=["bilibili"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_data={
        "": ["bin/ffmpeg/windows/all/*.*", 
             "bin/ffmpeg/macos/all/*.*", 
             "bin/ffmpeg/linux/x64/*.*", 
             "bin/ffmpeg/linux/arm64/*.*"]
    },
    install_requires=requires.splitlines(),
    url="https://github.com/Nemo2011/bilibili-api/tree/dev/MPlayer",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["mplayer = mplayer/__main__.py:main"],
    },
)
