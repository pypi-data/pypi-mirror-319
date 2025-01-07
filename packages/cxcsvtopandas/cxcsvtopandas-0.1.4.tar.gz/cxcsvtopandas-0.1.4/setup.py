from setuptools import setup, find_packages

setup(
    name="cxcsvtopandas",
    version="0.1.4",
    packages=find_packages(),
    author="Amit Gupta",
    author_email="amit864@gmail.com",
    description="Python package for SAI propritary report generation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amitgupta7/base-cxpandascsvloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          "pandas==2.2.2"
          ,"plotly==5.22.0"
    ],
    python_requires='>=3.6',
)
