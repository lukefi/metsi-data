# MetSi forest data model

This project is a collection of Python classes for a structured object model of forest stands with contained tree strata
and reference trees. We also serve a library implementation for converting forest inventory data into these classes.

Original implementation of the data model and data conversion by Arto Haara, Natural Resources Institute Finland.

Backwards compatibility with semantic versioning is guaranteed for users of this library.

## Technology and the project

This is a Python library developed under Python 3.10. We offer support for this library via GitHub issues and welcome
pull requests for improvement.

## Library description

The data structures for forest stands and reference trees were originally created from the RSD data format specification
of the MELA forest calculation utility. They have been extended for tree strata. The core data model is gradually being
changed from RSD categorizations to be a unified representation for Finnish national forest survey (VMI) and Finnish
Forest Center (SMK) data formats. This is achieved by mapping out enumerations and utilizing them for conversion
between the source data formats, the Metsi data model and the RSD output model.

We provide an input converter from VMI12 and VMI13 forest inventory data[^1] and Finnish Forest Center forest
inventory data[^2]. In addition, output data conversion is provided for creating RSD-like files according to the MELA
forest calculation utility 2016 specification. The conversion functionality is under consideration to be moved into a
separate code project.

## Library structure

The code for this project is structured as follows.

| path                                | comment                                                                                                         |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| metsi_data/model.py                 | Main data structures module                                                                                     |
| metsi_data/conversion               | Utility package for converting enumerations between data formats                                                |
| metsi_data/enums                    | Package for category variable enumerations                                                                      |
| metsi_data/formats/ForestBuilder.py | Builder pattern style classes for populating a collection of forest stands with reference tree and stratum data |
| metsi_data/formats/io_utils.py      | Utilities for formatting data for various output formats                                                        |
| metsi_data/formats/rsd_const.py     | support structures for RSD data indices                                                                         |
| metsi_data/formats/smk_util.py      | Forest Centre XML data related parsing logic                                                                    |
| metsi_data/formats/util.py          | general utility functions                                                                                       |
| metsi_data/formats/vmi_const.py     | support structures for VMI data indices                                                                         |
| metsi_data/formats/vmi_util.py      | support functionality for VMI data parsing and conversion                                                       |
| tests                               | Test suites                                                                                                     |

## Data structures

Main data structure classes for the internal representation are as follows.

| class         | description                                                                                      |
|---------------|--------------------------------------------------------------------------------------------------|
| ForestStand   | Forest stand is a measurement area of interest for forest statistics and metadata                |
| ReferenceTree | Reference tree is a representation of trees of a certain species and size within a forest stand  |
| TreeStratum   | Tree stratum is a statistical representation of trees of a certain species within a forest stand |

Enumerated properties for above classes are as follows, with equivalent enumerations from source and target data formats
prefixed with `Vmi*`, `ForestCentre*` and `Mela*`:

| class         | enumerated property  | description                      |
|---------------|----------------------|----------------------------------|
| ForestStand   | LandUseCategory      | Type of land within this area    |
| ForestStand   | OwnerCategory        | Ownership of this area           |
| ForestStand   | SoilPeatlandCategory | Soil type of this area           |
| ForestStand   | SiteType             | Site richness of this area       |
| ForestStand   | DrainageCategory     | Drainage status of this area     |
| ForestStand   | ...                  | Work in progress                 |
| ReferenceTree | TreeSpecies          | Species of these trees           |
| ReferenceTree | ...                  | Work in progress                 |
| TreeStratum   | TreeSpecies          | Species of trees of this stratum |

## Troubleshooting

**Geopandas dependency resolution in Windows using pip**

For using the Forestry Centre (SMK) XML source files, geopandas library is needed for geocoordinate handling. When
using `pip` for dependency management, geopandas depends on the Fiona library, which depends on GDAL. Fiona and GDAL are
not properly installable without a C++ build environment.

Workaround:

Use Anaconda[^3] for Python virtual environment and library dependency management.

OR

Obtain WHL prepackaged Fiona and GDAL libraries from https://www.lfd.uci.edu/~gohlke/pythonlibs where you will find a
file such

* Fiona‑1.8.21‑cp310‑cp310‑win_amd64.whl
* GDAL‑3.4.2‑cp310‑cp310‑win_amd64.whl

Depending on the python version you are using, download the correct file by replacing the cp310 in the filename above:

* Python 3.10 -> cp310
* Python 3.9 -> cp39
* etc...

Install the package using `pip install GDAL‑3.4.2‑cp310‑cp310‑win_amd64.whl`
and `pip install Fiona‑1.8.21‑cp310‑cp310‑win_amd64.whl` before proceeding with `pip install -r requirements.txt`.

---

[^1] [National forest survey](https://www.luke.fi/fi/seurannat/valtakunnan-metsien-inventointi-vmi)

[^2] [Finnish Forest Center MV1.9 inventory data](https://metsatietostandardit.bitcomp.com)

[^3] [Anaconda](https://www.anaconda.com/products/distribution)