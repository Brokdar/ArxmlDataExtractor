import pytest

from arxml_data_extractor.query.data_value import DataValue
from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_object import DataObject
from arxml_data_extractor.query_handler import QueryHandler

arxml = 'arxml_data_extractor/tests/test.arxml'


@pytest.fixture
def only_value():
    return DataValue(
        'CAN Cluster',
        DataQuery(DataQuery.Reference('/Cluster/CAN1'), 'text', DataQuery.Format.String))


@pytest.fixture
def can_object():
    return DataObject('CAN Cluster', DataQuery.Reference('/Cluster/CAN'), [
        DataValue('Name', DataQuery(DataQuery.XPath('./SHORT-NAME'))),
        DataValue(
            'Baudrate',
            DataQuery(
                DataQuery.XPath('CAN-CLUSTER-VARIANTS/CAN-CLUSTER-CONDITIONAL/BAUDRATE'),
                format=DataQuery.Format.Integer)),
        DataValue('Language', DataQuery(DataQuery.XPath('LONG-NAME/L-4'), value='@L')),
        DataValue('Long Name', DataQuery(DataQuery.XPath('LONG-NAME/L-4')))
    ])


def test_invalid_file_raises_value_error():
    with pytest.raises(ValueError):
        query_handler = QueryHandler()
        query_handler.find_values('test.json', [])


def test_config_must_have_root_object(only_value):
    data_objects = [only_value]
    query_handler = QueryHandler()

    with pytest.raises(TypeError):
        query_handler.find_values(arxml, data_objects)


def test_find_object_by_reference(can_object):
    data_objects = [can_object]
    query_handler = QueryHandler()

    data_results = query_handler.find_values(arxml, data_objects)

    assert isinstance(data_results, dict)
    assert 'CAN Cluster' in data_results
    can_cluster = data_results['CAN Cluster']
    assert isinstance(can_cluster, dict)
    assert can_cluster['Name'] == 'CAN'
    assert can_cluster['Baudrate'] == 500000
    assert can_cluster['Language'] == 'FOR-ALL'
    assert can_cluster['Long Name'] == 'CAN Channel 1'


def test_raises_value_error_if_reference_not_found(only_value):
    data_object = DataObject('CAN Cluster', DataQuery.Reference('/Cluster/CAN1'),
                             [DataValue('Name', DataQuery(DataQuery.XPath('./SHORT-NAME')))])

    query_handler = QueryHandler()

    with pytest.raises(ValueError):
        query_handler.find_values(arxml, [data_object])


def test_raises_value_error_if_no_element_found_with_xpath():
    data_object = DataObject('CAN Cluster', DataQuery.Reference('/Cluster/CAN'),
                             [DataValue('Name', DataQuery(DataQuery.XPath('/SHORT-NAME')))])

    query_handler = QueryHandler()

    with pytest.raises(ValueError):
        query_handler.find_values(arxml, [data_object])


def test_raises_value_error_if_no_attribute_found_with_specified_name():
    data_object = DataObject('CAN Cluster', DataQuery.Reference('/Cluster/CAN'),
                             [DataValue('UUID', DataQuery(DataQuery.XPath('.'), value='@S'))])

    query_handler = QueryHandler()

    with pytest.raises(ValueError):
        query_handler.find_values(arxml, [data_object])