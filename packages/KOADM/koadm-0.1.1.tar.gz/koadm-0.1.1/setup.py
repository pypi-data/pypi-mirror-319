# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='KOADM',
    version='0.1.1',
    packages=find_packages(),
    package_data={
        '': ['train_data.csv'],  # 包含当前目录下的 train_data.csv 文件
    },
    include_package_data=True,
    description='Knee osteoarthritis diagnosis model',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='QWB',
    license='MIT',
    install_requires=['pandas==2.1.4','numpy==1.26.4','scikit-learn==1.2.2',
                      'xgboost==2.1.3','lightgbm==4.5.0','keras==3.4.1','tensorflow==2.17.0'],
    entry_points={
        'console_scripts': [
            'KOADM=KOADM:KOA_diag',  
        ],},
)


