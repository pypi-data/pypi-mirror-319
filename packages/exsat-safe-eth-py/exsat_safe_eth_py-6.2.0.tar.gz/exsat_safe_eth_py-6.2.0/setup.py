from setuptools import setup, find_packages

setup(
    name="exsat-safe-eth-py",  
    version="6.2.0",  
    author="",  
    author_email="Uxío <uxio@safe.global>",  
    description="Safe Ecosystem Foundation utilities for Ethereum projects",  
    long_description=open("README.rst").read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/exsat-network/safe-eth-py",  
    packages=find_packages(where="/safe_eth"),  
    python_requires=">=3.6",  
)
