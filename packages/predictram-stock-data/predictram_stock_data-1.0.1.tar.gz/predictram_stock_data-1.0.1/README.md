# predictram_stock_data

## Overview

The `predictram_stock_data` package provides functionality to load and process stock data and economic indicators such as the Index of Industrial Production (IIP). The package includes functions to retrieve stock data for specific stocks, filter by date range, and load IIP data.

## Installation

To install this package locally, you can run the following command:

```cmd
pip install predictram_stock_data

```

## Modules and Functions

### `load_iip_data`

- **Description**: Loads the Index of Industrial Production (IIP) data from an Excel file.
- **Returns**: A `pandas.DataFrame` containing the IIP data.
- **Raises**:
  - `FileNotFoundError`: If the IIP data file is not found at the specified file path.
  - `ValueError`: If there is an issue reading the IIP data file.

### `load_stock_data`

- **Description**: Loads stock data for a specific stock, with optional date range filtering.
- **Arguments**:
  - `stock_name` (str): The name of the stock (without the `.xlsx` extension).
  - `start_date` (str, optional): The start date (inclusive) in `YYYY-MM-DD` format. Defaults to `None`.
  - `end_date` (str, optional): The end date (inclusive) in `YYYY-MM-DD` format. Defaults to `None`.
- **Returns**: A `pandas.DataFrame` containing the stock data, optionally filtered by the specified date range.
- **Raises**:
  - `FileNotFoundError`: If the stock data file is not found at the specified location.
  - `ValueError`: If there is an issue reading the stock data or processing the date range.

## Usage Example

```python
from predictram_stock_data import load_stock_data, load_iip_data

# Load stock data for a specific stock
stock_data = load_stock_data("AAPL", start_date="2021-01-01", end_date="2021-12-31")

# Load IIP data
iip_data = load_iip_data()
```
