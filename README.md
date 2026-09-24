# Address Label Generator

This is a personal script designed to generate PDFs of address labels formatted for Avery 8160 sticky label sheets.

It is tailored to work with my specific address data, in an Excel spreadsheet. The script reads the address information, allows for filtering of specific addresses, and then creates a printable PDF file.

## Excel Format

The script expects an `.xlsx` or `.csv` file with the following columns in order. A header is optional

`last_name1, first_name1, last_name2, first_name2, address1, address2, city, state, zip, country`

## Usage

### Command Line

Use `uv run main.py -h` for help.

### GUI

There's also a GUI. Run it with:
`uv run gui.py`

It has all the same options and saves your settings between sessions.

On Linux, the GUI needs the tk system package
On Linux, the file dialogue uses either zenity or kdialog

### Testing

`./run-tests.sh`
