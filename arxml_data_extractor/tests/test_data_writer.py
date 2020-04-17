import pytest
from pathlib import Path

from arxml_data_extractor.data_writer import DataWriter


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