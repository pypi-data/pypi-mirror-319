import pandas as pd

def load_stock_data(stock_name: str, start_date: str = None, end_date: str = None):
    """
    Load stock data for a specific stock, with optional date range filtering.

    Args:
        stock_name (str): The name of the stock symbol (ex.-5PAISA).
        start_date (str, optional): The start date (inclusive) for filtering the stock data, in `YYYY-MM-DD` format.
                                   If not provided, no start date filter will be applied.
        end_date (str, optional): The end date (inclusive) for filtering the stock data, in `YYYY-MM-DD` format.
                                 If not provided, no end date filter will be applied.

    Returns:
        pd.DataFrame: A DataFrame containing the stock data, optionally filtered by the provided date range.

    Raises:
        ValueError: If there is an issue reading the stock data or processing the date range.
    """
    stock_file_path = f"https://bhaumikankan.github.io/predictram_stock_files/Stock_Price/{stock_name}.xlsx"

    try:
        stock_data = pd.read_excel(stock_file_path)
        
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        
        if start_date and end_date:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            stock_data = stock_data[(stock_data['Date'] >= start_date) & (stock_data['Date'] <= end_date)]
        
        return stock_data
    except Exception as e:
        raise ValueError(f"Error loading stock data for {stock_name}: {e}")
