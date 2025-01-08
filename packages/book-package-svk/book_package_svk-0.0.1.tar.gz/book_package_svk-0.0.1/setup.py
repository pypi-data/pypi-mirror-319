from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package for managing book information with a slightly longer description'

setup(
    name="book_package_svk",
    version=VERSION,
    description=LONG_DESCRIPTION,
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
