from lxml.etree import Element
from typing import Union, List, Any

from arxml_data_extractor.handler import value_handler
from arxml_data_extractor.handler.navigator import Navigator
from arxml_data_extractor.asr.asr_parser import AsrParser
from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_object import DataObject
from arxml_data_extractor.query.data_value import DataValue


class ObjectHandler():

    def __init__(self, parser: AsrParser):
        self.navigator = Navigator(parser)

    def handle(self, data_object: DataObject, node: Element = None) -> Union[list, dict]:
        if node is None:
            node = self.navigator.parser.root

        values = []
        elements = self.navigator.elements_by_path(data_object.path, node)
        for element in elements:
            values.append(self.__handle_values(data_object.values, element))

        return values[0] if len(values) == 1 else values

    def __handle_values(self, values: List[Union[DataValue, DataObject]], node: Element) -> dict:
        results = {}
        for value in values:
            if isinstance(value, DataObject):
                results[value.name] = self.handle(value, node)
            elif isinstance(value, DataValue):
                results[value.name] = self.__handle_value(value.query, node)
            else:
                raise TypeError(f'Unexpected value type: {type(value)}')

        return results

    def __handle_value(self, query: DataQuery, node: Element) -> Any:
        if isinstance(query.path, DataQuery.XPath):
            if query.path.is_reference:
                element = self.navigator.element_by_inline_ref(query.path, node)
            else:
                element = self.navigator.element_by_xpath(query.path.xpath, node)
        else:  # DataQuery.Reference isn't allowed on DataValue
            return None

        return value_handler.handle(query, element)
