"""Setup script for the Nakala Python Connector.

This script allows the package to be installed with `pip install -e .`
for development purposes.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nakala-connector",
    version="0.1.0",
    author="EFEO",
    author_email="contact@efeo.fr",
    description="A Python client for the Nakala API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EFEO/nakala-connector",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "pydantic>=1.10.0,<3.0.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=0.991",
            "types-requests>=2.28.0",
            "types-python-dateutil>=2.8.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.19.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Text Processing",
    ],
)
