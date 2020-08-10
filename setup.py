import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="documental",
    version="0.2.0",
    author="Dennis Merkus",
    description="Unified interface for handling different structured document types",
    long_description=long_description,
    url="https://github.com/DennisMerkus/documental",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.8",
)
