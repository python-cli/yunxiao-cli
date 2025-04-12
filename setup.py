from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yunxiao-cli",
    version="0.1.0",
    author="Wei Han",
    author_email="xingheng.hax@qq.com",
    description="A CLI tool for interacting with Alibaba Cloud Yunxiao",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/python-cli/yunxiao-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
    install_requires=[
        "alibabacloud-tea",
        "alibabacloud-tea-openapi",
        "aliyun-python-sdk-core",
        "aliyun-python-sdk-sts",
        "aliyunsdkcore",
        "click",
        "PyYAML",
        "requests",
        "rich",
        "selenium",
        "webdriver-manager",
    ],
    entry_points={
        "console_scripts": [
            "yunxiao-cli=yunxiao.main:cli",
        ],
    },
)
