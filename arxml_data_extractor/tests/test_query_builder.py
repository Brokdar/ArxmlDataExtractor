import pytest

from arxml_data_extractor.query.data_object import DataObject
from arxml_data_extractor.query_builder import QueryBuilder
from arxml_data_extractor.query.data_query import DataQuery
from arxml_data_extractor.query.data_value import DataValue


def test_build_simple_data_object_with_xpath():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': '/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)

    assert isinstance(data_objects, list)
    data_object = data_objects[0]
    assert isinstance(data_object, DataObject)
    assert data_object.name == 'SimpleObject'
    assert isinstance(data_object.path, DataQuery.XPath)
    assert data_object.path.xpath == '/path/element'
    data_value = data_object.values[0]
    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert isinstance(data_value.query, DataQuery)
    assert isinstance(data_value.query.path, DataQuery.XPath)
    assert data_value.query.path.xpath == '/SHORT-NAME'
    assert data_value.query.path.is_relative is True
    assert data_value.query.value == 'text'
    assert data_value.query.format == DataQuery.Format.String


def test_build_simple_data_object_with_reference():
    config = {'SimpleObject': {'_ref': '/path/element', 'SimpleValue': '/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)

    assert isinstance(data_objects, list)
    data_object = data_objects[0]
    assert isinstance(data_object, DataObject)
    assert data_object.name == 'SimpleObject'
    assert isinstance(data_object.path, DataQuery.Reference)
    assert data_object.path.ref == '/path/element'
    data_value = data_object.values[0]
    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert isinstance(data_value.query, DataQuery)
    assert isinstance(data_value.query.path, DataQuery.XPath)
    assert data_value.query.path.xpath == '/SHORT-NAME'
    assert data_value.query.path.is_relative is True
    assert data_value.query.value == 'text'
    assert data_value.query.format == DataQuery.Format.String


def test_object_is_missing_xpath_or_ref():
    config = {'SimpleObject': {'SimpleValue': '/SHORT-NAME'}}
    builder = QueryBuilder()

    with pytest.raises(ValueError):
        builder.build(config)


def test_object_has_too_many_separators():
    config = {
        'SimpleObject': {
            '_xpath': '/path/element',
            'SimpleValue': '/ar:AR-PACKAGE/ar:SHORT-NAME'
        }
    }
    builder = QueryBuilder()

    with pytest.raises(ValueError):
        builder.build(config)


def test_text_value():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': 'text:/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)
    data_value = data_objects[0].values[0]

    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert data_value.query.path == DataQuery.XPath('/SHORT-NAME')
    assert data_value.query.value == 'text'
    assert data_value.query.format == DataQuery.Format.String


def test_tag_value():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': 'tag:/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)
    data_value = data_objects[0].values[0]

    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert data_value.query.path == DataQuery.XPath('/SHORT-NAME')
    assert data_value.query.value == 'tag'
    assert data_value.query.format == DataQuery.Format.String


def test_attribute_value():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': '@T:/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)
    data_value = data_objects[0].values[0]

    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert data_value.query.path == DataQuery.XPath('/SHORT-NAME')
    assert data_value.query.value == '@T'
    assert data_value.query.format == DataQuery.Format.String


def test_text_value_as_string():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': 'text>string:/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)
    data_value = data_objects[0].values[0]

    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert data_value.query.path == DataQuery.XPath('/SHORT-NAME')
    assert data_value.query.value == 'text'
    assert data_value.query.format == DataQuery.Format.String


def test_text_value_as_integer():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': 'text>int:/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)
    data_value = data_objects[0].values[0]

    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert data_value.query.path == DataQuery.XPath('/SHORT-NAME')
    assert data_value.query.value == 'text'
    assert data_value.query.format == DataQuery.Format.Integer


def test_text_value_as_float():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': 'text>float:/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)
    data_value = data_objects[0].values[0]

    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert data_value.query.path == DataQuery.XPath('/SHORT-NAME')
    assert data_value.query.value == 'text'
    assert data_value.query.format == DataQuery.Format.Float


def test_text_value_as_date():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': 'text>date:/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)
    data_value = data_objects[0].values[0]

    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert data_value.query.path == DataQuery.XPath('/SHORT-NAME')
    assert data_value.query.value == 'text'
    assert data_value.query.format == DataQuery.Format.Date


def test_text_value_with_invalid_format():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': 'text>bool:/SHORT-NAME'}}
    builder = QueryBuilder()

    data_objects = builder.build(config)
    data_value = data_objects[0].values[0]

    assert isinstance(data_value, DataValue)
    assert data_value.name == 'SimpleValue'
    assert data_value.query.path == DataQuery.XPath('/SHORT-NAME')
    assert data_value.query.value == 'text'
    assert data_value.query.format == DataQuery.Format.String


def test_invalid_path_characters():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': '>/SHORT-NAME'}}
    builder = QueryBuilder()

    with pytest.raises(ValueError):
        builder.build(config)


def test_invalid_attribute_characters():
    config = {'SimpleObject': {'_xpath': '/path/element', 'SimpleValue': '@:/SHORT-NAME'}}
    builder = QueryBuilder()

    with pytest.raises(ValueError):
        builder.build(config)


def test_data_objects_can_contain_data_object():
    config = {
        'SimpleObject': {
            '_xpath': '/path/element',
            'SimpleValue': '/SHORT-NAME',
            'OtherObject': {
                '_xpath': '/path/other_element',
                'Value': '@T>date:/date_time'
            }
        }
    }

    builder = QueryBuilder()
    data_objects = builder.build(config)
    other_object = data_objects[0].values[1]

    assert isinstance(other_object, DataObject)
    assert isinstance(other_object.path, DataQuery.XPath)
    assert other_object.path.xpath == '/path/other_element'
    data_value = other_object.values[0]
    assert isinstance(data_value, DataValue)
    assert data_value.name == 'Value'
    assert isinstance(data_value.query.path, DataQuery.XPath)
    assert data_value.query.path.xpath == '/date_time'
    assert data_value.query.value == '@T'
    assert data_value.query.format == DataQuery.Format.Date
