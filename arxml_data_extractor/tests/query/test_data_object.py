import pytest

from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_object import DataObject
from arxml_data_extractor.query.data_value import DataValue


@pytest.fixture
def value():
    query = DataQuery(DataQuery.XPath('/SHORT-NAME'))
    return DataValue('Name', query)


@pytest.mark.parametrize("name, path", [
    ('Signal', DataQuery.XPath('//I-SIGNALS')),
    ('Signal123', DataQuery.XPath('//I-SIGNALS')),
    ('Signal_123', DataQuery.XPath('//I-SIGNALS')),
    ('Signal 123', DataQuery.XPath('//I-SIGNALS')),
    ('Signal 123', DataQuery.Reference('/Signals')),
])
def test_create_data_object(name, path, value):
    data_object = DataObject(name, path, [value])

    assert data_object.name == name
    assert data_object.path == path
    assert data_object.values[0] == value


def test_values_contain_data_objects(value):
    sub_object = DataObject('Timings', DataQuery.XPath('//TIMING'), [value])
    data_object = DataObject('Signals', DataQuery.XPath('//I-SIGNALS'), [sub_object])

    assert data_object.name == 'Signals'
    data_object_value = data_object.values[0]
    assert isinstance(data_object_value, DataObject)
    assert data_object_value == sub_object
    assert data_object_value.values[0] == value


def test_empty_values_raises_value_error():
    with pytest.raises(ValueError):
        DataObject('Signals', DataQuery.XPath('/SHORT-NAME'), [])


def test_invalid_values_raise_type_error(value):
    with pytest.raises(TypeError):
        DataObject('Signals', DataQuery.XPath('/SHORT-NAME'), value)


def test_invalid_path_type_raises_type_error(value):
    with pytest.raises(TypeError):
        DataObject('Signals', None, [value])
        DataObject('Signals', 'path', [value])
