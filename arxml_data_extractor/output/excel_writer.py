from dataclasses import dataclass
from xlsxwriter import Workbook

from arxml_data_extractor.output.tabularize import tabularize


@dataclass
class Cell():
    row: int
    col: int
    val: any
    col_span: int = 0
    is_object: bool = False


class ExcelWriter():

    def write(self, file: str, data: dict):
        workbook = Workbook(file)
        self.header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'bg_color': 'white'
        })

        for key, value in data.items():
            sheet = workbook.add_worksheet(key)
            row_count = self.write_header(sheet, value)
            self.write_data_frames(sheet, value, row_count)

        workbook.close()

    def write_header(self, sheet, data):
        headers = []
        max_row, max_col = self.analyze_header(data, headers)
        self.preformat_header(sheet, max_row, max_col)

        while headers:
            cell = headers.pop()
            if cell.is_object:
                if cell.col_span > 0:
                    sheet.merge_range(cell.row, cell.col, cell.row, cell.col + cell.col_span,
                                      cell.val, self.header_format)
                else:
                    sheet.write(cell.row, cell.col, cell.val, self.header_format)
            else:
                sheet.write(max_row, cell.col, cell.val, self.header_format)

        return max_row

    def preformat_header(self, sheet, rows, cols):
        for row in range(rows):
            for col in range(cols):
                sheet.write(row, col, None, self.header_format)

    def analyze_header(self, data, header, row=0, col=0):
        max_row = row

        if isinstance(data, list):
            data = data[0]

        for key, value in data.items():
            if isinstance(value, (list, dict)):
                max_row, n_col = self.analyze_header(value, header, row + 1, col)
                header.append(Cell(row, col, key, n_col - col, True))
                col = n_col
            else:
                header.append(Cell(row, col, key))
            col += 1

        return max_row, col - 1

    def write_data_frames(self, sheet, data, start_row):
        if isinstance(data, dict):
            data = [data]

        data_frames = tabularize(data)
        for row_idx, df in enumerate(data_frames, start_row + 1):
            sheet.write_row(row_idx, 0, df)

        row_count = len(data_frames)
        column_count = len(data_frames[0]) - 1
        sheet.autofilter(start_row, 0, row_count, column_count)
