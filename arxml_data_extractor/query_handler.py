from typing import List
from pathlib import Path
import logging

from arxml_data_extractor.asr.asr_parser import AsrParser
from arxml_data_extractor.handler.object_handler import ObjectHandler
from arxml_data_extractor.query.data_object import DataObject

from tqdm import tqdm


class QueryHandler():

    def __init__(self):
        self.logger = logging.getLogger()

    def handle_queries(self, input: str, queries: List[DataObject]) -> dict:
        arxml = Path(input)
        if not arxml.exists:
            error = f'QueryHandler - input file doesn\'t exist \'{input}\''
            self.logger.error(error)
            raise ValueError(error)
        if not arxml.is_file:
            error = f'QueryHandler - input is not a file \'{input}\''
            self.logger.error(error)
            raise ValueError(error)
        if arxml.suffix != '.arxml':
            error = f'QueryHandler - invalid input file extension \'{arxml.suffix}\' != \'.arxml\''
            self.logger.error(error)
            raise ValueError(error)

        object_handler = ObjectHandler(AsrParser(str(arxml)))

        results = {}
        for data_object in tqdm(queries, desc='Handle Queries'):
            if (not isinstance(data_object, DataObject)):
                error = f'QueryHandler - invalid root element type \'{type(data_object)}\' != \'DataObject\''
                self.logger.error(error)
                raise TypeError(error)

            results[data_object.name] = object_handler.handle(data_object)

        return results
