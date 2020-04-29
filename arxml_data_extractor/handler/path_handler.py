from lxml.etree import Element
from typing import Union, List, Tuple
import logging

from arxml_data_extractor.asr.asr_parser import AsrParser
from arxml_data_extractor.query.data_query import DataQuery


class PathHandler():

    def __init__(self, parser: AsrParser):
        self.logger = logging.getLogger()
        self.parser = parser

    def elements_by_path(self, path: Union[DataQuery.XPath, DataQuery.Reference],
                         node: Element) -> Union[List[Element], None]:
        if isinstance(path, DataQuery.XPath):
            elements = self.elements_by_xpath(path.xpath, node)
            if not elements:
                self.logger.warning(f'PathHandler - no elements found with XPath \'{path.xpath}\'')
                return elements

            if path.is_reference is False:
                return elements

            if len(elements) != 1:
                error = f'PathHandler - too many references found with XPath \'{path.xpath}\''
                self.logger.error(error)
                raise Exception(error)
            return [self.element_by_ref(elements[0].text)]

        elif isinstance(path, DataQuery.Reference):
            return [self.element_by_ref(path.ref)]
        else:
            error = f'PathHandler - invalid path type (type: {type(path)}). Path must be of type DataQuery.XPath or DataQuery.Reference'
            self.logger.error(error)
            raise TypeError(error)

    def elements_by_xpath(self, path: str, node: Element) -> List[Element]:
        xpath = self.parser.assemble_xpath(path)
        return self.parser.find(node, xpath)

    def element_by_xpath(self, path: str, node: Element) -> Union[Element, None]:
        element = next(iter(self.elements_by_xpath(path, node)), None)
        if element is None:
            self.logger.warning(f'PathHandler - no element found with XPath \'{path}\'')
            return None
        return element

    def element_by_ref(self, ref: str) -> Union[Element, None]:
        element = self.parser.find_reference(ref)
        if element is None:
            self.logger.warning(f'PathHandler - no element found with reference \'{ref}\'')
            return None
        return element

    def element_by_inline_ref(self, path: DataQuery.XPath, node: Element) -> Union[Element, None]:
        path_to_reference, path_to_value = self.__split(path.xpath)

        reference = self.element_by_xpath(path_to_reference, node)
        if 'REF' not in reference.tag:
            self.logger.warning(
                f'PathHandler - processing inline reference, no reference found at \'{path.xpath}\''
            )
            return None

        referred_element = self.element_by_ref(reference.text)
        return self.element_by_xpath(path_to_value, referred_element)

    def __split(self, inline_ref: str) -> Tuple[str, str]:
        start_inline_ref = '&('
        if not inline_ref.startswith(start_inline_ref):
            error = f'PathHandler - invalid inline reference syntax \'{inline_ref}\'. Syntax: \'&(<path-to-element>)<path-to-value>\''
            self.logger.error(error)
            raise ValueError(error)

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
            error = f'PathHandler - mismatching parantheses in inline reference \'{inline_ref}\''
            self.logger.error(error)
            raise ValueError(error)

        return path_to_reference, path_to_value
