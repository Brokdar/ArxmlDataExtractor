from lxml.etree import Element, QName
from typing import Union, List, Any
from tqdm import tqdm
import logging

from arxml_data_extractor.handler import value_handler
from arxml_data_extractor.handler.path_handler import PathHandler
from arxml_data_extractor.asr.asr_parser import AsrParser
from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_object import DataObject
from arxml_data_extractor.query.data_value import DataValue


class ObjectHandler():

    def __init__(self, parser: AsrParser):
        self.logger = logging.getLogger()
        self.path_handler = PathHandler(parser)

    def handle(self, data_object: DataObject, node: Element = None) -> Union[list, dict]:
        is_not_root = True
        if node is None:
            is_not_root = False
            node = self.path_handler.parser.root

        if is_not_root:
            self.logger.info(f'ObjectHandler - handle DataObject(\'{data_object.name}\')')
        else:
            self.logger.info(f'ObjectHandler - [root] handle DataObject(\'{data_object.name}\')')

        values = []
        elements = self.path_handler.elements_by_path(data_object.path, node)
        for element in tqdm(
                elements,
                desc=f'Handle DataObject(\'{data_object.name}\')',
                disable=is_not_root,
                bar_format="{desc:<70}{percentage:3.0f}% |{bar:70}| {n_fmt:>4}/{total_fmt}"):
            if element is not None:
                self.logger.info(
                    f'ObjectHandler - element found: \'{QName(element).localname}\' at line {element.sourceline - 1}'
                )
                values.append(self.__handle_values(data_object.values, element))

        if not values:
            self.logger.warning(
                f'ObjectHandler - no values found for DataObject(\'{data_object.name}\')')
        else:
            self.logger.info(
                f'ObjectHandler - values found for DataObject(\'{data_object.name}\'): {len(values)}'
            )

        return values[0] if len(values) == 1 else values

    def __handle_values(self, values: List[Union[DataValue, DataObject]], node: Element) -> dict:
        results = {}
        for value in values:
            if isinstance(value, DataObject):
                results[value.name] = self.handle(value, node)
            elif isinstance(value, DataValue):
                results[value.name] = self.__handle_value(value.query, node)
                if results[value.name] is None:
                    self.logger.info(
                        f'ObjectHandler - no value found for DataValue(\'{value.name}\')')
                else:
                    self.logger.info(
                        f'ObjectHandler - value found: DataValue(\'{value.name}\') = \'{results[value.name]}\''
                    )
            else:
                error = f'ObjectHandler - invalid value type ({type(value)}). Value must be of type DataObject or DataValue'
                self.logger.error(error)
                raise TypeError(error)

        return results

    def __handle_value(self, query: DataQuery, node: Element) -> Any:
        if isinstance(query.path, DataQuery.XPath):
            if query.path.is_reference:
                element = self.path_handler.element_by_inline_ref(query.path, node)
            else:
                element = self.path_handler.element_by_xpath(query.path.xpath, node)
        else:  # DataQuery.Reference isn't allowed on DataValue
            return None

        if element is None:
            return None

        return value_handler.handle(query, element)
