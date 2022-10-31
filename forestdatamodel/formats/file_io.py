import csv
from enum import Enum
from itertools import chain
import pickle
from typing import Any, List, Tuple, Callable
from forestdatamodel.model import ForestStand, ReferenceTree, TreeStratum
import jsonpickle
from forestdatamodel.formats.rsd_const import MSBInitialDataRecordConst as msb_meta


def vmi_file_reader(file: str) -> List[str]:
    with open(file, 'r', encoding='utf-8') as input_file:
        return input_file.readlines()


def xml_file_reader(file: str) -> str:
    with open(file, 'r', encoding='utf-8') as input_file:
        return input_file.read()


def select_file_reader(file_type: str) -> Callable:
    if file_type == 'vmi':
        return vmi_file_reader
    elif file_type == 'xml':
        return xml_file_reader


def recreate_stand_indices(stands: List[ForestStand]) -> List[ForestStand]:
    for idx, stand in enumerate(stands):
        stand.set_identifiers(idx + 1)
    return stands


def recreate_tree_indices(trees: List[ReferenceTree]) -> List[ReferenceTree]:
    for idx, tree in enumerate(trees):
        tree.tree_number = idx + 1
    return trees


def cleaned_output(stands: List[ForestStand]) -> List[ForestStand]:
    """Recreate forest stands for output:
        1) filtering out non-living reference trees
        2) recreating indices for reference trees
        3) filtering out non-forestland stands and empty auxiliary stands
        4) recreating indices for stands"""
    for stand in stands:
        stand.reference_trees = [t for t in stand.reference_trees if t.is_living()]
        stand.reference_trees = recreate_tree_indices(stand.reference_trees)
    stands = [s for s in stands if (
        s.is_forest_land()
        and not s.is_other_excluded_forest()
        and (not s.is_auxiliary() or s.has_trees() or s.has_strata())
    )]
    stands = recreate_stand_indices(stands)
    return stands


def rsd_float(source: str or int or float or None) -> str:
    try:
        return f'{round(float(source), 6):.6f}'
    except:
        return f'{0:.6f}'


def msb_metadata(stand: ForestStand) -> Tuple[List[str], List[str], List[str]]:
    """
    Generate a triple with:
        MSB physical record metadata
        Initial data record stand metadata
        Initial data record tree set metadata
    """
    logical_record_length = sum([
        msb_meta.logical_record_metadata_length,
        msb_meta.stand_record_length,
        msb_meta.logical_subrecord_metadata_length,
        len(stand.reference_trees) * msb_meta.tree_record_length
    ])
    physical_record_metadata = [
        rsd_float(stand.stand_id),  # UID
        str(sum([
            logical_record_length,
            msb_meta.logical_record_header_length
        ]))  # physical record length
    ]
    logical_record_metadata = [
        rsd_float(msb_meta.logical_record_type),  # logical record type
        rsd_float(logical_record_length),
        rsd_float(msb_meta.stand_record_length)
    ]
    logical_subrecord_metadata = [
        rsd_float(len(stand.reference_trees)),
        rsd_float(msb_meta.tree_record_length)
    ]
    return physical_record_metadata, logical_record_metadata, logical_subrecord_metadata


def rsd_forest_stand_rows(stand: ForestStand) -> List[str]:
    """Generate RSD data file rows (with MSB metadata) for a single ForestStand"""
    result = []
    msb_preliminary_records = msb_metadata(stand)
    result.append(" ".join(chain(
        msb_preliminary_records[0],
        msb_preliminary_records[1],
        map(rsd_float, stand.as_rsd_row()),
        msb_preliminary_records[2]
    )))
    for tree in stand.reference_trees:
        result.append(" ".join(map(rsd_float, tree.as_rsd_row())))
    return result


def csv_value(source: Any) -> str:
    if source is None:
        return "None"
    else:
        return str(source)

def stand_to_csv_rows(stand: ForestStand, delimeter: str) -> List[str]:
    """converts the :stand:, its reference trees and tree strata to csv rows."""
    result = []
    result.append(delimeter.join(map(lambda x: csv_value(x), stand.as_internal_csv_row())))
    result.extend(
        map(
            lambda tree: delimeter.join(
                map(
                    lambda x: csv_value(x),
                    tree.as_internal_csv_row())),
            stand.reference_trees)
    )
    result.extend(
        map(
            lambda stratum: delimeter.join(
                map(
                    lambda x: csv_value(x),
                    stratum.as_internal_csv_row())),
            stand.tree_strata)
    )
    return result


def stands_to_csv(stands: List[ForestStand], delimeter: str) -> List[str]:
    result = []
    for stand in stands:
        result.extend(stand_to_csv_rows(stand, delimeter))
    return result


def csv_to_stands(file_path: str, delimeter: str) -> List[ForestStand]:
    stands = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=delimeter)
        for row in reader:
            if row[0] == "stand":
                stands.append(ForestStand.from_csv_row(row))
            elif row[0] == "tree":
                stands[-1].reference_trees.append(ReferenceTree.from_csv_row(row))
            elif row[0] == "stratum":
                stands[-1].tree_strata.append(TreeStratum.from_csv_row(row))

        # once all stands are recreated, add the stand reference to trees and strata 
        for stand in stands:
            for tree in stand.reference_trees:
                tree.stand = stand
            for stratum in stand.tree_strata:
                stratum.stand = stand
    return stands


def outputtable_rows(stands: List[ForestStand], formatter: Callable[[List[ForestStand]], List[str]]) -> List[str]:
    result = []
    for stand in cleaned_output(stands):
        result.extend(formatter(stand))
    return result


def rsd_rows(stands: List[ForestStand]) -> List[str]:
    """Generate RSD file contents for the given list of ForestStand"""
    return outputtable_rows(stands, lambda stand: rsd_forest_stand_rows(stand))


def write_forest_csv(stands: List[ForestStand], filename: str):
    with open(filename, 'w', newline='\n') as file:
        file.writelines('\n'.join(stands_to_csv(stands, ';')))


def write_forest_rsd(stands: List[ForestStand], filename: str):
    with open(filename, 'w', newline='\n') as file:
        file.writelines('\n'.join(rsd_rows(stands)))


def write_forest_json(stands: List[ForestStand], output_file: str):
    jsonpickle.set_encoder_options("json", indent=2)
    with open(output_file, 'w', newline='\n') as f:
        f.write(jsonpickle.encode(stands))

def pickle_writer(file_path: str, data: Any):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f, protocol=5)

def pickle_reader(file_path: str) -> Any:
    with open(file_path, 'rb') as f:
        return pickle.load(f)
