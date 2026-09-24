
from src.data_sheet import Address, ADDRESS_COLUMN_COUNT
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import load_workbook
from pathlib import Path


class ExcelDataSheet:

    def __init__(self, header: bool, input_path: str):
        self.min_row = 2 if header else 1
        self.ws = self._load_worksheet(input_path)
        self.max_row = self._find_max_row(self.ws)

    # assume that the input path is the correct filetype and exists
    def _load_worksheet(self, input_path: str) -> Worksheet:
        """Loads an Excel file and returns the first Worksheet"""
        path = Path(input_path)
        # if not path.is_file():
        #     raise FileNotFoundError(f"Input file not found at: {path}")
        # if path.suffix.lower() != ".xlsx":
        #     raise ValueError(f"Unsupported file type: {path.suffix}. Only or .xlsx files are supported.")
        wb = load_workbook(path)
        return wb.active

    def _find_max_row(self, ws: Worksheet) -> int:
        """Finds the max row that is not empty, since ws.max_row counts empty rows at the end"""
        count = 0
        for row in ws:
            if any(cell.value is not None for cell in row):
                count += 1
        return count

    def get_address(self, row: int) -> Address:
        """Returns a address record from the data at the 1 based row index"""
        if row < self.min_row or row > self.max_row:
            raise ValueError(f"Row index: {row} out of bounds: {self.min_row}-{self.max_row}")
        values = [
            self.ws.cell(row=row, column=col).value
            for col in range(1, ADDRESS_COLUMN_COUNT + 1)
        ]
        return Address(*values)
