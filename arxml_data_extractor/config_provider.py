import yaml


class ConfigProvider():

    def __init__(self):
        pass

    def load(self, file: str) -> dict:
        if not file.endswith('.yaml'):
            raise ValueError(f'{file} is not a .yaml file')

        with open(file, 'r') as stream:
            config = yaml.safe_load(stream)

        return config

    def parse(self, text: str) -> dict:
        config = yaml.safe_load(text)

        return config
