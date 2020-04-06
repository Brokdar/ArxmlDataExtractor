import pytest

from arxml_data_extractor.query.data_query import DataQuery


@pytest.mark.parametrize("path, value, format", [
    (DataQuery.Reference('/Signals/Signal1'), 'text', DataQuery.Format.String),
    (DataQuery.Reference('/Signals/Signal1'), 'tag', DataQuery.Format.Integer),
    (DataQuery.Reference('/Signals/Signal1'), '@', DataQuery.Format.Float),
    (DataQuery.Reference('/Signals/Signal1'), '@attribute', DataQuery.Format.Date),
    (DataQuery.XPath('/SHORT-NAME', False), 'text', DataQuery.Format.String),
    (DataQuery.XPath('/SHORT-NAME', True), 'tag', DataQuery.Format.Integer),
    (DataQuery.XPath('/SHORT-NAME'), '@', DataQuery.Format.Float),
    (DataQuery.XPath('/SHORT-NAME'), '@attribute', DataQuery.Format.Date),
])
def test_create_data_query(path, value, format):
    query = DataQuery(path, value, format)

    assert query.path == path
    assert query.value == value
    assert query.format == format


@pytest.mark.parametrize("path, value", [
    (DataQuery.Reference('/Signals/Signal1'), 'text'),
    (DataQuery.Reference('/Signals/Signal1'), '@attribute'),
    (DataQuery.XPath('/SHORT-NAME', True), 'tag'),
    (DataQuery.XPath('/SHORT-NAME'), '@'),
])
def test_create_data_query_with_default_format(path, value):
    query = DataQuery(path, value)

    assert query.path == path
    assert query.value == value
    assert query.format == DataQuery.Format.String


def test_create_data_query_with_default_value():
    path = DataQuery.XPath('/SHORT-NAME')
    format = DataQuery.Format.Date

    query = DataQuery(path, format=format)

    assert query.path == path
    assert query.value == 'text'
    assert query.format == format


def test_create_data_query_with_absolute_xpath():
    path = DataQuery.XPath('/AR-PACKAGE/SHORT-NAME', False)

    query = DataQuery(path)

    assert query.path == path
    assert query.value == 'text'
    assert query.format == DataQuery.Format.String


def test_create_data_query_with_relative_xpath():
    path = DataQuery.XPath('/SHORT-NAME')

    query = DataQuery(path)

    assert query.path == path
    assert query.value == 'text'
    assert query.format == DataQuery.Format.String


def test_invalid_value_raise_value_error():
    with pytest.raises(ValueError):
        DataQuery(DataQuery.XPath('/SHORT-NAME'), 'something')


def test_invalid_path_raises_exception():
    with pytest.raises(TypeError):
        DataQuery('/SHORT-NAME')


def test_xpath_containing_namespaces_raise_value_error():
    with pytest.raises(ValueError):
        DataQuery(DataQuery.XPath('/ar:SHORT-NAME'))


def test_reference_containing_namespaces_raise_value_error():
    with pytest.raises(ValueError):
        DataQuery(DataQuery.Reference('/ar:Signals'))
