import setuptools
import os

with open(
    os.path.join(os.path.dirname(__file__), "requirements.txt"), 
    "r", 
    encoding="utf8"
) as f:
    requires = f.read()

setuptools.setup(
    name = "ivitools", 
    version = "2.33", 
    license = "GPLv3+", 
    author = "Nemo2011", 
    packages = [
        "ivitools", 
        "ivitools.ffmpeg"
    ], 
    keywords = ["bilibili"], 
    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ], 
    package_data = {
        "": ["ffmpeg/*.*", "ffmpeg/*"]
    }, 
    install_requires = requires.splitlines(), 
    python_requires = ">=3.8", 
    entry_points = {
        "console_scripts": [
            "ivitools = ivitools.__main__:main", 
        ], 
    }
)
