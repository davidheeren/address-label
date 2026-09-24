
import argparse
from argparse import Namespace


def get_args(defaults: bool = False) -> Namespace:
    """Gets the command line args. If 'defaults' then return the default arguments"""
    parser = argparse.ArgumentParser(
        prog="address_label",
        description="Creates a pdf for printing address labels from an Excel file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-i", "--input", required=True, help="The input excel spreadsheet file path")
    parser.add_argument("-o", "--output", required=True, help="The output pdf file path")
    parser.add_argument("-f", "--filter", default="*", help="Ex: 'mary joe, 4-9, !5'")
    parser.add_argument("-b", "--bias", type=int, default=0, help="Count of labels to offset")
    parser.add_argument("-n", "--name", default="", help="Your name to find return addresses row")
    parser.add_argument("-r", "--ret", action="store_true", help="Include the same number of return address labels")
    parser.add_argument("-t", "--test", action="store_true", help="Put box lines around each lablel")
    parser.add_argument("-l", "--launch", action="store_true", help="Launch the pdf in the browser")
    parser.add_argument("-s", "--scale", type=int, default=100, help="Scale in percent for the UI in the window")
    parser.add_argument("-H", "--no-header", action="store_true", help="The data file has no header row")
    if defaults:
        # Because we require input and output arguments,
        # we need to pass in empty strings
        return parser.parse_args(["-i", " ", "-o", " "])
    return parser.parse_args()
