
from setuptools import setup, find_packages

setup(
    name="sms_send_cjh",
    version="0.5",
    package_dir={"": "src"},  # 指定包的根目录在 src 下
    packages=find_packages(where="src"),
    long_description=open('README.md').read(),  # 读取 README 文件作为包描述
    long_description_content_type='text/markdown',
    include_package_data=True,  # 确保包含 MANIFEST.in 中的文件
    install_requires=[
        "aliyun-python-sdk-core",
        "aliyun-python-sdk-dysmsapi",
    ],
    description="发送短信包",
    author="CJH",
    author_email="942130598@qq.com",
    url="https://github.com/chongjiahao223/sms_sender.git",
    python_requires = ">=3.12",
)