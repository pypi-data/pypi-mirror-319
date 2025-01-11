from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cvmpy",
    version="0.1.3",
    author="Douglas Ricardo Sansao",
    author_email="douglasrsansao@example.com",
    description="Package to read and process data from the CVM website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drsansao/cvm",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.2.3",
        "numpy>=1.21.1",
        "beautifulsoup4>=4.10.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.0',
)