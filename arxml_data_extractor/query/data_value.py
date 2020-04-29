import logging

from arxml_data_extractor.query.data_query import DataQuery


class DataValue:

    def __init__(self, name: str, query: DataQuery):
        self.name = name
        self.logger = logging.getLogger()
        if (query is None):
            error = f'DataValue(\'{self.name}\') - invalid query type ({type(query)}). Query must be of type DataQuery'
            self.logger.error(error)
            raise TypeError(error)
        self.query = query
