import yaml
from pathlib import Path


class ConfigProvider():

    def load(self, file: str) -> dict:
        config_file = Path(file)
        if config_file.suffix != '.yaml':
            raise ValueError(
                f'invalid config file extension: \'{config_file.suffix}\' != \'.yaml\'')

        with open(str(config_file), 'r') as stream:
            config = yaml.safe_load(stream)

        return config

    def parse(self, text: str) -> dict:
        config = yaml.safe_load(text)

        return config
