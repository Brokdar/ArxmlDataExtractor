import argparse
from pathlib import Path

from arxml_data_extractor.config_provider import ConfigProvider
from arxml_data_extractor.query_builder import QueryBuilder
from arxml_data_extractor.query_handler import QueryHandler
from arxml_data_extractor.data_writer import DataWriter


def run():
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
        help='output file, possible file formats are .txt, .json or .xlsx',
        required=True)

    args = parser.parse_args()

    input_file = Path(args.input)
    if not input_file.exists or not input_file.is_file:
        raise Exception(f'Input file not found: {args.input}')

    config_file = Path(args.config)
    if not config_file.exists or not config_file.is_file:
        raise Exception(f'Config file not found: {args.config}')

    output_file = Path(args.output)
    allowed_suffix = ['.txt', '.json', '.xlsx']
    if output_file.suffix not in allowed_suffix:
        raise Exception(
            f'Output file needs to be of type ".txt, .json or .xlsx". Currently: {output_file.suffix}'
        )

    print('Parsing config file...')
    config_provider = ConfigProvider()
    config = config_provider.load(str(config_file))

    print('Building queries...')
    query_builder = QueryBuilder()
    queries = query_builder.build(config)

    print('Handle queries...')
    query_handler = QueryHandler()
    data = query_handler.handle_queries(str(input_file), queries)

    print(f'write file {str(output_file)}')
    output_writer = DataWriter()
    if output_file.suffix == '.json':
        output_writer.write_json(str(output_file), data)
    elif output_file.suffix == '.xlsx':
        output_writer.write_excel(str(output_file), data, queries)
    else:
        output_writer.write(str(output_file), data)


if __name__ == '__main__':
    run()
