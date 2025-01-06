import setuptools
from pathlib import Path

setuptools.setup(
    name="dexpdf2",
    version="1.0.1",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(
        exclude=["tests", "data"])  # Excludes tests and data

)


# To upload need to set username and password through and API token:
# $env:TWINE_USERNAME="__token__"
# $env:TWINE_PASSWORD="your_actual_api_token_here"
# twine upload dist/*
