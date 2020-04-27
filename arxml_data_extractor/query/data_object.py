from __future__ import annotations

from typing import Union, List
import logging

from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_value import DataValue


class DataObject():

    def __init__(self, name: str, path: Union[DataQuery.XPath, DataQuery.Reference],
                 values: List[Union[DataValue, DataObject]]):

        self.logger = logging.getLogger()
        self.name = name
        self.path = self.__set_path(path)
        self.values = self.__set_values(values)

    def __set_path(self, path):
        if (isinstance(path, (DataQuery.Reference, DataQuery.XPath))):
            return path
        else:
            error = f'DataObject(\'{self.name}\') - path ({type(path)}) must be of type DataQuery.XPath or DataQuery.Reference'
            self.logger.error(error)
            raise TypeError(error)

    def __set_values(self, values):
        if type(values) is not list:
            error = f'DataObject(\'{self.name}\') - values ({type(values)}) must be of type list'
            self.logger.error(error)
            raise TypeError(error)
        if not values:
            error = f'DataObject(\'{self.name}\') - values cannot be empty'
            self.logger.error(error)
            raise ValueError(error)
        if all(isinstance(x, (DataObject, DataValue)) for x in values):
            return values

        error = f'DataObject(\'{self.name}\') - values can only hold items of type DataObject or DataValue'
        self.logger.error(error, [f'{v}: {type(v)}' for v in values])
        raise ValueError(error)
