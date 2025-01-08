import setuptools
import os
import shutil
from setuptools import Command

with open("README.md", "r") as fh:
    long_description = fh.read()


class CleanCommand(Command):
    """自定义清理命令，删除 dist/ 目录"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('yplib.egg-info'):
            shutil.rmtree('yplib.egg-info')


def get_version():
    return '7.0.1'


version = get_version()

setuptools.setup(
    name="yplib",
    version=version,
    author="yangpu",
    author_email="wantwaterfish@gmail.com",
    description="util",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        "openpyxl==3.1.2",
        "xlrd==2.0.1",
        "bs4==0.0.2",
        "requests==2.31.0",
        "PyMySQL==1.1.0",
        "pyarrow==16.0.0",
        "pandas==2.2.2"
    ],
    cmdclass={
        'clean': CleanCommand,  # 注册 clean 命令
    }
)
