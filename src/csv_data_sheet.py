
from src.data_sheet import Address, ADDRESS_COLUMN_COUNT
import csv


class CsvDataSheet:

    def __init__(self, header: bool, input_path: str):
        self.min_row = 2 if header else 1
        self.data = self._load_data(input_path)
        self.max_row = self._find_max_row(self.data)

    # assume that the input path is the correct filetype and exists
    def _load_data(self, input_path: str) -> list[list[object]]:
        """Loads a whole csv file into memory as a list"""
        with open(input_path, mode="r") as file:
            # convert empty strings to None values for consistency with the excel version
            return [[value if value != "" else None for value in row] for row in csv.reader(file)]

    def _find_max_row(self, data: list[list[object]]) -> int:
        """Nothing special here because csv files don't have lots of extra rows due to formatting"""
        return len(data)

    def get_address(self, row: int) -> Address:
        """Returns a address record from the data at the 1 based row index"""
        if row < self.min_row or row > self.max_row:
            raise ValueError(f"Row index: {row} out of bounds: {self.min_row}-{self.max_row}")
        values = [
            self.data[row - 1][col]
            for col in range(0, ADDRESS_COLUMN_COUNT)
        ]
        return Address(*values)
