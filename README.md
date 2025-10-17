# Report of Monaco 2018 Racing

## Description
Package **Report of Monaco 2018 Racing** processes results of Racing in keys of general score and drivers`s personals results.

Using results`s log files Package makes table with results and marks drivers who go to the next stage of competition. 

## Using
Package can be used directly as well as via command line
### To use directly:
```python
from racing_reports_2018 import print_report, get_text_from_pdf
print(print_report(<path_to_file>, <driver_name>, <desc_of_asc (True/None>))

# Extract text from PDF files
text = get_text_from_pdf(<path_to_pdf_file>)
```
`path_to_file_1` - path to folder where are log files (start.log, end.log, abbreviation.txt)

`driver_name` - name driver (to show driver result) /optional/ (for default - `None`)

`desc_of_asc` - if `None` score will form from the fastest result, if `True` - from the slowest (for default - `None`).

`path_to_pdf_file` - path to PDF file for text extraction

### To use via command line
```commandline
--files <folder_path> --driver “Sebastian Vettel” --desc
```
`--files` - path to folder where are log files (start.log, end.log, abbreviation.txt)

`--desc` - to ger reversed score (from slowest)(for default not used)

`--driver` - name driver (to show driver result) /optional/ (for default not used)

>Package has all necessary [unittest](https://docs.python.org/3/library/unittest.html) with **coverage near 90% of code**.

## Package consists from:
 - **main.py**: module with the main functional tools
 - **parser_main.py**: module which are responsible for command line functions
 - **test_main.py**: with tests for main.py
 - **test_parser.py**: with tests for parser_main.py

## Used tools:
- lru_cache from [functools](https://docs.python.org/3/library/functools.html)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF text extraction

and for testing
- [unittest](https://docs.python.org/3/library/unittest.html)
- patch, mock_open from [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [os](https://docs.python.org/3/library/os.html#module-os)
