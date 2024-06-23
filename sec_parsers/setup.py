from setuptools import setup, find_packages

setup(
    name="sec_parsers",
    author="John Friedman",
    version="0.401",
    description = "A package to parse SEC filings",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'pandas',
        're',
        'tempfile',
        'pandas'   
    ],
)