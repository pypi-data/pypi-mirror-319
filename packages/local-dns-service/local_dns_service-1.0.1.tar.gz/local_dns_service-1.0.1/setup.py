from setuptools import setup, find_packages

setup(
    name="local-dns-service", 
    version="1.0.1", 
    description="A Python library for DNS service registration using Zeroconf",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Cld338",
    author_email="jihuno291@gmail.com",
    url="https://github.com/cld338/local-dns-service",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "zeroconf>=0.39.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
