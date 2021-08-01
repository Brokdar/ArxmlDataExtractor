import re

from lxml import etree
from typing import Union


class AsrParser():
    """Provides parsing functions for navigating within an ARXML file.
    """

    def __init__(self, arxml: str):
        parser = etree.XMLParser(remove_blank_text=True)
        self.__tree = etree.parse(arxml, parser)
        self.__root = self.tree.getroot()

        # get namespace from arxml file
        AsrParser.ns = {'ar': self.__root.nsmap[None]}

        self._packages = {
            AsrParser.get_shortname(element): element
            for element in self.find_all_elements('AUTOSAR/AR-PACKAGES/AR-PACKAGE')
        }

    @property
    def tree(self):
        return self.__tree

    @property
    def root(self):
        return self.__root

    @property
    def packages(self):
        return self._packages

    def find_all_elements(self, path: str) -> list:
        """Finds all elements specified by the XML element path. The path can
        either be a simple element name, a complex xml path with namespaces
        or a combination of both.

        Arguments:
            element_path {str} -- element name, XML element path or a combination

        Returns:
            list -- all found elements reachable with the specified element path
        """
        xpath = AsrParser.__assemble_xpath(path)
        return AsrParser.find(self.root, '//' + xpath)

    def find_reference(self, reference: str) -> etree.Element:
        """Tries to find the element described by the AUTOSAR reference

        Arguments:
            reference {str} -- AUTOSAR reference

        Returns:
            etree.Element -- xml element node or None
        """
        ref_parts = reference.split('/')
        if (reference.startswith('/')):
            ref_parts = ref_parts[1:]

        element = self.packages[ref_parts[0]]
        if (element is None):
            return None

        for i in range(1, len(ref_parts)):
            xpath = f'.//*/ar:SHORT-NAME[text()="{ref_parts[i]}"]/..'
            element = AsrParser.__first(AsrParser.find(element, xpath))
            if (element is None):
                return None

        return element

    @staticmethod
    def __append_namespace(path: str) -> str:
        if (path.startswith('ar:')):
            return path
        return 'ar:' + path

    @classmethod
    def __assemble_xpath(cls, path: str) -> str:
        if ('/' in path):
            return '/'.join([cls.__append_namespace(part) for part in path.split('/')])

        return AsrParser.__append_namespace(path)

    @staticmethod
    def __first(list: list):
        return next(iter(list or []), None)

    @staticmethod
    def find(base: etree.Element, xpath: Union[str, etree.XPath]) -> list:
        """Evaluates an XPath expression on the given base element

        Arguments:
            base {etree.Element} -- base element, starting point
            xpath {str} -- XPath expression defined by W3C consortium

        Returns:
            list -- results of XPath evaluation
        """
        if isinstance(xpath, etree.XPath):
            return xpath(base)
        return base.xpath(xpath, namespaces=AsrParser.ns)

    @classmethod
    def find_elements(cls, base: etree.Element, path: str) -> list:
        """Finds all child elements of the given base element defined by the given Element structure

        Arguments:
            base {etree.Element} -- base element, starting point
            path {str} -- XML element structure with or without namespace

        Returns:
            list -- found elements or empty list
        """
        xpath = cls.__assemble_xpath(path)
        return cls.find(base, './/' + xpath)

    @classmethod
    def find_first_element(cls,
                           base: etree.Element,
                           path: str,
                           attribute: str = None,
                           text: str = None) -> etree.Element:

        elements = cls.find_elements(base, path)
        return cls.__first(elements)

    @classmethod
    def find_element_by_shortname(cls, base: etree.Element, path: str, name: str) -> etree.Element:
        """Finds the element of specified type with the provided name

        Arguments:
            base {etree.Element} -- base element, starting point
            path {str} -- element name, XML element path or a combination
            name {str} -- shortname of the element

        Returns:
            etree.Element -- found element or None
        """
        xpath = cls.__assemble_xpath(path)
        xpath = xpath + f'/ar:SHORT-NAME[text()="{name}"]/..'
        return cls.__first(cls.find(base, './/' + xpath))

    @classmethod
    def get_shortname(cls, element: etree.Element) -> Union[str, None]:
        """Gets the shortname of an element

        Arguments:
            element {etree.Element} -- xml element with shortname

        Returns:
            str -- shortname if found otherwise None
        """
        return cls.__first(cls.find(element, 'ar:SHORT-NAME/text()'))

    @staticmethod
    def assemble_xpath(path: str) -> str:
        xpath = re.sub(r"([\/]+)(?!$)", r'\1ar:', path)
        if xpath.startswith('/') or xpath.startswith('.'):
            return xpath
        else:
            return 'ar:' + xpath
