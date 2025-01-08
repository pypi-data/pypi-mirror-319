from setuptools import setup, find_packages
import pathlib

VERSION = '0.0.2'
DESCRIPTION = 'My first Python package'

setup(
    name="book_package_svk",
    version=VERSION,
    description=DESCRIPTION,
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['python', 'book package svk'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
