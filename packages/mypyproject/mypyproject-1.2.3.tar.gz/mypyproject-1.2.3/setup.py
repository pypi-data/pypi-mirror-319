# a simple setup file

from setuptools import find_packages, setup
# print(find_packages(include=['tools']))
setup(
    name="learn_pyproject",
    version="0.0.0",
    packages=find_packages(include=['tools']),
)
# print(find_packages(include=['tools']))
