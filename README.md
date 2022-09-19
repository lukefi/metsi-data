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

### Application structure

| path                          | comment                                                                                                                |
|-------------------------------|------------------------------------------------------------------------------------------------------------------------|
| forestdatamodel/cli.py                            | application entry point                                                                            |
| forestdatamodel/formats                           | application source code                                                                            |
| forestdatamodel/formats/file_io.py                | File IO                                                                                            |
| forestdatamodel/formats/ForestBuilder.py          | Builder pattern style classes for populating a collection of Forest Stands with Tree data          |
| forestdatamodel/formats/rsd_const.py              | support structures for RSD data indices                                                            |
| forestdatamodel/formats/smk_util.py               | SMK related parse logic                                                     |
| forestdatamodel/formats/util.py                   | general utility functions                                                                          |
| forestdatamodel/formats/vmi_const.py              | support structures for VMI data indices                                                            |
| forestdatamodel/formats/vmi_util.py               | support functionality for VMI-RSD data conversion                                                  |
| tests                                             | Test suites                                                                                        |
| data                                              | example data                                                                                       |
| data/VMI_12_formaatti.dat                         | VMI12 example source data                                                                          |
| data/VMI_13_formaatti.dat                         | VMI13 example source data                                                                          |
| data/SMK_formaatti.xml                            | SMK example source data                                                                          |

Program entry point is `forestdatamodel/cli.py`.

### Instructions

Application can be run from the project root. Usage instructions:

```
Usage: python -m forestdatamodel.cli convert [OPTIONS] INPUT OUTPUT

Options:
  -i, --input-format [auto|pickle|vmi12|vmi13|forest_centre]
                                  Input file format
  -o, --output-format [auto|pickle|json|rsd|csv]
                                  Output file format
  -t, --reference-trees           Copy reference trees from VMI data
  -s, --strata-origin [1|2|3]     Type number of forest center xml strata
                                  origin: '1' = Inventory, '2' = Present, '3'
                                  = Predicted
  --help                          Show this message and exit.
```

`python -m forestdatamodel.cli convert --help`


For example the following will convert vmi12 source data to pickle format:

`python -m forestdatamodel.cli convert -i vmi12 -o pickle data/VMI_12_formaatti.dat vmi12_fdm.pickle`


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
