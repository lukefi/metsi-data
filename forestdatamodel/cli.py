import os
import click
from forestdatamodel.formats.ForestBuilder import ForestCentreBuilder, VMI12Builder, VMI13Builder
from forestdatamodel.formats.file_io import pickle_reader, pickle_writer, vmi_file_reader, write_forest_csv, write_forest_json, write_forest_rsd, xml_file_reader
from forestdatamodel.model import ForestStand

@click.group()
def main():
    pass

def conv_inputfmt(input: str) -> str:
    _, ext = os.path.splitext(input.lower())
    if ext == ".xml":
        return "forest_centre"
    elif ext == ".pickle":
        return "pickle"
    raise click.ClickException("Can't infer input format from file name, use -i to set input format.")

def conv_outputfmt(output: str) -> str:
    _, ext = os.path.splitext(output.lower())
    if ext in (".pickle", ".json", ".rsd", ".csv"):
        return ext[1:]
    raise click.ClickException("Can't infer output format from file name, use -o to set output format.")

def conv_read(input: str, fmt: str, flags: dict) -> list[ForestStand]:
    if fmt == "pickle":
        return pickle_reader(input)
    elif fmt == "vmi13":
        Builder, read = VMI13Builder, vmi_file_reader
    elif fmt == "vmi12":
        Builder, read = VMI12Builder, vmi_file_reader
    elif fmt == "forest_centre":
        Builder, read = ForestCentreBuilder, xml_file_reader
    else:
        assert False # can't go here -- fmt is checked at convert()
    return Builder(flags, read(input)).build() # type: ignore

def conv_write(output: str, fmt: str, stands: list[ForestStand]):
    if fmt == "pickle":
        pickle_writer(output, stands)
    elif fmt == "json":
        write_forest_json(stands, output)
    elif fmt == "rsd":
        write_forest_rsd(stands, output)
    elif fmt == "csv":
        write_forest_csv(stands, output)

@main.command()
@click.argument(
    "input",
    type=click.Path(exists=True, dir_okay=False),
)
@click.argument(
    "output",
    type=click.Path(dir_okay=False, writable=True),
)
@click.option(
    "-i", "--input-format",
    type=click.Choice(["auto", "pickle", "vmi12", "vmi13", "forest_centre"]),
    default="auto",
    help="Input file format"
)
@click.option(
    "-o", "--output-format",
    type=click.Choice(["auto", "pickle", "json", "rsd", "csv"]),
    default="auto",
    help="Output file format"
)
@click.option(
    "-t", "--reference-trees",
    default=False,
    is_flag=True,
    help="Copy reference trees from VMI data"
)
@click.option(
    "-s", "--strata-origin",
    type=click.Choice(["1", "2", "3"]),
    default="1",
    help="Type number of forest center xml strata origin: '1' = Inventory, '2' = Present, '3' = Predicted"
)
def convert(
    input: str,
    output: str,
    input_format: str,
    output_format: str,
    **builder_flags
):
    if input_format == "auto":
        input_format = conv_inputfmt(input)
    if output_format == "auto":
        output_format = conv_outputfmt(output)
    stands = conv_read(input, input_format, builder_flags)
    conv_write(output, output_format, stands)

if __name__ == "__main__":
    main()
