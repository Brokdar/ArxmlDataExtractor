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
def simple_object_by_ref():
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


@pytest.fixture
def complex_object_by_ref():
    return DataObject('CAN Cluster', DataQuery.Reference('/Cluster/CAN'), [
        DataValue('Name', DataQuery(DataQuery.XPath('./SHORT-NAME'))),
        DataValue(
            'Baudrate',
            DataQuery(
                DataQuery.XPath('CAN-CLUSTER-VARIANTS/CAN-CLUSTER-CONDITIONAL/BAUDRATE'),
                format=DataQuery.Format.Integer)),
        DataObject('Long Name', DataQuery.XPath('LONG-NAME/L-4'), [
            DataValue('Language', DataQuery(DataQuery.XPath('.'), value='@L')),
            DataValue('Name', DataQuery(DataQuery.XPath('.')))
        ])
    ])


@pytest.fixture
def simple_object_by_xpath():
    return DataObject('CAN Cluster', DataQuery.XPath('.//AR-PACKAGE/ELEMENTS/CAN-CLUSTER'), [
        DataValue('Name', DataQuery(DataQuery.XPath('./SHORT-NAME'))),
        DataValue(
            'Baudrate',
            DataQuery(
                DataQuery.XPath('CAN-CLUSTER-VARIANTS/CAN-CLUSTER-CONDITIONAL/BAUDRATE'),
                format=DataQuery.Format.Integer)),
        DataValue('Language', DataQuery(DataQuery.XPath('LONG-NAME/L-4'), value='@L')),
        DataValue('Long Name', DataQuery(DataQuery.XPath('LONG-NAME/L-4')))
    ])


@pytest.fixture
def complex_object_by_xpath():
    return DataObject('CAN Cluster', DataQuery.XPath('.//CAN-CLUSTER'), [
        DataValue('Name', DataQuery(DataQuery.XPath('./SHORT-NAME'))),
        DataValue(
            'Baudrate',
            DataQuery(
                DataQuery.XPath('CAN-CLUSTER-VARIANTS/CAN-CLUSTER-CONDITIONAL/BAUDRATE'),
                format=DataQuery.Format.Integer)),
        DataObject('Long Name', DataQuery.XPath('LONG-NAME/L-4'), [
            DataValue('Language', DataQuery(DataQuery.XPath('.'), value='@L')),
            DataValue('Name', DataQuery(DataQuery.XPath('.')))
        ])
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


def test_find_object_by_reference(simple_object_by_ref):
    data_objects = [simple_object_by_ref]
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


def test_find_complex_object_by_reference(complex_object_by_ref):
    data_objects = [complex_object_by_ref]
    query_handler = QueryHandler()

    data_results = query_handler.find_values(arxml, data_objects)

    assert isinstance(data_results, dict)
    assert 'CAN Cluster' in data_results
    can_cluster = data_results['CAN Cluster']
    assert isinstance(can_cluster, dict)
    assert can_cluster['Name'] == 'CAN'
    assert can_cluster['Baudrate'] == 500000
    assert 'Long Name' in can_cluster
    long_name = can_cluster['Long Name']
    assert long_name['Language'] == 'FOR-ALL'
    assert long_name['Name'] == 'CAN Channel 1'


def test_find_simple_object_by_xpath(simple_object_by_xpath):
    data_objects = [simple_object_by_xpath]
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


def test_find_complex_object_by_xpath(complex_object_by_xpath):
    data_objects = [complex_object_by_xpath]
    query_handler = QueryHandler()

    data_results = query_handler.find_values(arxml, data_objects)

    assert isinstance(data_results, dict)
    assert 'CAN Cluster' in data_results
    can_cluster = data_results['CAN Cluster']
    assert isinstance(can_cluster, dict)
    assert can_cluster['Name'] == 'CAN'
    assert can_cluster['Baudrate'] == 500000
    assert 'Long Name' in can_cluster
    long_name = can_cluster['Long Name']
    assert long_name['Language'] == 'FOR-ALL'
    assert long_name['Name'] == 'CAN Channel 1'