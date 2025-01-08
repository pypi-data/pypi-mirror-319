from setuptools import setup, find_packages


setup(
    name='pyatoms', 
    version='0.0.1', 
    description='Python automated tools for materials screening', 
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown', 
    author='Xiang Feng', 
    author_email='buaamsefengxiang@buaa.edu.cn', 
    packages=find_packages(), 
    python_requires=">=3.9", 
    install_requires=[
        'ase>=3.23.0', 
        'matplotlib>=3.9.4', 
        'numpy>=1.26.4', 
        'prettytable>=3.12.0', 
        'pymatgen==2024.3.1', 
        'scipy>=1.13.1', 
        'setuptools>=75.6.0', 
        'statsmodels>=0.14.4', 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
