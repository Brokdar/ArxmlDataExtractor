from arxml_data_extractor.output.tabularize import tabularize


def test_flatten_dict():
    input = {'Name': 'Message', 'Length': 16, 'Cyclic Timing': 0.1}

    result = tabularize([input])

    assert result == [['Message', 16, 0.1]]


def test_flatten_nested_dict():
    input = {
        'Name': 'Message',
        'Length': 8,
        'Cyclic Timing': 0.1,
        'Signal': {
            'Name': 'Signal1',
            'Length': 8
        }
    }

    result = tabularize([input])

    assert result == [['Message', 8, 0.1, 'Signal1', 8]]


def test_multiple_entries():
    input = [{'Name': 'Request', 'Length': 8}, {'Name': 'Response', 'Length': 16}]

    result = tabularize(input)

    assert result == [['Request', 8], ['Response', 16]]


def test_dict_containing_list():
    input = {
        'Name': 'Message',
        'Length': 16,
        'Signal': [{
            'Name': 'Signal1',
            'Length': 8
        }, {
            'Name': 'Signal2',
            'Length': 8
        }]
    }

    result = tabularize([input])

    assert result == [['Message', 16, 'Signal1', 8], ['Message', 16, 'Signal2', 8]]


def test_dict_containing_lists_with_same_dimension():
    input = {
        'Name': 'Message',
        'Length': 16,
        'Signal': [{
            'Name': 'Signal1',
            'Length': 8
        }, {
            'Name': 'Signal2',
            'Length': 8
        }],
        'SignalGroup': [{
            'Name': 'SignalGroup1'
        }, {
            'Name': 'SignalGroup2'
        }]
    }

    result = tabularize([input])

    assert result == [['Message', 16, 'Signal1', 8, 'SignalGroup1'],
                      ['Message', 16, 'Signal2', 8, 'SignalGroup2']]


def test_dict_containing_lists_different_dimensions():
    input = {
        'Name':
            'Message',
        'Length':
            16,
        'Signal': [{
            'Name': 'Signal1',
            'Length': 8
        }, {
            'Name': 'Signal2',
            'Length': 8
        }],
        'SignalGroup': [{
            'Name': 'SignalGroup1'
        }, {
            'Name': 'SignalGroup2'
        }, {
            'Name': 'SignalGroup3'
        }]
    }

    result = tabularize([input])

    assert result == [['Message', 16, 'Signal1', 8, 'SignalGroup1'],
                      ['Message', 16, 'Signal1', 8, 'SignalGroup2'],
                      ['Message', 16, 'Signal1', 8, 'SignalGroup3'],
                      ['Message', 16, 'Signal2', 8, 'SignalGroup1'],
                      ['Message', 16, 'Signal2', 8, 'SignalGroup2'],
                      ['Message', 16, 'Signal2', 8, 'SignalGroup3']]
