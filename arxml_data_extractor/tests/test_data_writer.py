import pytest
from pathlib import Path

from arxml_data_extractor.data_writer import DataWriter
from arxml_data_extractor.query.data_value import DataValue
from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_object import DataObject


@pytest.fixture
def query():
    return [
        DataObject('PDU', DataQuery.XPath('.//I-SIGNAL-I-PDU'), [
            DataValue('Name', DataQuery(DataQuery.XPath('SHORT-NAME'))),
            DataValue('Length', DataQuery(
                DataQuery.XPath('LENGTH'), format=DataQuery.Format.Integer)),
            DataValue(
                'Cyclic Timing',
                DataQuery(
                    DataQuery.XPath(
                        './*/I-PDU-TIMING/TRANSMISSION-MODE-DECLARATION/TRANSMISSION-MODE-TRUE-TIMING/CYCLIC-TIMING/TIME-PERIOD/VALUE'
                    ),
                    format=DataQuery.Format.Float)),
            DataObject('Signal Mappings', DataQuery.XPath('.//I-SIGNAL-TO-I-PDU-MAPPING'), [
                DataValue('Signal', DataQuery(DataQuery.XPath('SHORT-NAME'))),
                DataValue(
                    'Start Position',
                    DataQuery(DataQuery.XPath('START-POSITION'), format=DataQuery.Format.Integer)),
                DataObject('I-Signal', DataQuery.XPath('I-SIGNAL-REF', is_reference=True), [
                    DataValue(
                        'Init Value',
                        DataQuery(DataQuery.XPath('.//VALUE'), format=DataQuery.Format.Integer)),
                    DataValue('Length',
                              DataQuery(DataQuery.XPath('LENGTH'), format=DataQuery.Format.Integer))
                ])
            ])
        ])
    ]


@pytest.fixture
def data():
    return {
        'PDU': [{
            'Name': 'TxMessage',
            'Length': 5,
            'Cyclic Timing': 0.1,
            'Signal Mapping': {
                'Signal': 'Signal1',
                'Start Position': 0,
                'I-Signal': {
                    'Init Value': 128,
                    'Length': 5
                }
            }
        }, {
            'Name':
                'RxMessage',
            'Length':
                2,
            'Cyclic Timing':
                0.1,
            'Signal Mapping': [{
                'Signal': 'Signal2',
                'Start Position': 0,
                'I-Signal': {
                    'Init Value': 0,
                    'Length': 1
                }
            }, {
                'Signal': 'Signal3',
                'Start Position': 1,
                'I-Signal': {
                    'Init Value': 0,
                    'Length': 1
                }
            }]
        }]
    }


def test_print_data(data):
    writer = DataWriter()
    text = writer.to_text(data)

    assert text == 'PDU[0]:\n  Name: TxMessage\n  Length: 5\n  Cyclic Timing: 0.1\n  Signal Mapping:\n    Signal: Signal1\n    Start Position: 0\n    I-Signal:\n      Init Value: 128\n      Length: 5\nPDU[1]:\n  Name: RxMessage\n  Length: 2\n  Cyclic Timing: 0.1\n  Signal Mapping[0]:\n    Signal: Signal2\n    Start Position: 0\n    I-Signal:\n      Init Value: 0\n      Length: 1\n  Signal Mapping[1]:\n    Signal: Signal3\n    Start Position: 1\n    I-Signal:\n      Init Value: 0\n      Length: 1'


def test_write_to_file(data):
    file = Path('result.txt')
    writer = DataWriter()

    writer.write(str(file), data)

    assert file.exists()
    file.unlink()


def test_write_to_json(data):
    file = Path('result.json')
    writer = DataWriter()

    writer.write_json(str(file), data)

    assert file.exists()
    file.unlink()


def test_write_to_excel(data, query):
    file = Path('result.xlsx')
    writer = DataWriter()

    writer.write_excel(str(file), data, query)

    assert file.exists()
    file.unlink()
