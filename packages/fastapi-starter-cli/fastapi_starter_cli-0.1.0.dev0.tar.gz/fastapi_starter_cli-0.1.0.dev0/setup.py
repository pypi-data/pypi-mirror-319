from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="fastapi-starter-cli",
    version="0.1.0-dev",
    packages=find_packages(include=['cli', 'cli.*']),
    include_package_data=True,
    install_requires=[
        "typer>=0.15.0",
        "colorama>=0.4.6",
        "rich>=13.9.0",
    ],
    entry_points={
        "console_scripts": [
            "fastapi=cli.main:app",
        ],
    },
    author="betooo",
    description="CLI tool for generating FastAPI projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RobertoRuben/fastapi-starter-cli",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    package_data={
        'cli': ['templates/**/*', 'templates/**/**/*'],
    },
)