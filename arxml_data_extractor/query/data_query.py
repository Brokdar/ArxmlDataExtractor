from __future__ import annotations

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
        is_relative: bool = True

    class Format(Enum):
        String = 0
        Integer = 1
        Float = 2
        Date = 3

    def __init__(self,
                 path: Union[XPath, Reference],
                 value: str = 'text',
                 format: Format = Format.String):

        self.path = self.__set_path(path)
        self.value = self.__set_value(value)
        self.format = format

    def __set_value(self, value):
        if (value == 'text' or value == 'tag' or value.startswith('@')):
            return value
        raise ValueError(f'{value} have to be one of [tag, text, @..]')

    def __set_path(self, path):
        if (isinstance(path, DataQuery.XPath)):
            if (':' in path.xpath):
                raise ValueError(f'"{path.xpath}" xpath must not contain namespace information')
        elif isinstance(path, DataQuery.Reference):
            if (':' in path.ref):
                raise ValueError(f'"{path.ref}" reference must not contain namespace information')
        else:
            raise TypeError(f'{path} is not of type XPath or Reference')

        return path
