"""
Setup configuration for Nakala Client package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else ""

setup(
    name="nakala-client",
    version="1.0.0",
    author="École française d'Extrême-Orient",
    author_email="digital@efeo.fr",
    description="A comprehensive Python client for the Nakala research data repository API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/efeo/o-nakala-core",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.32.3",
        "tenacity>=9.1.2",
        "typing-extensions>=4.14.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "cli": [
            "click>=8.0.0",
            "rich>=13.0.0",
            "python-dotenv>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nakala-upload=nakala_client.upload:main",
            "nakala-collection=nakala_client.collection:main",
            "nakala-search=nakala_client.search:main",
            "nakala-curator=nakala_client.curator:main",
            "nakala-metadata=nakala_client.metadata:main",
        ],
    },
    include_package_data=True,
    package_data={
        "nakala_client": ["config/*.json", "templates/*.csv"],
    },
)
