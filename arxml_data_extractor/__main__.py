import argparse
import logging
from pathlib import Path

from arxml_data_extractor.config_provider import ConfigProvider
from arxml_data_extractor.query_builder import QueryBuilder
from arxml_data_extractor.query_handler import QueryHandler
from arxml_data_extractor.data_writer import DataWriter


# sets the text color to red
def print_error(msg: str):
    print('\033[91m' + msg + '\033[0m')


def run():
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

    args = parser.parse_args()

    # setup logging
    logger = logging.getLogger()

    if args.debug:
        logging.basicConfig(
            filename='extraction.log', filemode='w', format='%(levelname)s: %(message)s')
        logger.setLevel('DEBUG')
    else:
        logger.disabled = True

    # console argument validation
    input_file = Path(args.input)
    if not input_file.exists() or not input_file.is_file():
        logger.error(f'input file: \'{args.input}\' doesn\'t exist or isn\'t a valid file')
        print_error(f'ERROR: input file not found: \'{args.input}\'')
        exit(-1)

    config_file = Path(args.config)
    if not config_file.exists() or not config_file.is_file():
        logger.error(f'config file: \'{args.config}\' doesn\'t exist or isn\'t a valid file.')
        print_error(f'ERROR: config file not found: \'{args.config}\'.')
        exit(-1)

    output_file = Path(args.output)
    allowed_suffix = ['.txt', '.json', '.xlsx']
    if output_file.suffix not in allowed_suffix:
        logger.error(
            f'invalid output file extension \'{output_file.suffix}\'. Allowed extensions: \'txt\', \'json\' or \'xlsx\''
        )
        print_error(
            f'invalid output file extension \'{output_file.suffix}\'. Allowed extensions: \'txt\', \'json\' or \'xlsx\''
        )
        exit(-1)

    # load configuration file
    try:
        logger.info(f'START PROCESS - loading configuration \'{str(config_file)}\'')
        config_provider = ConfigProvider()
        config = config_provider.load(str(config_file))
        logger.info('END PROCESS - successfully finished loading configuration')
    except Exception as e:
        logger.exception(f'failed reading configuration file {str(config_file)}')
        print_error(f'ERROR: reading config file \'{str(config_file)}\', {str(e)}')
        exit(-1)

    # parse configuration and build queries
    try:
        logger.info('START PROCESS - building queries from configuration')
        query_builder = QueryBuilder()
        queries = query_builder.build(config)
        logger.info('END PROCESS - successfully finished building queries from configuration')
    except Exception as e:
        logger.exception(f'failed building queries')
        print_error(f'ERROR: failed building queries, {str(e)}')
        exit(-1)

    # handle queries and extract the data
    try:
        logger.info('START PROCESS - handling of data queries')
        query_handler = QueryHandler()
        data = query_handler.handle_queries(str(input_file), queries)
        logger.info('END PROCESS - successfully finished handling of data queries')
    except Exception as e:
        logger.exception(f'failed handling queries')
        print_error(f'ERROR: failed handling queries, {str(e)}')
        exit(-1)

    # write the extracted data in the given output format
    try:
        logger.info(f'START PROCESS - writing the results to \'{str(output_file)}\'')
        print(f'writing results to \'{str(output_file)}\'')

        output_writer = DataWriter()
        if output_file.suffix == '.json':
            output_writer.write_json(str(output_file), data)
        elif output_file.suffix == '.xlsx':
            output_writer.write_excel(str(output_file), data, queries)
        else:
            output_writer.write(str(output_file), data)

        logger.info('END PROCESS - successfully finished writing the results')
        print(f'Done.')

    except Exception as e:
        logger.exception(f'failed writing results to \'{str(output_file)}\'')
        print_error(f'ERROR: failed writing result to \'{str(output_file)}\', {str(e)}')
        exit(-1)


if __name__ == '__main__':
    run()
