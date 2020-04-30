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


def test_write_text_file_as_table(data):
    file = Path('result.txt')
    writer = DataWriter()

    writer.write_text(str(file), data)

    assert file.exists()
    file.unlink()


def test_write_to_json(data):
    file = Path('result.json')
    writer = DataWriter()

    writer.write_json(str(file), data)

    assert file.exists()
    file.unlink()


def test_write_to_excel(data):
    file = Path('result.xlsx')
    writer = DataWriter()

    writer.write_excel(str(file), data)

    assert file.exists()
    file.unlink()
