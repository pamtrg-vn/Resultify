from setuptools import setup, find_packages

setup(
    name='resultify',
    version='0.1.0',
    description='A Python library to implement the Result Pattern for robust error management',
    author='Phạm Văn Trường',
    author_email='devpham@hotmail.com',
    url='https://github.com/pamtrg-vn/resultify',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pytest',
    ],
)
