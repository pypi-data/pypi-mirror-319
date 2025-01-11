from setuptools import setup, find_packages

setup(
    name="tenzro",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
    ],
    author="Tenzro Team",
    author_email="eng@tenzro.com",
    description="Official Python SDK for Tenzro API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tenzro/tenzro-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
