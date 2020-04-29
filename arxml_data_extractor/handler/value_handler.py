import arrow
import logging
from lxml.etree import Element
from typing import Any, Union

from arxml_data_extractor.query.data_query import DataQuery


def handle(query: DataQuery, node: Element) -> Any:
    value = __get_value(query.value, node)
    if value is None:
        return value
    return __convert_value(value, query.format)


def __get_value(value: str, node: Element) -> Union[str, None]:
    if value == 'text':
        return node.text
    elif value == 'tag':
        return node.tag
    elif value.startswith('@'):
        attribute = value[1:]
        if attribute in node.attrib:
            return node.attrib[attribute]
        logging.getLogger().warning(f'ValueHandler - no attribute found with name \'{attribute}\'')
        return None
    else:
        error = f'ValueHandler - invalid value syntax \'{value}\'. Value must be either \'tag\', \'text\' or \'@..\''
        logging.getLogger().error(error)
        raise Exception(error)


def __convert_value(value: str, format: DataQuery.Format) -> Any:
    try:
        if format == DataQuery.Format.String:
            return value
        elif format == DataQuery.Format.Integer:
            return int(value)
        elif format == DataQuery.Format.Float:
            return float(value)
        elif format == DataQuery.Format.Date:
            return arrow.get(value)
        else:
            logging.getLogger().warning(
                f'ValueHandler - convertion error {value} to {format} -> fallback to string')
            return value
    except Exception as e:
        logging.getLogger().exception(
            f'ValueHandler - error while converting {value} to {format} -> fallback to string', e)
        return value
