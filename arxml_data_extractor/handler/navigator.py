from lxml.etree import Element
from typing import Union, List, Tuple

from arxml_data_extractor.asr.asr_parser import AsrParser
from arxml_data_extractor.query.data_query import DataQuery


class Navigator():

    def __init__(self, parser: AsrParser):
        self.parser = parser

    def elements_by_path(self, path: Union[DataQuery.XPath, DataQuery.Reference],
                         node: Element) -> List[Element]:
        if isinstance(path, DataQuery.XPath):
            elements = self.elements_by_xpath(path.xpath, node)
            if not elements:
                raise ValueError(f'No elements found with: {path.xpath}')

            if path.is_reference is False:
                return elements

            if len(elements) != 1:
                raise Exception(f'Too many references found with: {path.xpath}')
            return [self.element_by_ref(elements[0].text)]

        elif isinstance(path, DataQuery.Reference):
            return [self.element_by_ref(path.ref)]
        else:
            raise TypeError(
                f'Unexpected error while finding elements with path of type: {type(path)}')

    def elements_by_xpath(self, path: str, node: Element) -> List[Element]:
        xpath = self.parser.assemble_xpath(path)
        return self.parser.find(node, xpath)

    def element_by_xpath(self, path: str, node: Element) -> Element:
        element = next(iter(self.elements_by_xpath(path, node)), None)
        if element is None:
            raise ValueError(f'No element found with XPath: {path}')
        return element

    def element_by_ref(self, ref: str) -> Element:
        element = self.parser.find_reference(ref)
        if element is None:
            raise ValueError(f'No reference found with: {ref}')
        return element

    def element_by_inline_ref(self, path: DataQuery.XPath, node: Element) -> Element:
        path_to_reference, path_to_value = self.__split(path.xpath)

        reference = self.element_by_xpath(path_to_reference, node)
        if 'REF' not in reference.tag:
            raise ValueError(f'No reference found at "{path.xpath}')

        referred_element = self.element_by_ref(reference.text)
        return self.element_by_xpath(path_to_value, referred_element)

    def __split(self, inline_ref: str) -> Tuple[str, str]:
        start_inline_ref = '&('
        if not inline_ref.startswith(start_inline_ref):
            raise ValueError(
                'Specified inline reference XPath contains invalid syntax. "&(<path-to-element>)<path-to-value>"'
            )

        parantheses_count = 1
        path_to_value = path_to_reference = None
        ref_start_idx = len(start_inline_ref)
        for i, c in enumerate(inline_ref[ref_start_idx:], ref_start_idx):
            if c == '(':
                parantheses_count += 1
            elif c == ')':
                parantheses_count -= 1
                if parantheses_count == 0:
                    path_to_reference = inline_ref[ref_start_idx:i]
                    path_to_value = inline_ref[i + 1:]
                    break
        if path_to_value is None or path_to_reference is None:
            raise Exception(f'Mismatching parantheses in "{inline_ref}"')

        return path_to_reference, path_to_value
