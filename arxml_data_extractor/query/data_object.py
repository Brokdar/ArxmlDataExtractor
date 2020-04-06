from __future__ import annotations

from typing import Union, List

from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_value import DataValue


class DataObject():

    def __init__(self, name: str, path: Union[DataQuery.XPath, DataQuery.Reference],
                 values: List[Union[DataValue, DataObject]]):
                 
        self.name = name
        self.path = self.__set_path(path)
        self.values = self.__set_values(values)

    def __set_path(self, path):
        if (isinstance(path, (DataQuery.Reference, DataQuery.XPath))):
            return path
        else:
            raise TypeError(f'path has to be of type DataQuery.XPath or DataQuery.Reference')

    def __set_values(self, values):
        if type(values) is not list:
            raise TypeError('values must be of type list')
        if not values:
            raise ValueError(f'values cannot be empty')
        if all(isinstance(x, (DataObject, DataValue)) for x in values):
            return values
        raise ValueError('values can only contain items of type DataObject or DataValue')