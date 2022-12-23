import geopandas
import datetime

from geopandas import GeoSeries
from shapely.geometry import Polygon, Point
from typing import Tuple, List, Optional, Dict
from xml.etree.ElementTree import Element
from types import SimpleNamespace
from forestdatamodel.formats import util

ns = {
        "schema_location": "http://standardit.tapio.fi/schemas/forestData ForestData.xsd",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xlink": "http://www.w3.org/1999/xlink",
        "gml": "http://www.opengis.net/gml",
        "gdt": "http://standardit.tapio.fi/schemas/forestData/common/geometricDataTypes",
        "co": "http://standardit.tapio.fi/schemas/forestData/common",
        "sf": "http://standardit.tapio.fi/schemas/forestData/specialFeature",
        "op": "http://standardit.tapio.fi/schemas/forestData/operation",
        "dts": "http://standardit.tapio.fi/schemas/forestData/deadTreeStrata",
        "tss": "http://standardit.tapio.fi/schemas/forestData/treeStandSummary",
        "tst": "http://standardit.tapio.fi/schemas/forestData/treeStratum",
        "ts": "http://standardit.tapio.fi/schemas/forestData/treeStand",
        "st": "http://standardit.tapio.fi/schemas/forestData/Stand",
        "default": "http://standardit.tapio.fi/schemas/forestData"
    }


def parse_stand_basic_data(xml_stand: Element) -> SimpleNamespace:
    sns = SimpleNamespace()
    sns.id = xml_stand.attrib['id']
    sns.CompleteState = xml_stand.findtext('./st:StandBasicData/st:CompleteState', None, ns)
    sns.StandBasicDataDate = xml_stand.findtext('./st:StandBasicData/st:StandBasicDataDate', None, ns)
    sns.Area = xml_stand.findtext('./st:StandBasicData/st:Area', None, ns)
    sns.SubGroup = xml_stand.findtext('./st:StandBasicData/st:SubGroup', None, ns)
    sns.FertilityClass = xml_stand.findtext('./st:StandBasicData/st:FertilityClass', None, ns)
    sns.DrainageState = xml_stand.findtext('./st:StandBasicData/st:DrainageState', None, ns)
    sns.MainGroup = xml_stand.findtext('./st:StandBasicData/st:MainGroup', None, ns)
    sns.CuttingRestriction = xml_stand.findtext('./st:StandBasicData/st:CuttingRestriction', None, ns)
    return sns


def parse_stratum_data(estratum: Element) -> SimpleNamespace:
    sns = SimpleNamespace()
    sns.id = estratum.attrib['id']
    sns.StratumNumber = estratum.findtext('tst:StratumNumber', None, ns)
    sns.TreeSpecies = estratum.findtext('tst:TreeSpecies', None, ns)
    sns.Storey = estratum.findtext('tst:Storey', None, ns)
    sns.Age = estratum.findtext('tst:Age', None, ns)
    sns.BasalArea = estratum.findtext('tst:BasalArea', None, ns)
    sns.StemCount = estratum.findtext('tst:StemCount', None, ns)
    sns.MeanDiameter = estratum.findtext('tst:MeanDiameter', None, ns)
    sns.MeanHeight = estratum.findtext('tst:MeanHeight', None, ns)
    sns.Volume = estratum.findtext('tst:Volume', None, ns)
    sns.DataSource = estratum.findtext('co:DataSource', None, ns)
    return sns


def parse_date(value: str) -> datetime.date:
    """ format of value is yyyy-mm-dd """
    date = list(map(int, value.split('-')))
    return datetime.date(*date)


def parse_past_operations(eoperations: List[Element]) -> Dict[int, Tuple[int, int]]:
    operations = {}
    for eoper in eoperations:
        oper_id = util.parse_int(eoper.attrib['id'])
        oper_type = util.parse_int(eoper.findtext('./op:OperationType', None, ns))
        date = parse_date(eoper.findtext('./op:CompletionData/op:CompletionDate', None, ns))
        oper_year = date.year
        operations[oper_id] = (oper_type, oper_year)
    return operations


