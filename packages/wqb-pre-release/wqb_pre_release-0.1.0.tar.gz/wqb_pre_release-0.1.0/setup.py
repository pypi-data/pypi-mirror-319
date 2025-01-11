from setuptools import setup, find_packages

setup(
    name='wqb-pre-release',
    version='0.1.0',
    author='Rocky Haotian Du',
    author_email='qq2712479005@gmail.com',
    description='wqb-pre-release',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',
    ],
    python_requires='>=3.11',
)
