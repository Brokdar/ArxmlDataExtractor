from arxml_data_extractor.query.data_query import DataQuery


class DataValue:

    def __init__(self, name: str, query: DataQuery):
        self.name = name
        if (query is None):
            raise Exception('query cannot be of type None')
        self.query = query