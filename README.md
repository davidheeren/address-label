# Address Label Generator

A personal script for generating PDFs of address labels formatted for Avery 8160 sticky label sheets, from a spreadsheet of address data.

The script reads address rows from an Excel or CSV file, lets you filter which rows to include, and produces a printable PDF.

## Data File Format

The script expects an `.xlsx` or `.csv` file with the following columns, in this order:

`last_name1, first_name1, last_name2, first_name2, address1, address2, city, state, zip, country`

A header row is optional - if your file has one, pass `-H`/`--no-header` so the first row isn't treated as data.

Rows are referenced by one based index. Row 1 is the first data row (or 2 is if there is a header).

## Options

| Flag | Long form | Argument | Default | Description |
|------|-----------|----------|---------|-------------|
| `-i` | `--input` | path | *(required)* | Path to the input `.xlsx` or `.csv` address file |
| `-o` | `--output` | path | *(required)* | Path to write the output PDF |
| `-f` | `--filter` | string | `*` | Selects which rows to include (see [Filtering](#filtering)) |
| `-H` | `--no-header` | flag | off | Set this if the data file has no header row |
| `-b` | `--bias` | int | `0` | Number of label positions to skip on the first sheet (if you're reusing a partially used label sheet) |
| `-c` | `--count` | int | `1` | Number of copies to print of each selected address |
| `-n` | `--name` | string | *(none)* | Your name, used to find your own row for return-address labels (see [Return addresses](#return-addresses)) |
| `-r` | `--ret` | flag | off | Prints return-address labels using the `name` option, one return label for each address matched by the `filter`|
| `-t` | `--test` | flag | off | Draw box outlines around each label, useful for checking alignment before printing on real label sheets |
| `-l` | `--launch` | flag | off | Open the generated PDF automatically after creation in a browser |
| `-s` | `--scale` | int | `100` | UI scale percentage, GUI only |

### Filtering

The `-f`/`--filter` option controls which rows are included in the output. It takes a comma-separated list of terms, each of which either **adds** or **removes** rows from the selection. Terms are applied left to right, so later terms can override earlier ones.

Each term is one of:

| Term | Meaning |
|------|---------|
| `*` | All rows |
| `3` | A single row, by index |
| `4-9` | A range of rows, inclusive |
| `mary jane` | Match by name - a row matches if **all** the words given appear in that row's name fields (case-insensitive, works across first/last name and second recipient's names) |

Prefix any term with `!` to **remove** matching rows from the current selection instead of adding them.

Terms are evaluated in order, so:

`"*, !5-10, !john, 15"`

means: 
1. start with all rows
2. remove rows 5 through 10
3. remove any row matching "john"
4. add row 15 back in


### Return Addresses

If you pass `--name "Your Name"`, the script finds the row matching that name and treats it as **your** row rather than a recipient:

- Your row is always excluded from the regular recipient labels, regardless of whether it was included by the `filter`.
- If `-r`/`--ret` is also set, return-address labels using your row are added to the output, matching the count of recipient labels selected.
- `-n` must match exactly one row.


## Usage

### Command Line

`uv run main.py -i <input file> -o <output file> [options]`

Example: generate labels for every row in addresses.xlsx:

`uv run main.py -i addresses.xlsx -o labels.pdf`

Example — only rows 1 through 5, skip row 3, add box outlines for test printing:

`uv run main.py -i addresses.xlsx -o labels.pdf -f "1-5, !3" -t`

Example — print every row except mine, and include return address labels using my row:

`uv run main.py -i addresses.xlsx -o labels.pdf -n "Jane Doe" -r`

### GUI

There's also a GUI, with all the same options, which saves your settings between sessions:

`uv run gui.py`

On Linux, the GUI requires the `tk` system package, and its file dialogs use either `zenity` or `kdialog`.

### Testing

`./run-tests.sh`

## Desktop Shortcuts

The `desktop/` folder has files for launching the GUI directly from your desktop environment, without opening a terminal.

### Windows

Use `desktop/AddressLabel.bat`:

1. Copy the file (or create a shortcut to it).
2. Edit it and replace `C:\the-path-of-this-repo-here` with the absolute path where you cloned this repo.
3. Place the copy or shortcut in `~\Desktop` or `~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs`.
4. Optionally, set the shortcut's icon to `desktop/icon.ico`.

### Linux

Use `desktop/AddressLabel.desktop`:

1. Edit the file and replace `/the-path-of-this-repo-here` in the `Exec`, `Path`, and `Icon` fields with the absolute path where you cloned this repo.
2. Copy it to `~/.local/share/applications` or to `~/Desktop`.

`desktop/icon.png` is the icon referenced by the `.desktop` file.
