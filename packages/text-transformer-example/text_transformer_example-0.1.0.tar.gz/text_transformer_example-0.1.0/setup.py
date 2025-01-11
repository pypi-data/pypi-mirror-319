# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='text_transformer_example',  # 请根据需要修改包名
    version='0.1.0',                  # 初始版本
    author='YourName',                # 修改为你的姓名
    author_email='your.email@example.com',
    description='A simple text transformer package',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/text_transformer_example/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # 如果有第三方依赖包，在此处添加
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
