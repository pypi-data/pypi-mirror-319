# Shiftify

Shiftify is a Python package that provides easy and efficient tools for converting data between CSV and JSON formats. It supports direct file operations to transform CSV files into JSON and vice versa.

## Features

- **CSV to JSON Conversion**: Convert CSV files into JSON format with automatic field detection.
- **JSON to CSV Conversion**: Convert JSON files back into CSV format, also with automatic field detection.
- **Customizable Delimiters and Quotes**: Customize how CSV files are read and written by specifying different delimiters and quote characters.


## Installation

To install Shiftify, run the following command in your terminal:

```bash
pip install Shiftify
```

## Usage

# Converting CSV to JSON
```python
from shiftify import Convert

convert = Convert()
convert.csv_to_json('path/to/your/input.csv', 'path/to/your/output.json')
```
# Converting JSON to CSV
```python
from shiftify import Convert

convert = Convert()
convert.json_to_csv('path/to/your/input.json', 'path/to/your/output.csv')
```
# Update delimiter or quotechar

By default delimiter is `,` and quotechar is `"`, if you want to update these see below:
```python
from shiftify import Convert

convert = Convert(delimiter=',', quotechar='"')
convert.json_to_csv('path/to/your/input.json', 'path/to/your/output.csv')
```

# Contributing
Contributions to Shiftify are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

# License
This project is licensed under the MIT License - see the LICENSE file for details.