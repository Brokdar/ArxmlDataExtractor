from __future__ import annotations

import logging
from enum import Enum
from typing import Union
from dataclasses import dataclass


class DataQuery():

    @dataclass
    class Reference():
        ref: str

    @dataclass
    class XPath():
        xpath: str
        is_reference: bool = False

    class Format(Enum):
        String = 0
        Integer = 1
        Float = 2
        Date = 3

    def __init__(self,
                 path: Union[XPath, Reference],
                 value: str = 'text',
                 format: Format = Format.String):

        self.logger = logging.getLogger()
        self.path = self.__set_path(path)
        self.value = self.__set_value(value)
        self.format = format

    def __set_value(self, value):
        if (value == 'text' or value == 'tag' or value.startswith('@')):
            return value

        error = f'DataQuery - invalid value \'{value}\'. Value needs to be either \'tag\', \'text\' or \'@..\''
        self.logger.error(error)
        raise ValueError(error)

    def __set_path(self, path):
        if (isinstance(path, DataQuery.XPath)):
            if (':' in path.xpath):
                error = f'DataQuery - invalid XPath \'{path.xpath}\'. XPath must not contain namespace information'
                self.logger.error(error)
                raise ValueError(error)
        elif isinstance(path, DataQuery.Reference):
            if (':' in path.ref):
                error = f'DataQuery - invalid Reference \'{path.ref}\'. Reference must not contain namespace information'
                self.logger.error(error)
                raise ValueError(error)
        else:
            error = f'DataQuery - invalid path type ({type(path)}). Path must be of type DataQuery.XPath or DataQuery.Reference'
            logging.error(error)
            raise TypeError(error)

        return path
