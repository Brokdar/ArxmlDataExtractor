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


@pytest.fixture
def multi_value_complex_object():
    return DataObject('PDUs', DataQuery.XPath('.//I-SIGNAL-I-PDU'), [
        DataValue('Name', DataQuery(DataQuery.XPath('SHORT-NAME'))),
        DataValue('Length', DataQuery(DataQuery.XPath('LENGTH'), format=DataQuery.Format.Integer)),
        DataValue(
            'Unused Bit Pattern',
            (DataQuery(DataQuery.XPath('UNUSED-BIT-PATTERN'), format=DataQuery.Format.Integer))),
        DataObject('Timing Specification', DataQuery.XPath('./*/I-PDU-TIMING'), [
            DataValue('Minimum Delay',
                      DataQuery(DataQuery.XPath('MINIMUM-DELAY'), format=DataQuery.Format.Integer)),
            DataValue(
                'Cyclic Timing',
                DataQuery(
                    DataQuery.XPath(
                        'TRANSMISSION-MODE-DECLARATION/TRANSMISSION-MODE-TRUE-TIMING/CYCLIC-TIMING/TIME-PERIOD/VALUE'
                    ),
                    format=DataQuery.Format.Float))
        ]),
        DataObject('Signal Mappings', DataQuery.XPath('.//I-SIGNAL-TO-I-PDU-MAPPING'), [
            DataValue('Signal Name', DataQuery(DataQuery.XPath('SHORT-NAME'))),
            DataValue('Start Position',
                      DataQuery(DataQuery.XPath('START-POSITION'),
                                format=DataQuery.Format.Integer)),
            DataValue('Transfer Property', DataQuery(DataQuery.XPath('TRANSFER-PROPERTY'))),
            DataObject('Signal', DataQuery.XPath('I-SIGNAL-REF', is_reference=True), [
                DataValue('Init Value',
                          DataQuery(DataQuery.XPath('.//VALUE'), format=DataQuery.Format.Integer)),
                DataValue('Length',
                          DataQuery(DataQuery.XPath('LENGTH'), format=DataQuery.Format.Integer))
            ])
        ])
    ])


def test_find_object_by_reference(simple_object_by_ref):
    data_objects = [simple_object_by_ref]
    query_handler = QueryHandler()

    data_results = query_handler.handle_queries(arxml, data_objects)

    assert isinstance(data_results, dict)
    assert 'CAN Cluster' in data_results
    can_cluster = data_results['CAN Cluster']
    assert isinstance(can_cluster, dict)
    assert can_cluster['Name'] == 'CAN'
    assert can_cluster['Baudrate'] == 500000
    assert can_cluster['Language'] == 'FOR-ALL'
    assert can_cluster['Long Name'] == 'CAN Channel 1'


def test_find_complex_object_by_reference(complex_object_by_ref):
    data_objects = [complex_object_by_ref]
    query_handler = QueryHandler()

    data_results = query_handler.handle_queries(arxml, data_objects)

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

    data_results = query_handler.handle_queries(arxml, data_objects)

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

    data_results = query_handler.handle_queries(arxml, data_objects)

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


