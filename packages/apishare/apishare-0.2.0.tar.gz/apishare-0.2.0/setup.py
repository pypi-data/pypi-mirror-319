from setuptools import setup, find_packages
import re
import ast


def get_version():
    """Get version from __init__.py"""
    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    with open('apishare/__init__.py', 'rb') as f:
        version = str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))
    return version

setup(
    name="apishare",
    version=get_version(),
    author="chengangqiang",
    author_email="chengq@niututu.com",
    description="A Python package for financial market data access",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.apishare.cn",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.28.1",
        "pandas>=2.2.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
