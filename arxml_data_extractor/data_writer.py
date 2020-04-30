import json
import xlsxwriter

from dataclasses import dataclass
from typing import Union, List

from arxml_data_extractor.query.data_object import DataObject
from arxml_data_extractor.output.tabularize import tabularize
from arxml_data_extractor.output.text_writer import TextWriter


@dataclass
class Cell():
    row: int
    col: int
    val: any
    row_span: bool = False
    col_span: int = 0


class DataWriter():

    def write_text(self, file: str, data: dict):
        writer = TextWriter()
        text = writer.as_table(data)

        with open(file, 'w') as f:
            f.write(text)

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

    def __write_worksheet(self, sheet, data: Union[dict, list], query: DataObject):
        header = self.__extract_header(query)
        if isinstance(data, dict):
            data = [data]
        df = tabularize(data)

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
