import unittest
from src.arguments import get_args
from src.label_generator import LabelGenerator
from src.data_sheet import Address
from src.excel_data_sheet import ExcelDataSheet
from src.csv_data_sheet import CsvDataSheet

EXCEL_DATA_PATH = "tests/TestData.xlsx"
CSV_DATA_PATH = "tests/TestData.csv"


class TestLabelGenerator(unittest.TestCase):

    def _get_default_args(self):
        args = get_args(True)
        args.input = EXCEL_DATA_PATH
        args.output = "labels.pdf"
        return args

    def test_split_filters1(self):
        args = self._get_default_args()
        args.filter = "1 - 5, !Mary Jane,,   , 5, ! * "
        label_generator = LabelGenerator(args)
        new_filters = label_generator._split_and_format_filters()
        compare_filters = [
            ("1 - 5", False),
            ("Mary Jane", True),
            ("5", False),
            (" *", True),
        ]
        self.assertEqual(new_filters, compare_filters)

    def test_split_filters2(self):
        args = self._get_default_args()
        args.filter = "hello , ! ,,"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "dangling '!'"):
            _ = label_generator._split_and_format_filters()

    def test_get_address1(self):
        new_excel_address = ExcelDataSheet(True, EXCEL_DATA_PATH).get_address(2)
        new_csv_address = CsvDataSheet(True, CSV_DATA_PATH).get_address(2)
        compare_address = Address("Chen", "Olivia", None, None, "123 Maple St", None, "Sunnyvale", "CA", "94086", None)
        self.assertEqual(new_excel_address, compare_address)
        self.assertEqual(new_csv_address, compare_address)

    def test_get_address2(self):
        new_excel_address = ExcelDataSheet(True, EXCEL_DATA_PATH).get_address(5)
        new_csv_address = CsvDataSheet(True, CSV_DATA_PATH).get_address(5)
        compare_address = Address("Goldberg", "Liam", "Miller", "Sarah", "101 Cedar Ct", None, "Portland", "OR", "97209", None)
        self.assertEqual(new_excel_address, compare_address)
        self.assertEqual(new_csv_address, compare_address)

    def test_get_address3(self):
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = ExcelDataSheet(True, EXCEL_DATA_PATH).get_address(50)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = CsvDataSheet(True, CSV_DATA_PATH).get_address(50)

    def test_get_address4(self):
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = ExcelDataSheet(False, EXCEL_DATA_PATH).get_address(0)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = CsvDataSheet(False, CSV_DATA_PATH).get_address(0)

    def test_get_address5(self):
        new_excel_address = ExcelDataSheet(True, EXCEL_DATA_PATH).get_address(10)
        new_csv_address1 = CsvDataSheet(True, CSV_DATA_PATH).get_address(10)
        new_csv_address2 = CsvDataSheet(True, CSV_DATA_PATH).get_address(11)
        new_csv_address3 = CsvDataSheet(True, CSV_DATA_PATH).get_address(12)
        compare_address = Address(None, None, None, None, None, None, None, None, None, None)
        self.assertEqual(new_excel_address, compare_address)
        self.assertEqual(new_csv_address1, compare_address)
        self.assertEqual(new_csv_address2, compare_address)
        self.assertEqual(new_csv_address3, compare_address)

    def test_get_address6(self):
        new_excel_sheet = ExcelDataSheet(True, EXCEL_DATA_PATH)
        new_csv_sheet = CsvDataSheet(True, CSV_DATA_PATH)
        compare_address = Address("Kim", "Mia", None, None, "667 Maple St", None, "Sunnyvale", "CA", "94086", None)
        self.assertEqual(new_excel_sheet.max_row, 13)
        self.assertEqual(new_csv_sheet.max_row, 13)
        self.assertEqual(new_excel_sheet.get_address(13), compare_address)
        self.assertEqual(new_csv_sheet.get_address(13), compare_address)

    def test_format_name(self):
        cases = [
            (("Doe", None, None, None), "Doe"),
            (("Doe", "Jan", None, None), "Jan Doe"),
            (("Doe", "Jan", None, "Sam"), "Jan & Sam Doe"),
            (("Doe", "Jan", "Roe", "Sam"), "Jan Doe & Sam Roe"),
            (("Doe", "Jan", "Roe", None), "Jan Doe & Roe"),
            (("Doe", None, None, "Sam"), "Sam Doe"),
            (("Doe", None, "Roe", "Sam"), "Doe & Sam Roe"),
            (("Doe", None, "Roe", None), "Doe & Roe"),
            ((None, "Jan", "Roe", "Sam"), None),
        ]
        for names, compare_name in cases:
            address = Address(*names, "1 Main St", None, "Town", "CA", "94086", None)
            self.assertEqual(LabelGenerator._format_name(address), compare_name)

    def test_match_names1(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Carter")
        comare_indices = {3}
        self.assertEqual(new_indices, comare_indices)

    def test_match_names2(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("noah patel")
        comare_indices = {7}
        self.assertEqual(new_indices, comare_indices)

    def test_match_names3(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("   Olivia     Chen    ")
        comare_indices = {2}
        self.assertEqual(new_indices, comare_indices)

    def test_match_names4(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Liam Goldberg Sarah Miller")
        comare_indices = {5}
        self.assertEqual(new_indices, comare_indices)

    def test_match_names5(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Ki")
        comare_indices = set()
        self.assertEqual(new_indices, comare_indices)

    def test_match_names6(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Lucas Williams Miller")
        comare_indices = set()
        self.assertEqual(new_indices, comare_indices)

    def test_match_names7(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Sarah")
        comare_indices = {3, 5}
        self.assertEqual(new_indices, comare_indices)

    def test_match_index_or_range1(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_index_or_range("2")
        comare_indices = {2}
        self.assertEqual(new_indices, comare_indices)

    def test_match_index_or_range2(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_index_or_range("  3 -  5")
        comare_indices = {3, 4, 5}
        self.assertEqual(new_indices, comare_indices)

    def test_match_index_or_range3(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Invalid index range"):
            _ = label_generator._match_index_or_range("3 -- 5")

    def test_match_index_or_range4(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Invalid index range"):
            _ = label_generator._match_index_or_range("3   -")

    def test_match_index_or_range5(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Invalid index range"):
            _ = label_generator._match_index_or_range("-")

    def test_match_index_or_range6(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = label_generator._match_index_or_range("50")

    def test_match_index_or_range7(self):
        args = self._get_default_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "start > end"):
            _ = label_generator._match_index_or_range(" 5 -3 ")

    def test_filter_indices1(self):
        args = self._get_default_args()
        args.filter = "2"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        comare_indices = ({2}, -1)
        self.assertEqual(new_indices, comare_indices)

    def test_filter_indices2(self):
        args = self._get_default_args()
        args.filter = "*"
        args.name = "Noah Patel"
        args.ret = True
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        comare_indices = ({2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13}, 7)
        self.assertEqual(new_indices, comare_indices)

    def test_filter_indices3(self):
        args = self._get_default_args()
        args.filter = "*, !5-10, !chen, 7"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        comare_indices = ({3, 4, 7, 11, 12, 13}, -1)
        self.assertEqual(new_indices, comare_indices)

    def test_filter_indices4(self):
        args = self._get_default_args()
        args.filter = "1 - ava"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Not a valid filter"):
            _ = label_generator._filter_indices()

    def test_filter_indices5(self):
        args = self._get_default_args()
        args.filter = "  ,  ,"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = (set(), -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices6(self):
        args = self._get_default_args()
        args.filter = "!5"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = (set(), -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices7(self):
        args = self._get_default_args()
        args.filter = "Sarah, !Sarah"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = (set(), -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices8(self):
        args = self._get_default_args()
        args.filter = "2-6"
        args.name = "Ava Nguyen"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = ({2, 3, 4, 5}, 6)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices9(self):
        args = self._get_default_args()
        args.filter = " * , !9-10 "
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = ({2, 3, 4, 5, 6, 7, 8, 11, 12, 13}, -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices10(self):
        args = self._get_default_args()
        args.filter = "Sarah Someone"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = (set(), -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices11(self):
        args = self._get_default_args()
        args.filter = "0"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = label_generator._filter_indices()

    def test_filter_indices12(self):
        args = self._get_default_args()
        args.filter = "14"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = label_generator._filter_indices()

    def test_filter_indices13(self):
        args = self._get_default_args()
        args.filter = "-5"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Invalid index range"):
            _ = label_generator._filter_indices()

    def test_filter_indices14(self):
        args = self._get_default_args()
        args.filter = "12abc"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Not a valid filter"):
            _ = label_generator._filter_indices()

    def test_filter_indices15(self):
        args = self._get_default_args()
        args.filter = "*"
        args.name = "Sarah"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "found multiple times"):
            _ = label_generator._filter_indices()

    def test_filter_indices16(self):
        args = self._get_default_args()
        args.filter = "*"
        args.name = "Nonexistent Person"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "not found"):
            _ = label_generator._filter_indices()

    def _get_return_label_count(self, filter: str, count: int) -> int:
        args = self._get_default_args()
        args.output = "/dev/null"
        args.filter = filter
        args.count = count
        args.name = "Noah Patel"
        args.ret = True
        label_generator = LabelGenerator(args)
        indices, name_idx = label_generator._filter_indices()
        sheet = label_generator._create_sheet()
        label_generator._save_pdf(sheet, indices, name_idx)
        return sheet.label_count

    def test_return_labels1(self):
        # 8 recipients and 8 return labels, rows 10-12 are blank
        self.assertEqual(self._get_return_label_count("*", 1), 16)

    def test_return_labels2(self):
        self.assertEqual(self._get_return_label_count("*", 2), 32)

    def test_return_labels3(self):
        # Only Kim is left, rows 10-12 are blank
        self.assertEqual(self._get_return_label_count("*, !2-9", 1), 2)