def parse_future_operations(eoperations: List[Element]) -> Dict[int, Tuple[int, int]]:
    operations = {}
    for eoper in eoperations:
        oper_id = util.parse_int(eoper.attrib['id'])
        oper_type = util.parse_int(eoper.findtext('./op:OperationType', None, ns))
        oper_year = util.parse_int(eoper.findtext('./op:ProposalData/op:ProposalYear', None, ns))
        operations[oper_id] = (oper_type, oper_year)
    return operations


def parse_stand_operations(estand: Element, target_operations=None) -> List[Dict[int, Tuple[int, int]]]:
    eoperations = estand.findall('./op:Operations/op:Operation', ns)
    past_eoperatios = list(filter(lambda eoper: False if eoper.find('./op:CompletionData', ns) is None else True, eoperations))
    future_eoperations = list(filter(lambda eoper: False if eoper.find('./op:ProposalData', ns) is None else True, eoperations))
    past_operations = parse_past_operations(past_eoperatios)
    future_operations = parse_future_operations(future_eoperations)
    if target_operations == 'past':
        return past_operations
    elif target_operations == 'future':
        return future_operations
    else:
        all_operations = {}
        all_operations.update(past_operations)
        all_operations.update(future_operations)
        return all_operations


def parse_year(source: str) -> int or None:
    return(None if len(source) < 4 else util.parse_int(source[:4]))


def parse_land_use_category(source: str) -> int or None:
    if source in ('1','2','3'):
        return int(source)
    return None


def parse_drainage_category(source: str) -> int or None:
    if source in ('1', '2'):
        return 0
    elif source in ('3'):
        return 1
    elif source in ('6'):
        return 2
    elif source in ('7'):
        return 3
    elif source in ('8'):
        return 4
    elif source in ('9'):
        return 5
    else:
        return util.parse_int(source)


def parse_forest_management_category(source: str) -> int or float or None:
    try:
        if source in ('1'):
            return 2.1
        elif source in ('2', '3'):
            return 2.2
        elif source in ('4'):
            return 2.3
        elif source in ('6', '7'):
            return 2.4
        elif source in ('5'):
            return 2.5
        elif source in ('8'):
            return 2.6
        elif source in ('9'):
            return 7
        else:
            return 1
    except:
        return None


def point_series(value: str) -> List[Tuple[float, float]]:
    """ Converts a gml string presentation to a list of (x, y) points"""
    series = []
    for xy_point in value.split(' '):
        point = xy_point.split(',')
        series.append((float(point[0]), float(point[1])))
    return series


def parse_centroid(sns: SimpleNamespace) -> Tuple[float, float, str]:
    """
    GeoSeries instance of Geopandas library is used as container for stand gml data.
    The centroid of geoseries contain the latitude and longitude of the stand geometry.

    Also the parsed crs is returned altough SMK XML is standardised to use ESPG:3067 as default.
    """
    crs = sns.egeometry.attrib['srsName']
    raw_coords = sns.egeometry.findtext(sns.coord_xpath, None, ns)
    Geometry = None
    if sns.geometry_type == 'point':
        Geometry = Point
    else:
        Geometry = Polygon
    geometry = Geometry(point_series(raw_coords))
    gs = geopandas.GeoSeries(data=geometry, crs=crs)
    return (gs.centroid.x[0], gs.centroid.y[0], gs.crs.srs)


def parse_coordinates(estand: Element) -> Tuple[float, float, str]:
    """
    Extracting stand latitude and longitude coordinates from gml point or polygon smk xml element.
    Also the coordiante reference system (crs) is extracted and returned.
    """
    epoint = estand.find('./st:StandBasicData/gdt:PolygonGeometry/gml:pointProperty/gml:Point', ns)
    epolygon = estand.find('./st:StandBasicData/gdt:PolygonGeometry/gml:polygonProperty/gml:Polygon', ns)
    sns = SimpleNamespace(geometry_type=None, egeometry=None, coord_xpath=None)
    if epoint:
        sns.geometry_type = 'point'
        sns.egeometry = epoint
        sns.coord_xpath = './gml:coordinates'
    elif epolygon:
        sns.geometry_type = 'polygon'
        sns.egeometry = epolygon
        sns.coord_xpath = './gml:exterior/gml:LinearRing/gml:coordinates'
    else:
        return (None, None, None)
    (longitude, latitude, crs) = parse_centroid(sns)
    return (float(latitude), float(longitude), crs)
