import sys
from typing import Optional, Any, Tuple
from enum import Enum


def parse_int(source: str) -> Optional[int]:
    try:
        return int(source)
    except (ValueError, TypeError):
        return None


def parse_float(source: str) -> Optional[float]:
    try:
        return float(source)
    except (ValueError, TypeError):
        return None


def get_or_default(maybe: Optional[Any], default: Any = None) -> Any:
    return default if maybe is None else maybe


def convert_str_to_type(_class: type, value: str, property_name: str):
    """convert value to the type given by its type hint in self.__annotations__"""
    if value == "None":
        return None
    property_type = _class.__annotations__[property_name]
    if property_type in (bool, Optional[bool]):
        return value == "True"
    if property_type in (int, Optional[int]):
        return int(value)
    if property_type in (float, Optional[float]):
        return float(value)
    if property_type in (str, Optional[str]):
        return str(value)

    if type(value) == tuple:
        if not any(v == "None" for v in value):
            #stand.stems_per_ha_scaling_factors
            if property_type == tuple[float, float]:
                return tuple(float(v) for v in value)
            #stand.geo_location
            if property_type == Optional[tuple[float, float, float, str]]:
                return tuple(float(v) for v in value[0:3]) + (str(value[3]),)
            #stand.monthly rainfall and stand.monthly_temperatures
            if property_type == Optional[list[float]]:
                return [float(v) for v in value]
            #stratum.stand_origin_relative_position
            if property_type == tuple[float,float,float]:
                return tuple(float(v) for v in value) 
    else:
        raise Exception(f"could not convert {value} to {property_name}.")
