import pandas as pd
import os
from .config import IIP_FILE_PATH

def load_iip_data():
    """
    Load the Index of Industrial Production (IIP) data.

    Args:
        None

    Returns:
        pd.DataFrame: A DataFrame containing the IIP data.

    Raises:
        FileNotFoundError: If the IIP data file is not found at the specified file path.
        ValueError: If there is an issue reading the IIP data from the file.
    """
    print(IIP_FILE_PATH)
    if not IIP_FILE_PATH or not os.path.exists(IIP_FILE_PATH):
        raise FileNotFoundError(f"File {IIP_FILE_PATH} not found.")
    try:
        iip_data = pd.read_excel(IIP_FILE_PATH)
        return iip_data
    except Exception as e:
        raise ValueError(f"Error loading IIP data: {e}")
