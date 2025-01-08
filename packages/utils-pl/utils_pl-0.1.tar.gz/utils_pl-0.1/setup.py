from setuptools import setup, find_packages

description = "A set of utilities written in python for various tasks. "
try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = description

setup(
    name="utils-pl",
    version="0.1",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "rich",
    ],
    description=description,
    long_description=long_description,
)
