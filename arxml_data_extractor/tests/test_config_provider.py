import pytest

from arxml_data_extractor.config_provider import ConfigProvider


def test_provides_config_from_file():
    yaml = 'arxml_data_extractor/tests/test_config.yaml'

    provider = ConfigProvider()
    config = provider.load(yaml)

    assert isinstance(config, dict)
    assert len(config) == 1
    root = config['RootObject']
    assert isinstance(root, dict)
    assert root['_xpath'] == './/*'
    assert root['SingleValue'] == 'text:Value'
    object_value = root['ObjectValue']
    assert object_value['_xpath'] == './/Object'
    assert object_value['Name'] == 'text:Name'
    assert object_value['Data'] == 'text>int:Data'


def test_raises_value_error_if_not_yaml():
    yaml = 'test/config.json'

    provider = ConfigProvider()

    with pytest.raises(ValueError):
        provider.load(yaml)


def test_raises_exception_if_file_not_exists():
    not_existing_file = 'non-existing.yaml'

    provider = ConfigProvider()

    with pytest.raises(FileNotFoundError):
        provider.load(not_existing_file)


def test_provides_config_from_string():
    yaml = """
    SingleValue: "text:/PathToElement"
    """

    provider = ConfigProvider()
    config = provider.parse(yaml)

    assert isinstance(config, dict)
    assert config['SingleValue'] == 'text:/PathToElement'
