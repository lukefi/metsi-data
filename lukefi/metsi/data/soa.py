from functools import reduce
from typing import Optional, Sequence, TypeVar, Generic, Hashable, ClassVar
import numpy as np
import pandas as pd


T = TypeVar("T", bound=Hashable)


class Soa(Generic[T]):
    """
    This class implements a Pandas DataFrame/Numpy backed Struct of Arrays data structure for a list of objects T.
    The rationale is to provide a memory-contiguous and thus better performing storage for maintaining state changes for
    an Array of Structs kind of collection, such as a list of objects. Data classes may implement this as an alternative
    for their native dict based property maps or as partial overlays for subsets of properties.
    """

    def __init__(self, object_list: list[T] = [], initial_property_names: list[str] = []):
        """Constructs a Soa instance, optionally populating it with given object data and property names."""
        values = []
        if object_list and initial_property_names:
            values = [[obj.__dict__[property_name] for obj in object_list] for property_name in initial_property_names]
        self.frame = pd.DataFrame(values, columns=object_list, index=initial_property_names)

    def has_property(self, prop_name: str) -> bool:
        """Truth value for a property name being represented in the dataframe."""
        return prop_name in self.frame.index

    def has_object(self, object_reference: T) -> bool:
        """Truth value for object being represented in the dataframe."""
        return object_reference in self.frame.columns

    def get_property_values(self, prop_name: str) -> Optional[np.array]:
        """Find the list of values for an existing property or None"""
        return self.frame.loc[prop_name].array.to_numpy() if self.has_property(prop_name) else None

    def get_object_properties(self, object_reference: T) -> list[tuple]:
        """
        Find existing property-value pairs for given object or empty list for unknown object or no properties recorded.
        """
        return [(x, self.frame[object_reference][x]) for x in self.frame.index] if self.has_object(object_reference) else list()

    def get_object_property(self, prop_name: str, object_reference: T) -> Optional:
        """Find existing property value or None for unknown object or property."""
        return self.frame[object_reference][prop_name] if self.has_property(prop_name) and self.has_object(object_reference) else None

    def upsert_property_values(self, prop_name: str, values: Sequence):
        """
        Insert or update the values for a given property. Raises ValueError if values length doesn't match dataframe
        dimensions. This function has to blindly trust that given values match the objects/columns they are intended
        for.
        """
        if len(values) != len(self.frame.columns):
            raise ValueError(f"Attempting to insert {len(list(values))} values into container of {len(self.frame.columns)} values")
        if self.has_property(prop_name):
            self.frame.loc[prop_name] = values
        else:
            addition = pd.DataFrame([values], columns=self.frame.columns, index=[prop_name])
            self.frame = pd.concat((self.frame, addition))

    def upsert_objects(self, object_references: list[T]):
        """
        Insert or update the columns for given objects with values from the objects' properties.
        """
        def split_accumulator(acc: tuple, cur):
            if cur in self.frame.columns:
                acc[0].append(cur)
            else:
                acc[1].append(cur)
            return acc

        old, new = reduce(split_accumulator, object_references, ([], []))

        for obj in old:
            values = [obj.__dict__.get(prop_name) for prop_name in self.frame.index]
            self.frame[obj] = values
        if new:
            values = []
            for prop_name in self.frame.index:
                rows = [obj.__dict__.get(prop_name) for obj in new]
                if rows:
                    values.append(rows)
            addition = pd.DataFrame(values, index=self.frame.index, columns=new)
            self.frame = pd.concat((self.frame, addition), axis=1)

    def del_objects(self, object_references: list[T]):
        """Drop from dataframe those columns which exist for the given objects."""
        removables = set(object_references) & set(self.frame.columns)
        if removables:
            self.frame = self.frame.drop(removables, axis=1)

    def fixate(self):
        for object_reference in self.frame.columns:
            for property in self.frame.index:
                object_reference.__dict__[property] = self.get_object_property(property, object_reference)
        self.frame = pd.DataFrame([], columns=self.frame.columns)


class Soable:
    """This class implements access-by-precedence to Soa values via object properties."""
    _ol = ClassVar[Soa]

    def __getattribute__(self, item):
        """Return property from overlay if the overlay exists and the value is known for this object. Return default
        dict-value otherwise."""
        if object.__getattribute__(self, '_ol'):
            return object.__getattribute__(self, '_ol').get_object_property(item, self) or object.__getattribute__(self, item)
        else:
            return object.__getattribute__(self, item)

    @classmethod
    def set_soa(cls, soa: Soa):
        cls._ol = soa
