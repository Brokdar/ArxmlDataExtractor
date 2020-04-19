import json
import xlsxwriter

from dataclasses import dataclass
from typing import Union, List

from arxml_data_extractor.query.data_object import DataObject


@dataclass
class Cell():
    row: int
    col: int
    val: any
    row_span: bool = False
    col_span: int = 0


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

    def write_json(self, file: str, data: dict):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def write_excel(self, file: str, data: dict, queries: List[DataObject]):
        workbook = xlsxwriter.Workbook(file)
        self.header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
        })

        for key, value in data.items():
            sheet = workbook.add_worksheet(key)
            query = next(q for q in queries if q.name == key)
            self.__write_worksheet(sheet, value, query)

        workbook.close()

    def __write_worksheet(self, sheet, data: dict, query: DataObject):
        header = self.__extract_header(query)
        df = self.__flatten(data)

        start = self.__write_header(sheet, header)
        for row, frame in enumerate(df, start + 1):
            sheet.write_row(row, 0, frame)

        sheet.autofilter(start, 0, len(df), len(df[0]) - 1)

    @classmethod
    def __extract_header(cls, query: DataObject) -> list:
        header = []

        for value in query.values:
            if isinstance(value, DataObject):
                values = cls.__extract_header(value)
                header.append((value.name, values))
            else:
                header.append(value.name)

        return header

    def __write_header(self, sheet, header):
        stack = []
        max_row, _ = self.__analyze_structure(0, 0, header, stack)
        while stack:
            cell = stack.pop()
            if cell.row_span:  # value
                sheet.write(max_row, cell.col, cell.val, self.header_format)
            else:  # object
                if cell.col_span > 0:
                    sheet.merge_range(cell.row, cell.col, cell.row, cell.col + cell.col_span,
                                      cell.val, self.header_format)
                else:
                    sheet.write(cell.row, cell.col, cell.val, self.header_format)

        return max_row

    @classmethod
    def __analyze_structure(cls, row, col, header, stack):
        max_row = row

        for item in header:
            if isinstance(item, tuple):
                old_col = col
                max_row, col = cls.__analyze_structure(row + 1, col, item[1], stack)
                stack.append(Cell(row, old_col, item[0], col_span=col - old_col))
            else:
                stack.append(Cell(row, col, item, True))
            col += 1

        return max_row, col - 1

    @classmethod
    def __flatten(cls, data: Union[list, dict]):
        rows = []

        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, dict):
                    rows.extend(cls.__flatten(value))
                elif isinstance(value, list):
                    row = rows.copy()
                    rows.clear()
                    for v in value:
                        rows.append(row + cls.__flatten(v))
                else:
                    rows.append(value)
        elif isinstance(data, list):
            for d in data:
                res = cls.__flatten(d)
                if res and isinstance(res[0], list):
                    rows.extend(res)
                else:
                    rows.append(res)
        else:
            raise TypeError(f'data must be of type list or dict -> currently: {type(data)}')

        return rows
