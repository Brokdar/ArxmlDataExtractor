import pytest

from arxml_data_extractor.asr.asr_parser import AsrParser


@pytest.fixture
def parser() -> AsrParser:
    arxml = 'arxml_data_extractor/tests/asr/test.arxml'
    return AsrParser(arxml)


def test_lists_all_top_level_packages(parser: AsrParser):
    packages = parser.packages

    assert len(packages) == 3


def test_find_all_elements_by_element_name(parser: AsrParser):
    packages = parser.find_all_elements('AR-PACKAGE')

    assert len(packages) == 6


def test_find_all_elements_by_specified_path(parser: AsrParser):
    top_level_packages = parser.find_all_elements('AR-PACKAGES/AR-PACKAGE')

    assert len(top_level_packages) == 6


def test_find_elements_specified_with_namespace(parser: AsrParser):
    signals = parser.find_all_elements('ar:I-SIGNAL')

    assert len(signals) == 2


def test_find_elements_partly_specified_with_namespace(parser: AsrParser):
    pdus = parser.find_all_elements('ELEMENTS/ar:I-SIGNAL-I-PDU')

    assert len(pdus) == 1


def test_find_elements_from_defined_base_by_path(parser: AsrParser):
    pdu_package = parser.packages['Pdus']
    pdus = AsrParser.find_elements(pdu_package, 'I-SIGNAL-I-PDU')

    assert len(pdus) == 1


def test_find_element_from_defined_base_by_shortname(parser: AsrParser):
    signal_package = parser.packages['ISignals']
    signal = AsrParser.find_element_by_shortname(signal_package, 'I-SIGNAL', 'SignalData1')

    assert signal is not None
    assert AsrParser.get_shortname(signal) == 'SignalData1'


def test_get_shortname(parser: AsrParser):
    pdu_package = parser.packages['Pdus']
    shortname = AsrParser.get_shortname(pdu_package)

    assert shortname == 'Pdus'


def test_find_element_by_reference(parser: AsrParser):
    ref = '/ISignals/Bus/PduCollection/MyPdu/SignalData2'
    signal = parser.find_reference(ref)

    assert signal.tag == '{http://autosar.org/schema/r4.0}I-SIGNAL'
    assert AsrParser.get_shortname(signal) == 'SignalData2'
