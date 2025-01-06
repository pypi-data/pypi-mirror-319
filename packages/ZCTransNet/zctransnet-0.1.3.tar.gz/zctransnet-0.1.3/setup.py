from setuptools import setup, find_packages
from pathlib import Path

# 获取当前目录
current_dir = Path(__file__).parent

# 将编译好的 .pyd 文件作为包的一部分
setup(
    name="ZCTransNet",  # 包的名称
    version="0.1.3",  # 包的版本
    description="A Python package with C++ extension for UE functionality",
    author="ZC",  # 作者信息
    author_email="1263703239@qq.com",  # 作者邮箱
    # url="https://github.com/your-repo",  # 可选：你的代码仓库链接
    packages=find_packages(),  # 自动查找所有含有 __init__.py 的包
    include_package_data=True,  # 确保非代码文件也被包含
    package_data={
        "ZCTransNet": ["*.pyd"],  # 指定 .pyd 文件所在的路径
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.11",  # 兼容的 Python 版本
)
