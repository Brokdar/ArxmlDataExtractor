from typing import List, Union

from arxml_data_extractor.query.data_object import DataObject
from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_value import DataValue


class QueryBuilder():
    __path_separator = ':'
    __format_separator = '>'

    def __init__(self):
        pass

    def build(self, config: dict) -> List[DataObject]:
        data_objects = []
        for key, value in config.items():
            data_object = self.__parse_object(key, value)
            data_objects.append(data_object)
        return data_objects

    def __parse_object(self, name: str, values: dict) -> DataObject:
        required = {'_xpath', '_xref', '_ref'}
        path_value = required & values.keys()
        if len(path_value) != 1:
            raise ValueError(
                'DataObject must have exactly one of the following elements specified: _path or _ref'
            )

        if '_xpath' in path_value:
            xpath = values['_xpath'].split(self.__path_separator)[-1]
            path = DataQuery.XPath(xpath)
        elif '_xref' in path_value:
            xpath = values['_xref'].split(self.__path_separator)[-1]
            path = DataQuery.XPath(xpath, True)
        else:
            ref = values['_ref'].split(self.__path_separator)[-1]
            path = DataQuery.Reference(ref)

        data_values = []
        for key, value in values.items():
            if key in required:
                continue

            if isinstance(value, dict):
                data_object = self.__parse_object(key, value)
                data_values.append(data_object)
            else:
                data_value = self.__parse_value(key, value)
                data_values.append(data_value)

        return DataObject(name, path, data_values)

    def __parse_value(self, name: str, value: str) -> DataValue:
        try:
            query = self.__parse_query(value)
            return DataValue(name, query)
        except Exception as e:
            raise ValueError(f'Value: {name}') from e

    def __parse_query(self, text: str) -> DataQuery:
        if self.__path_separator not in text:
            path = self.__get_path(text)
            return DataQuery(path)

        raw_value_format, raw_path = text.split(self.__path_separator, 2)
        path = self.__get_path(raw_path)

        if self.__format_separator in raw_value_format:
            raw_value, raw_format = raw_value_format.split(self.__format_separator)
            value = self.__get_value(raw_value)
            format = self.__get_format(raw_format)
        else:
            value = self.__get_value(raw_value_format)
            format = DataQuery.Format.String

        return DataQuery(path, value, format)

    def __get_path(self, path: str) -> Union[DataQuery.XPath, DataQuery.Reference]:
        illegal_character = [self.__path_separator, self.__format_separator]
        if any(c in illegal_character for c in path):
            raise ValueError(f'{path} contains illegal characters [:>]')

        return DataQuery.XPath(path)

    def __get_value(self, value: str) -> str:
        if (value == '') or (value == 'tag') or (value == 'text'):
            return value
        elif value.startswith('@'):
            if len(value) > 1:
                return value
            else:
                raise ValueError(f'attribute names have to be defined')
        else:
            return 'text'

    def __get_format(self, format: str) -> DataQuery.Format:
        if (format == '') or (format == 'string'):
            return DataQuery.Format.String
        elif (format == 'int'):
            return DataQuery.Format.Integer
        elif (format == 'float'):
            return DataQuery.Format.Float
        elif (format == 'date'):
            return DataQuery.Format.Date
        else:
            return DataQuery.Format.String
