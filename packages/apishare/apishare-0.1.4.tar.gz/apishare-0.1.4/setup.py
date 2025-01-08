from setuptools import setup, find_packages
import re
import ast

from apishare.appinfo import APP_VERSION, APP_NAME

def get_version():
    """Get version from __init__.py"""
    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    with open('apishare/__init__.py', 'rb') as f:
        version = str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))
    return version

setup(
    name=APP_NAME,
    version=f"{APP_VERSION.major}.{APP_VERSION.minor}.{APP_VERSION.micro}",
    author="chengangqiang",
    author_email="chengq@niututu.com",
    description="A Python package for API sharing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/apishare",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.28.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
