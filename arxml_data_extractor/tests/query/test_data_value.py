import pytest

from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_value import DataValue


@pytest.mark.parametrize("name, query", [
    ('Signal', DataQuery(DataQuery.XPath('/SHORT-NAME'))),
    ('Signal123', DataQuery(DataQuery.XPath('/SHORT-NAME'))),
    ('Signal_123', DataQuery(DataQuery.XPath('/SHORT-NAME'))),
    ('Signal 123', DataQuery(DataQuery.XPath('/SHORT-NAME'))),
])
def test_create_data_value(name, query):
    value = DataValue(name, query)

    assert value.name == name
    assert value.query == query


def test_none_query_raises_exception():
    with pytest.raises(Exception):
        DataValue('name', None)
