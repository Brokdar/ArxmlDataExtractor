from tabulate import tabulate

from arxml_data_extractor.output.tabularize import tabularize


class TextWriter():

    def as_table(self, data: dict) -> str:
        text = []
        headers = self.analyze_headers(data)
        for i, values in enumerate(data.values()):
            if not isinstance(values, list):
                values = [values]
            rows = tabularize(values)
            text.append(tabulate(rows, headers=headers[i], tablefmt="orgtbl"))

        return '\n\n\n'.join(text)

    def analyze_headers(self, data: dict) -> list:
        headers = []

        for value in data.values():
            headers.append(self.__names(value))

        return headers

    @classmethod
    def __names(cls, data):
        names = []
        if isinstance(data, dict):
            for key, values in data.items():
                if isinstance(values, list) or isinstance(values, dict):
                    names.extend(cls.__names(values))
                else:
                    names.append(key)
        else:
            # first entry is enough to collect all names
            names.extend(cls.__names(data[0]))
        return names

    def as_dictionary(self, data: dict):
        text = []
        for key, value in data.items():
            self.__data_to_text(key, value, text)

        return '\n'.join(text)

    @classmethod
    def __data_to_text(cls, name, data, text, indent=0):
        if isinstance(data, dict):
            text.append(f'{"  " * indent}{name}:')
            for key, value in data.items():
                cls.__data_to_text(key, value, text, indent + 1)
        elif isinstance(data, list):
            for i, value in enumerate(data):
                n = f'{name}[{i}]'
                cls.__data_to_text(n, value, text, indent)
        else:
            text.append(f'{"  " * indent}{name}: {data}')
