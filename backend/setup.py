#!/usr/bin/env python3
"""
Ramanujan Compression SDK - Setup Configuration
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ramanujan-tokenizer",
    version="0.1.0",
    author="Ramanujan Compression Team",
    author_email="team@ramanujan-compression.com",
    description="Ramanujan-inspired compression SDK with HuggingFace tokenizer integration",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ramanujan-compression/ramanujan-tokenizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "pro": [
            "torch>=1.9.0",
            "cupy-cuda11x>=9.0.0",
            "stripe>=3.0.0",
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "ramanujan-cli=ramanujan_cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ramanujan_tokenizer": ["tokenizer_config.json"],
    },
)