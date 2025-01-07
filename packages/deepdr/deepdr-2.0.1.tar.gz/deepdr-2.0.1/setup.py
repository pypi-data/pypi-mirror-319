from setuptools import setup, find_packages

setup(
    name='deepdr',
    version='v2.0.1',
    description='A deep learning library for drug response prediction',
    packages=find_packages(),
    keywords=[
        'Drug response',
        'Deep learning',
        'Python library'
    ],
    install_requires=[
        'torch>=1.10.0',
        'torchvision>=0.11.0',
        'torchaudio>=0.10.0',
        'torch_geometric>=2.0.3',
        'torch_cluster>=1.5.9',
        'torch_scatter>=2.0.9',
        'torch_sparse>=0.6.12',
        'torch_spline_conv>=1.2.1',
        'rdkit',
        'wandb',
        'joblib',
        'openpyxl',
        'pubchempy'
    ],
    include_package_data=True,
    package_data={'': ['DefaultData/*']},
    author='Zhengxiang Jiang and Pengyong Li',
    author_email='jiangzx24@163.com',
    license='Apache 2.0'
)
