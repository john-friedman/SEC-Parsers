from setuptools import setup, find_packages

# TODO check dependencies
# add github link
setup(
    name="sec_parsers",
    author="John Friedman",
    version="0.501",
    description = "A package to parse SEC filings",
    packages=find_packages(),
    install_requires=[
        'lxml', 
    ],
)