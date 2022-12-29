import setuptools
from setuptools import setup

setup(
    name="forestdatamodel",
    description="Data classes and utilities for forest stand, tree strata and reference trees representation",
    version="1.0.0-rc1",
    packages=setuptools.find_namespace_packages(include=['forestdatamodel*']),
    install_requires=[
        "geopandas==0.12.*",
        "jsonpickle==3.0.*"
    ]
)
