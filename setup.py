from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ascii_chiper",
    version="0.1.2",
    author="glizzykingdreko",
    author_email="glizzykingdreko@protonmail.com",
    description="A versatile Python module for encrypting and decrypting strings, integers, and dictionaries using a variety of encryption techniques.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glizzykingdreko/ascii_chiper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy"
    ],
)