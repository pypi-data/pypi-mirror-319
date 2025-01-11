import pandas as pd

def load_iip_data():
    """
    Load the Index of Industrial Production (IIP) data.

    Args:
        None

    Returns:
        pd.DataFrame: A DataFrame containing the IIP data.

    Raises:
        ValueError: If there is an issue reading the IIP data from the file.
    """
   
    try:
        iip_data = pd.read_excel('https://bhaumikankan.github.io/predictram_stock_files/IIP_data_Nov_2024.xlsx')
        return iip_data
    except Exception as e:
        raise ValueError(f"Error loading IIP data: {e}")
