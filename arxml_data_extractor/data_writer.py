class DataWriter():

    def to_text(self, data: dict):
        text = []
        for key, value in data.items():
            self.__data_to_text(key, value, text)

        return '\n'.join(text)

    def __data_to_text(self, name, data, text, indent=0):
        if isinstance(data, dict):
            text.append(f'{"  " * indent}{name}:')
            for key, value in data.items():
                self.__data_to_text(key, value, text, indent + 1)
        elif isinstance(data, list):
            for i, value in enumerate(data):
                n = f'{name}[{i}]'
                self.__data_to_text(n, value, text, indent)
        else:
            text.append(f'{"  " * indent}{name}: {data}')

    def write(self, file: str, data: dict):
        with open(file, 'w') as f:
            f.write(self.to_text(data))
