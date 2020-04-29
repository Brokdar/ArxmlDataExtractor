import argparse
import logging
import sys
from pathlib import Path

from arxml_data_extractor.config_provider import ConfigProvider
from arxml_data_extractor.query_builder import QueryBuilder
from arxml_data_extractor.query_handler import QueryHandler
from arxml_data_extractor.data_writer import DataWriter


# sets the text color to red
def print_error(msg: str):
    print('\033[91mError: ' + msg + '\033[0m')


def handle_error(msg: str):
    logging.getLogger().error(msg)
    print_error(msg)


def handle_exception(msg: str, e: Exception):
    logging.getLogger().error(msg, exc_info=e)
    print_error(f'{msg}, {str(e)}')


def parse_arguments():
    # setup console arguments
    parser = argparse.ArgumentParser(
        description='Extracts specified data provided in a config file from an ARXML file.')
    parser.add_argument(
        '--config',
        '-c',
        help='config file that specifies the data that should be extracted',
        required=True)
    parser.add_argument(
        '--input', '-i', help='ARXML file from where the data should be extracted', required=True)
    parser.add_argument(
        '--output',
        '-o',
        help='output file, possible file formats are \'.txt\', \'.json\' or \'.xlsx\'.',
        required=True)
    parser.add_argument(
        '--debug',
        '-d',
        help='enable debug modus, this will create a log file.',
        action='store_true')

    return parser.parse_args()


def setup_logging(enable: bool):
    logger = logging.getLogger()

    if enable:
        logging.basicConfig(
            filename='extraction.log', filemode='w', format='%(levelname)s: %(message)s')
        logger.setLevel('DEBUG')
    else:
        logger.disabled = True


def validate_arguments(args):
    input_file = Path(args.input)
    if not input_file.exists() or not input_file.is_file():
        handle_error(f'input file: \'{args.input}\' doesn\'t exist or isn\'t a valid file')
        sys.exit(-1)

    config_file = Path(args.config)
    if not config_file.exists() or not config_file.is_file():
        handle_error(f'config file: \'{args.config}\' doesn\'t exist or isn\'t a valid file')
        sys.exit(-1)

    output_file = Path(args.output)
    allowed_suffix = ['.txt', '.json', '.xlsx']
    if output_file.suffix not in allowed_suffix:
        handle_error(
            f'invalid output file extension \'{output_file.suffix}\'. Allowed extensions: \'.txt\', \'.json\' or \'.xlsx\''
        )
        sys.exit(-1)

    return input_file, config_file, output_file


def load_config(file):
    logger = logging.getLogger()
    logger.info(f'START PROCESS - loading configuration \'{str(file)}\'')

    try:
        config_provider = ConfigProvider()
        config = config_provider.load(str(file))
    except Exception as e:
        handle_exception(f'reading configuration file \'{str(file)}\'', e)
        sys.exit(-1)

    logger.info('END PROCESS - successfully finished loading configuration')
    return config


def build_queries(config):
    logger = logging.getLogger()
    logger.info('START PROCESS - building queries from configuration')

    try:
        query_builder = QueryBuilder()
        queries = query_builder.build(config)
    except Exception as e:
        handle_exception('building queries', e)
        sys.exit(-1)

    logger.info('END PROCESS - successfully finished building queries from configuration')
    return queries


def extract_data(file, queries):
    logger = logging.getLogger()
    logger.info('START PROCESS - handling of data queries')

    try:
        query_handler = QueryHandler()
        data = query_handler.handle_queries(str(file), queries)
    except Exception as e:
        handle_exception('handling queries', e)
        sys.exit(-1)

    logger.info('END PROCESS - successfully finished handling of data queries')
    return data


def write_data(file, data, queries):
    logger = logging.getLogger()
    logger.info(f'START PROCESS - writing results to \'{str(file)}\'')
    print(f'Writing results to \'{str(file)}\'')

    try:
        output_writer = DataWriter()
        if file.suffix == '.json':
            output_writer.write_json(str(file), data)
        elif file.suffix == '.xlsx':
            output_writer.write_excel(str(file), data, queries)
        else:
            output_writer.write(str(file), data)
    except Exception as e:
        handle_exception(f'writing results to \'{str(file)}\'', e)
        sys.exit(-1)

    logger.info('END PROCESS - successfully finished writing results')
    print(f'Done.')


def run():
    args = parse_arguments()
    setup_logging(args.debug)
    input_file, config_file, output_file = validate_arguments(args)

    config = load_config(config_file)
    queries = build_queries(config)
    data = extract_data(input_file, queries)
    write_data(output_file, data, queries)


if __name__ == '__main__':
    run()
