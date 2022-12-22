import setuptools
from setuptools import setup

setup(
    name="forestdatamodel",
    description="Data classes and utilities for forest stand, tree strata and reference trees representation",
    version="0.4.7",
    packages=setuptools.find_namespace_packages(include=['forestdatamodel*']),
    install_requires=[
        "geopandas==0.10.*",
        "jsonpickle==2.2.0",
        "click==8.1.*"
    ],
    entry_points={"console_scripts": ["fdm=forestdatamodel.cli:main"]}
)
