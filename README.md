# Forest data model and the forest inventory data convertter

This project is a collection of Python classes usable describing a structured object model of forest stands with contained tree stratum and reference tree.

The project also serves a CLI application for converting forest inventory data into these classes.

## MENU forest data model

The classes were originally created from the RSD data format specification of the MELA forest calculation utility.
Going forward they will serve as an unified model for Finnish national forest survey (VMI) and Finnish forestry centre (SMK) data sources.
Utilities for conversion of the data for known application targets are provided, namely the Motti growth models and Mela 2.0 growth and forest management operation models.

Backwards compatibility with semantic versioning is guaranteed for users of this library.

## Forest inventory data converter

The code implements a data converter for VMI12 and VMI13 forest inventory data<sup>[1](#fn1)</sup> into other formats.
Original implementation produces the RSD data format used as a source format for the MELA forest growth simulator.
The aim of this project is to produce a tool which is able to incorporate further source formats and target formats.
In addition to VMI data, we wish to support Forest Centre (Metsäkeskus) XML data

Original implementation by Arto Haara

## Library structure

| path                                     | comment                                                                                                               |
|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| forestdatamodel/conversion               | Utilities for converting VMI12, VMI13 and Forest Centre data to Internal model, and further mapping to output formats |
| forestdatamodel/enums                    | Package for category variable enumerations                                                                            |
| forestdatamodel/formats/ForestBuilder.py | Builder pattern style classes for populating a collection of forest stands with reference tree and stratum data       |
| forestdatamodel/formats/io_utils.py      | Utilities for formatting data for various output formats                                                              |
| forestdatamodel/formats/rsd_const.py     | support structures for RSD data indices                                                                               |
| forestdatamodel/formats/smk_util.py      | Forest Centre XML data related parsing logic                                                                          |
| forestdatamodel/formats/util.py          | general utility functions                                                                                             |
| forestdatamodel/formats/vmi_const.py     | support structures for VMI data indices                                                                               |
| forestdatamodel/formats/vmi_util.py      | support functionality for VMI data parsing and conversion                                                             |
| tests                                    | Test suites                                                                                                           |

### Troubleshooting

#### Geopandas dependency resolution in Windows using pip

For using the Forestry Centre (SMK) XML source files, geopandas library is needed for geocoordinate handling.
When using `pip` for dependency management, geopandas depends on the Fiona library, which depends on GDAL.
Fiona and GDAL are not properly installable without a C++ build environment.

Workaround:

Use [Anaconda](https://www.anaconda.com/products/distribution) for Python virtual environment and library dependency management.

OR

Obtain WHL prepackaged Fiona and GDAL libraries from https://www.lfd.uci.edu/~gohlke/pythonlibs where you will find a file such
* Fiona‑1.8.21‑cp310‑cp310‑win_amd64.whl
* GDAL‑3.4.2‑cp310‑cp310‑win_amd64.whl

Depending on the python version you are using, download the correct file by replacing the cp310 in the filename above:

* Python 3.10 -> cp310
* Python 3.9 -> cp39
* etc...

Install the package using `pip install GDAL‑3.4.2‑cp310‑cp310‑win_amd64.whl` and `pip install Fiona‑1.8.21‑cp310‑cp310‑win_amd64.whl`  before proceeding with `pip install -r requirements.txt`.

### References

<a name="fn1">1</a>: https://www.luke.fi/en/natural-resources/forest/forest-resources-and-forest-planning/forest-resources
