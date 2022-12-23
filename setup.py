import setuptools
from setuptools import setup

setup(
    name="forestdatamodel",
    description="Data classes and utilities for forest stand, tree strata and reference trees representation",
    version="0.3.4",
    packages=setuptools.find_namespace_packages(include=['forestdatamodel*']),
    install_requires=[
        "scipy==1.7.*",
        "geopandas==0.10.*",
        "jsonpickle==2.2.0",
        "forestryfunctions@git+https://github.com/menu-hanke/forestry-function-library@0.1.2#egg=forestryfunctions"
    ],
    entry_points={"console_scripts": ["fdm=forestdatamodel.cli:main"]}
)
