from arxml_data_extractor.config_provider import ConfigProvider
from arxml_data_extractor.query_builder import QueryBuilder
from arxml_data_extractor.query_handler import QueryHandler

arxml = 'arxml_data_extractor/tests/test.arxml'


def test_extracting_simple_object():
    yaml = """
    'CAN Cluster':
        '_ref': '/Cluster/CAN'
        'Name': 'SHORT-NAME'
        'Baudrate': 'text>int:CAN-CLUSTER-VARIANTS/CAN-CLUSTER-CONDITIONAL/BAUDRATE'
        'Long Name': 'text:LONG-NAME/L-4'
        'Language': '@L:LONG-NAME/L-4'
    """

    config_provider = ConfigProvider()
    config = config_provider.parse(yaml)

    query_builder = QueryBuilder()
    queries = query_builder.build(config)

    query_handler = QueryHandler()
    data = query_handler.handle_queries(arxml, queries)

    assert isinstance(data, dict)
    assert data['CAN Cluster']['Name'] == 'CAN'
    assert data['CAN Cluster']['Baudrate'] == 500000
    assert data['CAN Cluster']['Long Name'] == 'CAN Channel 1'
    assert data['CAN Cluster']['Language'] == 'FOR-ALL'


def test_extracting_nested_objects():
    yaml = """
    'PDUs':
        '_xpath': './/I-SIGNAL-I-PDU'
        'Name': 'text:SHORT-NAME'
        'Length': 'text>int:LENGTH'
        'Cyclic Timing': 'text>float:.//TRANSMISSION-MODE-TRUE-TIMING/CYCLIC-TIMING/TIME-PERIOD/VALUE'
        'Signal Mappings':
            '_xpath': './/I-SIGNAL-TO-I-PDU-MAPPING'
            'Signal': 'SHORT-NAME'
            'Start Position': 'text>int:START-POSITION'
            'ISignal':
                '_xref': 'I-SIGNAL-REF'
                'Init Value': 'text>int:.//VALUE'
                'Length': 'text>int:LENGTH'
    """
    config_provider = ConfigProvider()
    config = config_provider.parse(yaml)

    query_builder = QueryBuilder()
    queries = query_builder.build(config)

    query_handler = QueryHandler()
    data = query_handler.handle_queries(arxml, queries)

    assert isinstance(data, dict)
    assert len(data['PDUs']) == 2
    assert data['PDUs'][0]['Name'] == 'TxMessage'
    assert data['PDUs'][0]['Length'] == 5
    assert data['PDUs'][0]['Cyclic Timing'] == 0.1
    assert data['PDUs'][0]['Signal Mappings']['Signal'] == 'Signal1'
    assert data['PDUs'][0]['Signal Mappings']['Start Position'] == 0
    assert data['PDUs'][0]['Signal Mappings']['ISignal']['Init Value'] == 128
    assert data['PDUs'][0]['Signal Mappings']['ISignal']['Length'] == 5

    assert data['PDUs'][1]['Name'] == 'RxMessage'
    assert data['PDUs'][1]['Length'] == 2
    assert data['PDUs'][1]['Cyclic Timing'] == 0.1
    assert data['PDUs'][1]['Signal Mappings'][0]['Signal'] == 'Signal2'
    assert data['PDUs'][1]['Signal Mappings'][0]['Start Position'] == 0
    assert data['PDUs'][1]['Signal Mappings'][0]['ISignal']['Init Value'] == 0
    assert data['PDUs'][1]['Signal Mappings'][0]['ISignal']['Length'] == 1
    assert data['PDUs'][1]['Signal Mappings'][1]['Signal'] == 'Signal3'
    assert data['PDUs'][1]['Signal Mappings'][1]['Start Position'] == 1
    assert data['PDUs'][1]['Signal Mappings'][1]['ISignal']['Init Value'] == 0
    assert data['PDUs'][1]['Signal Mappings'][1]['ISignal']['Length'] == 1
