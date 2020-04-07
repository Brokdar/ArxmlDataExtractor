from typing import List, Union, Any
from lxml.etree import Element

from arxml_data_extractor.asr.asr_parser import AsrParser
from arxml_data_extractor.query.data_object import DataObject
from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_value import DataValue


class QueryHandler():

    def find_values(self, file: str, data_objects: List[DataObject]) -> dict:
        if not file.endswith('.arxml'):
            raise ValueError(f'{file} is not of type ".arxml"')

        self.asr_parser = AsrParser(file)

        results = {}
        for data_object in data_objects:
            if (not isinstance(data_object, DataObject)):
                raise TypeError(
                    f'Root element must be of type DataObject: currently -> {type(data_object)}')

            results[data_object.name] = self.__parse_data_object(data_object)

        return results

    def __parse_data_object(self,
                            data_object: DataObject,
                            node: Element = None) -> Union[list, dict]:
        if node is None:
            node = self.asr_parser.root

        values = []
        elements = self.__get_elements_by_path(data_object.path, node)
        for element in elements:
            values.append(self.__parse_data_values(data_object.values, element))

        return values[0] if len(values) == 1 else values

    def __get_elements_by_path(self, path: Union[DataQuery.XPath, DataQuery.Reference],
                               node: Element) -> List[Element]:
        if isinstance(path, DataQuery.XPath):
            xpath = self.asr_parser.assemble_xpath(path.xpath)
            elements = self.asr_parser.find(node, xpath)

            if path.is_reference is False:
                return elements

            if elements:
                ref = elements[0].text
                return [self.__get_element_by_ref(ref)]
            else:
                raise ValueError(f'Unable to find referenced element with path: {path.xpath}')

        elif isinstance(path, DataQuery.Reference):
            return [self.__get_element_by_ref(path.ref)]
        else:
            raise TypeError(
                f'Unexpected error while finding elements with path of type: {type(path)}')

    def __get_element_by_ref(self, ref: str) -> Element:
        element = self.asr_parser.find_reference(ref)
        if element is None:
            raise ValueError(f'No reference found with "{ref}"')
        return element

    def __parse_data_values(self, values: List[Union[DataValue, DataObject]],
                            node: Element) -> dict:
        results = {}
        for value in values:
            if isinstance(value, DataObject):
                results[value.name] = self.__parse_data_object(value, node)
            else:
                results[value.name] = self.__parse_data_value(value.query, node)

        return results

    def __parse_data_value(self, query: DataQuery, node: Element) -> Any:
        if isinstance(query.path, DataQuery.XPath):
            xpath = self.asr_parser.assemble_xpath(query.path.xpath)
            element = next(iter(self.asr_parser.find(node, xpath)), None)
            if element is None:
                raise ValueError(f'No Element found with XPath "{query.path.xpath}"')
        else:
            return None

        value = self.__get_value(query.value, element)
        return self.__convert_value(value, query.format)

    def __get_value(self, value: str, node: Element) -> str:
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
            raise Exception(f'Unexpected error while parsing value: {value}')

    def __convert_value(self, value: str, format: DataQuery.Format):
        if format == DataQuery.Format.String:
            return value
        elif format == DataQuery.Format.Integer:
            return int(value)
        elif format == DataQuery.Format.Float:
            return float(value)
        elif format == DataQuery.Format.Date:
            pass
        else:
            raise Exception(f'Unexpected error while converting {value} -> {format}')
