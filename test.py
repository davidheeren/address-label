import unittest
import main
from label_generator import LabelGenerator, Address


class TestLabelGenerator(unittest.TestCase):

    def test_split_filters1(self):
        args = main.get_args()
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
        args = main.get_args()
        args.filter = "hello , ! ,,"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "dangling '!'"):
            _ = label_generator._split_and_format_filters()

    def test_get_address1(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_address = label_generator._get_address(2)
        compare_address = Address("Chen", "Olivia", None, None, "123 Maple St", None, "Sunnyvale", "CA", 94086, None)
        self.assertEqual(new_address, compare_address)

    def test_get_address2(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_address = label_generator._get_address(5)
        compare_address = Address("Goldberg", "Liam", "Miller", "Sarah", "101 Cedar Ct", None, "Portland", "OR", 97209, None)
        self.assertEqual(new_address, compare_address)

    def test_get_address3(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = label_generator._get_address(50)

    def test_match_names1(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Carter")
        comare_indices = {3}
        self.assertEqual(new_indices, comare_indices)

    def test_match_names2(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("noah patel")
        comare_indices = {7}
        self.assertEqual(new_indices, comare_indices)

    def test_match_names3(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("   Olivia     Chen    ")
        comare_indices = {2}
        self.assertEqual(new_indices, comare_indices)

    def test_match_names4(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Liam Goldberg Sarah Miller")
        comare_indices = {5}
        self.assertEqual(new_indices, comare_indices)

    def test_match_names5(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Ki")
        comare_indices = set()
        self.assertEqual(new_indices, comare_indices)

    def test_match_names6(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Lucas Williams Miller")
        comare_indices = set()
        self.assertEqual(new_indices, comare_indices)

    def test_match_names7(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_names("Sarah")
        comare_indices = {3, 5}
        self.assertEqual(new_indices, comare_indices)

    def test_match_index_or_range1(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_index_or_range("2")
        comare_indices = {2}
        self.assertEqual(new_indices, comare_indices)

    def test_match_index_or_range2(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        new_indices = label_generator._match_index_or_range("  3 -  5")
        comare_indices = {3, 4, 5}
        self.assertEqual(new_indices, comare_indices)

    def test_match_index_or_range3(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Invalid index range"):
            _ = label_generator._match_index_or_range("3 -- 5")

    def test_match_index_or_range4(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Invalid index range"):
            _ = label_generator._match_index_or_range("3   -")

    def test_match_index_or_range5(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Invalid index range"):
            _ = label_generator._match_index_or_range("-")

    def test_match_index_or_range6(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = label_generator._match_index_or_range("50")

    def test_match_index_or_range7(self):
        args = main.get_args()
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "start > end"):
            _ = label_generator._match_index_or_range(" 5 -3 ")

    def test_filter_indices1(self):
        args = main.get_args()
        args.filter = "2"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        comare_indices = ({2}, -1)
        self.assertEqual(new_indices, comare_indices)

    def test_filter_indices2(self):
        args = main.get_args()
        args.filter = "*"
        args.name = "Noah Patel"
        args.ret = True
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        comare_indices = ({2, 3, 4, 5, 6, 8, 9, 10}, 7)
        self.assertEqual(new_indices, comare_indices)

    def test_filter_indices3(self):
        args = main.get_args()
        args.filter = "*, !5-10, !chen, 7"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        comare_indices = ({3, 4, 7}, -1)
        self.assertEqual(new_indices, comare_indices)

    def test_filter_indices4(self):
        args = main.get_args()
        args.filter = "1 - ava"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Not a valid filter"):
            _ = label_generator._filter_indices()

    def test_filter_indices5(self):
        args = main.get_args()
        args.filter = "  ,  ,"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = (set(), -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices6(self):
        args = main.get_args()
        args.filter = "!5"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = (set(), -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices7(self):
        args = main.get_args()
        args.filter = "Sarah, !Sarah"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = (set(), -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices8(self):
        args = main.get_args()
        args.filter = "2-6"
        args.name = "Ava Nguyen"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = ({2, 3, 4, 5}, 6)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices9(self):
        args = main.get_args()
        args.filter = " * , !9-10 "
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = ({2, 3, 4, 5, 6, 7, 8}, -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices10(self):
        args = main.get_args()
        args.filter = "Sarah Someone"
        label_generator = LabelGenerator(args)
        new_indices = label_generator._filter_indices()
        compare_indices = (set(), -1)
        self.assertEqual(new_indices, compare_indices)

    def test_filter_indices11(self):
        args = main.get_args()
        args.filter = "0"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = label_generator._filter_indices()

    def test_filter_indices12(self):
        args = main.get_args()
        args.filter = "11"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            _ = label_generator._filter_indices()

    def test_filter_indices13(self):
        args = main.get_args()
        args.filter = "-5"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Invalid index range"):
            _ = label_generator._filter_indices()

    def test_filter_indices14(self):
        args = main.get_args()
        args.filter = "12abc"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "Not a valid filter"):
            _ = label_generator._filter_indices()

    def test_filter_indices15(self):
        args = main.get_args()
        args.filter = "*"
        args.name = "Sarah"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "found multiple times"):
            _ = label_generator._filter_indices()

    def test_filter_indices16(self):
        args = main.get_args()
        args.filter = "*"
        args.name = "Nonexistent Person"
        label_generator = LabelGenerator(args)
        with self.assertRaisesRegex(ValueError, "not found"):
            _ = label_generator._filter_indices()
