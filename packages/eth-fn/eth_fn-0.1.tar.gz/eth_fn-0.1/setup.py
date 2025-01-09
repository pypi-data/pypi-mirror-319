#!/usr/bin/env python
from setuptools import (
    find_packages,
    setup,
)

extras_require = {}

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="eth_fn",
    version="0.1",
    description="""eth_fn: Simple Python utilities for web3py to call ETH contract without ABI""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="0xKJ",
    author_email="kernel1983@gmail.com",
    url="https://github.com/kernel1983/eth-fn",
    include_package_data=True,
    install_requires=[
        "eth-utils>=2.0.0",
        "eth-abi>=5.0.0",
    ],
    python_requires=">=3.8, <4",
    extras_require=extras_require,
    py_modules=["eth_fn"],
    license="MIT",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["scripts", "scripts.*", "tests", "tests.*"]),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
)