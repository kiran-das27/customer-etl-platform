import os
from setuptools import setup, find_packages

build_number = os.getenv("BUILD_NUMBER", "0")

setup(
    name="customer_etl",
    version=f"1.0.{build_number}",
    packages=find_packages(),
)