def test_find_all_objects_by_xpath(multi_value_complex_object):
    data_objects = [multi_value_complex_object]
    query_handler = QueryHandler()

    data_results = query_handler.handle_queries(arxml, data_objects)

    assert isinstance(data_results, dict)
    assert 'PDUs' in data_results
    pdus = data_results['PDUs']
    assert isinstance(pdus, list)
    assert len(pdus) == 2
    assert isinstance(pdus[0], dict)
    assert pdus[0]['Name'] == 'TxMessage'
    assert pdus[0]['Length'] == 5
    assert pdus[0]['Unused Bit Pattern'] == 0
    assert pdus[0]['Timing Specification']['Minimum Delay'] == 0
    assert pdus[0]['Timing Specification']['Cyclic Timing'] == 0.1
    assert pdus[0]['Signal Mappings']['Signal Name'] == 'Signal1'
    assert pdus[0]['Signal Mappings']['Start Position'] == 0
    assert pdus[0]['Signal Mappings']['Transfer Property'] == 'PENDING'
    assert pdus[0]['Signal Mappings']['Signal']['Init Value'] == 128
    assert pdus[0]['Signal Mappings']['Signal']['Length'] == 5

    assert isinstance(pdus[1], dict)
    assert pdus[1]['Name'] == 'RxMessage'
    assert pdus[1]['Length'] == 2
    assert pdus[1]['Unused Bit Pattern'] == 0
    assert pdus[1]['Timing Specification']['Minimum Delay'] == 0
    assert pdus[1]['Timing Specification']['Cyclic Timing'] == 0.1
    assert pdus[1]['Signal Mappings'][0]['Signal Name'] == 'Signal2'
    assert pdus[1]['Signal Mappings'][0]['Start Position'] == 0
    assert pdus[1]['Signal Mappings'][0]['Transfer Property'] == 'PENDING'
    assert pdus[1]['Signal Mappings'][0]['Signal']['Init Value'] == 0
    assert pdus[1]['Signal Mappings'][0]['Signal']['Length'] == 1
    assert pdus[1]['Signal Mappings'][1]['Signal Name'] == 'Signal3'
    assert pdus[1]['Signal Mappings'][1]['Start Position'] == 1
    assert pdus[1]['Signal Mappings'][1]['Transfer Property'] == 'PENDING'
    assert pdus[1]['Signal Mappings'][1]['Signal']['Init Value'] == 0
    assert pdus[1]['Signal Mappings'][1]['Signal']['Length'] == 1


def test_handle_inline_reference():
    data_object = DataObject('SignalMapping', DataQuery.Reference('/PDU/TxMessage'), [
        DataValue(
            'Name',
            DataQuery(
                DataQuery.XPath(
                    '&(I-SIGNAL-TO-PDU-MAPPINGS/I-SIGNAL-TO-I-PDU-MAPPING/I-SIGNAL-REF)SHORT-NAME',
                    True)))
    ])

    query_handler = QueryHandler()
    results = query_handler.handle_queries(arxml, [data_object])

    assert isinstance(results, dict)
    assert isinstance(results['SignalMapping'], dict)
    assert results['SignalMapping']['Name'] == 'Signal1'


def test_invalid_file_raises_value_error():
    with pytest.raises(ValueError):
        query_handler = QueryHandler()
        query_handler.handle_queries('test.json', [])


def test_config_must_have_root_object(only_value):
    data_objects = [only_value]
    query_handler = QueryHandler()

    with pytest.raises(TypeError):
        query_handler.handle_queries(arxml, data_objects)


def test_returns_none_value_if_reference_not_found(only_value):
    data_object = DataObject('CAN Cluster', DataQuery.Reference('/Cluster/CAN1'),
                             [DataValue('Name', DataQuery(DataQuery.XPath('./SHORT-NAME')))])

    query_handler = QueryHandler()
    result = query_handler.handle_queries(arxml, [data_object])

    assert result['CAN Cluster'] == []


def test_returns_none_value_if_no_element_found_with_xpath():
    data_object = DataObject('CAN Cluster', DataQuery.Reference('/Cluster/CAN'),
                             [DataValue('Name', DataQuery(DataQuery.XPath('/SHORT-NAME')))])

    query_handler = QueryHandler()
    result = query_handler.handle_queries(arxml, [data_object])

    assert isinstance(result['CAN Cluster'], dict)
    assert result['CAN Cluster']['Name'] is None


def test_returns_none_value_if_no_attribute_found_with_specified_name():
    data_object = DataObject('CAN Cluster', DataQuery.Reference('/Cluster/CAN'),
                             [DataValue('UUID', DataQuery(DataQuery.XPath('.'), value='@S'))])

    query_handler = QueryHandler()
    result = query_handler.handle_queries(arxml, [data_object])

    assert isinstance(result['CAN Cluster'], dict)
    assert result['CAN Cluster']['UUID'] is None
