from typing import List
from pathlib import Path

from arxml_data_extractor.asr.asr_parser import AsrParser
from arxml_data_extractor.handler.object_handler import ObjectHandler
from arxml_data_extractor.query.data_object import DataObject

from tqdm import tqdm


class QueryHandler():

    def handle_queries(self, input: str, queries: List[DataObject]) -> dict:
        arxml = Path(input)
        if not arxml.exists:
            raise ValueError(f'{input} does not exit.')
        if not arxml.is_file:
            raise ValueError(f'{input} is not a file.')
        if arxml.suffix != '.arxml':
            raise ValueError(f'{input} is not of type ".arxml"')

        object_handler = ObjectHandler(AsrParser(str(arxml)))

        results = {}
        for data_object in tqdm(queries, desc='Handle Queries'):
            if (not isinstance(data_object, DataObject)):
                raise TypeError(
                    f'Root element must be of type DataObject: currently -> {type(data_object)}')

            results[data_object.name] = object_handler.handle(data_object)

        return results
