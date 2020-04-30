import json
from dataclasses import dataclass

from arxml_data_extractor.output.text_writer import TextWriter
from arxml_data_extractor.output.excel_writer import ExcelWriter


class DataWriter():

    def write_text(self, file: str, data: dict):
        writer = TextWriter()
        text = writer.as_table(data)

        with open(file, 'w') as f:
            f.write(text)

    def write_json(self, file: str, data: dict):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def write_excel(self, file: str, data: dict):
        writer = ExcelWriter()
        writer.write(file, data)
