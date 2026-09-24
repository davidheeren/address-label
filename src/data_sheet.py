
from collections import namedtuple

ADDRESS_COLUMN_COUNT = 10

# Record data format
Address = namedtuple(
    "Address", ["last_name1", "first_name1", "last_name2", "first_name2", "address1", "address2", "city", "state", "zip", "country"]
)


# base class for wrapping either .xlsx or .csv data
class DataSheet:
    def __init__(self):
        self.min_row = 0
        self.max_row = 0

    def get_address(self, row: int) -> Address:
        raise NotImplementedError("Should not be called on the base class")
