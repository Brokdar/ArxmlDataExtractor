import arrow
from lxml.etree import Element
from typing import Any

from arxml_data_extractor.query.data_query import DataQuery


def handle(query: DataQuery, node: Element) -> Any:
    value = __get_value(query.value, node)
    return __convert_value(value, query.format)


def __get_value(value: str, node: Element) -> str:
    if value == 'text':
        return node.text
    elif value == 'tag':
        return node.tag
    elif value.startswith('@'):
        attribute = value[1:]
        if attribute in node.attrib:
            return node.attrib[attribute]
        raise ValueError(f'No attribute found with name {attribute}')
    else:
        raise Exception(f'Unexpected error while parsing value at: {value}')


def __convert_value(value: str, format: DataQuery.Format) -> Any:
    if format == DataQuery.Format.String:
        return value
    elif format == DataQuery.Format.Integer:
        return int(value)
    elif format == DataQuery.Format.Float:
        return float(value)
    elif format == DataQuery.Format.Date:
        return arrow.get(value)
    else:
        raise Exception(f'Unexpected error while converting {value} -> {format}')
