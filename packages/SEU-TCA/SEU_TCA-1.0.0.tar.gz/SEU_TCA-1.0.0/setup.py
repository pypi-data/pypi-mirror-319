from setuptools import setup, find_packages

setup(
    name='SEU_TCA',
    version='1.0.0',
    description='A framework for integrating spatial and single-cell transcriptomics data using Transfer Component Analysis.',
    author='LinluoLab',
    author_email='230218444@seu.edu.cn',
    url='https://github.com/LinluoLab/SEU-TCA',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'scanpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)