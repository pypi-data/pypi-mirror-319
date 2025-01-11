from setuptools import setup, find_packages

setup(
    name="dtseqlib",
    version=1.0,
    description="Sequence data type.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="BesBobowyy",
    author_email="",
    url="https://github.com/BesBobowyy/dtseqlib",
    packages=find_packages(),
    classfilters=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>3.0'
)
