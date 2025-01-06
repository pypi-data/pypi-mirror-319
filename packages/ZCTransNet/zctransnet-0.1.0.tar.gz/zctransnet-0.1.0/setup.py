from setuptools import setup
from setuptools import Extension
from pathlib import Path

# 获取当前目录
current_dir = Path(__file__).parent

# 将编译好的 .pyd 文件作为包的一部分
setup(
    name="ZCTransNet",  # 包的名称
    version="0.1.0",  # 包的版本
    description="A Python package with C++ extension for UE functionality",
    author="ZC",  # 作者信息
    author_email="1263703239@qq.com",  # 作者邮箱
    # url="https://github.com/your-repo",  # 你的代码仓库链接（可选）
    packages=[],  # 如果不需要额外的 Python 代码，保持为空
    package_data={
        "": ["UE.cp311-win_amd64.pyd"],  # 包含 .pyd 文件
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires="==3.11",  # 兼容的 Python 版本
)
