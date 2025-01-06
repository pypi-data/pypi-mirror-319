
from setuptools import setup, find_packages

setup(
    name="sms_send_cjh",
    version="0.1",
    packages=find_packages(),
    long_description=open('README.md').read(),  # 读取 README 文件作为包描述
    long_description_content_type='text/markdown',
    install_requires=[
        "aliyun-python-sdk-core",
        "aliyun-python-sdk-dysmsapi",
    ],
    description="发送短信包",
    author="CJH",
    author_email="942130598@qq.com",
    url="https://github.com/chongjiahao223/sms_sender.git"
)