from setuptools import setup, find_packages

setup(
    name="himile-log",             # 包名
    version="0.1.0",                 # 版本号
    author="Zongwei Du",            # 作者
    author_email="pxwtp6519@gmail.com",  # 作者邮箱
    description="the log Create By Yi Sun",  # 包的描述
    long_description=open('README.md', encoding='utf-8').read(),  # 从README.md中读取详细描述
    long_description_content_type="text/markdown",  # 指定README的格式
    # url="https://github.com/yourname/my_package",  # 包的URL地址
    py_modules=["himile_log"],      # 自动发现所有子包
    classifiers=[                  # PyPi上的分类
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[             # 依赖的第三方库
        "loguru",
    ],
    python_requires='>=3.6',        # 支持的Python版本
)