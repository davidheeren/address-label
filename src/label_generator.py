
from argparse import Namespace
import webbrowser
from pathlib import Path
from pylabels import Sheet, Specification
from reportlab.graphics import shapes
from src.excel_data_sheet import ExcelDataSheet
from src.csv_data_sheet import CsvDataSheet
from src.data_sheet import DataSheet, Address

# Pylabels2 docs example: https://github.com/erikvw/pylabels2/blob/main/pylabels/demos/addresses.py


class LabelGenerator:
    def __init__(self, args: Namespace):
        """Setup and load data"""
        self.args = args
        self.data_sheet = self._load_data_sheet(self.args.input, not self.args.no_header)

    def _load_data_sheet(self, input_path: str, header: bool) -> DataSheet:
        if (input_path is None or input_path.strip() == ""):
            raise FileNotFoundError("Input path cannot be empty")
        path = Path(input_path)
        if not path.is_file():
            raise FileNotFoundError(f"Input file not found at: {path}")
        if path.suffix.lower() == ".xlsx":
            return ExcelDataSheet(header, input_path)
        elif path.suffix.lower() == ".csv":
            return CsvDataSheet(header, input_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}. Only .xlsx or .csv files are supported.")

    def _split_and_format_filters(self) -> list[tuple[str, bool]]:
        """Returns a list of filters: (string, invert). Split on ','"""
        f_strs = self.args.filter.split(",")
        filters = []
        for f in f_strs:
            invert = False
            f = f.strip()
            if not f:
                continue
            if f.startswith("!"):
                invert = True
                f = f[1:]
            if not f:
                raise ValueError("Invalid filter: dangling '!'")
            filters.append((f, invert))
        return filters

    def _match_names(self, filter: str) -> set[int]:
        """
        Takes a list of names seperated by spaces
        Returns a set of all indices matched in the name fields
        All parts in the split input filter, must match an address name field
        """
        filter_parts = [x.strip().lower() for x in filter.split()]
        indices = set()
        for i in range(self.data_sheet.min_row, self.data_sheet.max_row + 1):
            address = self.data_sheet.get_address(i)
            # Address name fields if they exist
            address_parts = {
                x.strip().lower()
                for x in (
                    address.last_name1,
                    address.first_name1,
                    address.last_name2,
                    address.first_name2,
                )
                if x}
            if all(a in address_parts for a in filter_parts):
                indices.add(i)
        return indices

    def _match_index_or_range(self, filter: str) -> set[int]:
        """Determines if filter is index or range and returns set of the matched indices"""
        # Filter is a range
        if "-" in filter:
            parts = filter.split("-")
            if len(parts) != 2 or not parts[0].strip().isdigit() or not parts[1].strip().isdigit():
                raise ValueError(f"Invalid index range: {filter}")
            start, end = map(int, (parts[0], parts[1]))
            if start < self.data_sheet.min_row or start > self.data_sheet.max_row or end < self.data_sheet.min_row or end > self.data_sheet.max_row:
                raise ValueError(f"Invalid index: {filter}, out of bounds {self.data_sheet.min_row}-{self.data_sheet.max_row}")
            if start > end:
                raise ValueError(f"Invalid range: start > end in {filter}")
            return set(range(start, end + 1))

        # Filter is single number
        num = int(filter)
        if num < self.data_sheet.min_row or num > self.data_sheet.max_row:
            raise ValueError(f"Invalid index: {filter}, out of bounds {self.data_sheet.min_row}-{self.data_sheet.max_row}")
        return {num}

    def _filter_indices(self) -> tuple[set[int], int]:
        """
        Finds all matched indices from the filter argument
        Also removes the name input arg
        Returns the set of matched indices and the name index
        """
        filters = self._split_and_format_filters()
        # Result indices to return
        indices = set()
        for filter, invert in filters:
            # Set of nums to either add to or remove from indices
            nums = set()

            # Filter is wildcard
            if filter == "*":
                nums.update(range(self.data_sheet.min_row, self.data_sheet.max_row + 1))

            # Filter is a name
            elif all(c.isalpha() or c.isspace() for c in filter):
                match_nums = self._match_names(filter)
                nums.update(match_nums)
                print(f"Matched name: '{filter}', {len(match_nums)} times")

            # Filter is number or number range
            elif all(c.isdigit() or c == "-" or c.isspace() for c in filter):
                match_nums = self._match_index_or_range(filter)
                nums.update(match_nums)

            # Not a valid filter
            else:
                raise ValueError(f"Not a valid filter: {filter}")

            # Update the indices based on the invert
            if invert:
                indices.difference_update(nums)
            else:
                indices.update(nums)

        # Remove name
        name_idx = -1
        if self.args.name:
            match_nums = self._match_names(self.args.name)
            if len(match_nums) == 0:
                raise ValueError(f"Name: '{self.args.name}' not found. This is needed for the return address")
            if len(match_nums) > 1:
                raise ValueError(f"Name: '{self.args.name}' found multiple times. There can only be one for the return address")
            indices.difference_update(match_nums)
            name_idx = match_nums.pop()

        return indices, name_idx

    # Makes the method not take self as a parameter
    @staticmethod
    def _draw_address(label, width, height, address: Address | None):
        """Draws an address to a label"""
        if address is None:
            return

        # Formats the name based on which entries are empty or not
        # John Miller, John & Mary Miller, John Miller & Mary Sue
        # If a single name, like a company, should only have last_name1
        name = ""
        if address.last_name1 and address.first_name1 and address.last_name2 and address.first_name2:
            name = f"{address.first_name1} {address.last_name1} & {address.first_name2} {address.last_name2}"
        elif address.last_name1 and address.first_name1 and address.first_name2:
            name = f"{address.first_name1} & {address.first_name2} {address.last_name1}"
        elif address.last_name1 and address.first_name1:
            name = f"{address.first_name1} {address.last_name1}"
        elif address.last_name1:
            name = address.last_name1
        else:
            print(f"Warning: Skipping line with invalid name '{address.last_name1} {address.first_name1} {address.last_name2} {address.first_name2}'")
            return

        # Only include the PO box, if not empty
        street = address.address1
        if address.address2:
            street = address.address2

        # Lines of the label
        # Uppercase for maximal readability
        lines = [
            address.country.upper() if address.country else None,
            f"{address.city} {address.state}  {address.zip}".upper(),
            street.upper(),
            name,
        ]

        # From the pylables2 library docs
        group = shapes.Group()
        x, y = 0, 0
        for line in lines:
            if not line:
                continue
            shape = shapes.String(x, y, line, textAnchor="start", fontSize=10)
            _, _, _, y = shape.getBounds()
            y += 3
            group.add(shape)
        _, _, lx, ly = label.getBounds()
        _, _, gx, gy = group.getBounds()

        if gx > lx:
            print(f"Warning: Address too long, name: {name}")
        if gy > ly:
            print(f"Warning: Address too tall, name: {name}")

        dx = (lx - gx) / 2
        dy = (ly - gy) / 2
        group.translate(dx, dy)

        label.add(group)

    def _create_sheet(self) -> Sheet:
        """Creates a sheet that can be saved as a PDF"""
        # Follows the Avery 8160 specs
        # From the pylabels2 docs
        padding = 1
        specs = Specification(
            215.9,
            279.4,
            3,
            10,
            66.7,
            25.4,
            corner_radius=2,
            left_margin=5,
            right_margin=5,
            top_margin=13,
            left_padding=padding,
            right_padding=padding,
            top_padding=padding,
            bottom_padding=padding,
            row_gap=0,
        )
        if self.args.test:
            return Sheet(specs, self._draw_address, border=True)
        return Sheet(specs, self._draw_address)

    def _save_pdf(self, sheet: Sheet, indices: set[int], name_idx: int):
        """Saves the sheet as a PDF"""
        # Add blank labels
        if self.args.bias > 0:
            sheet.add_label(None, count=self.args.bias)

        # add the address with a min count of 1
        repeat_count = self.args.count if self.args.count > 1 else 1

        # Add labels for the indices
        for i in sorted(list(indices)):
            address = self.data_sheet.get_address(i)

            if not any(address):
                print(f"Warning: Skipping blank row index '{i}'")
                continue

            if not address.last_name1 or not address.address1 or not address.city or not address.state or not address.zip:
                print(f"Warning: Skipping row with name: '{address.first_name1}', index: '{i}' due to one or more missing address fields.")
                continue

            for j in range(repeat_count):
                sheet.add_label(address)

        # Add return address labels
        if self.args.ret:
            if not self.args.name:
                raise ValueError("Name must be set to use the ret option")
            for j in range(repeat_count):
                sheet.add_label(self.data_sheet.get_address(name_idx), count=len(indices))

        if (self.args.output is None or self.args.output.strip() == ""):
            raise FileNotFoundError("Output path cannot be empty")
        sheet.save(self.args.output)
        print(f"{sheet.label_count} label(s) output on {sheet.page_count} page(s).")

    def generate_pdf(self):
        indices, name_idx = self._filter_indices()
        sheet = self._create_sheet()
        self._save_pdf(sheet, indices, name_idx)
        if self.args.launch:
            webbrowser.open(self.args.output)
