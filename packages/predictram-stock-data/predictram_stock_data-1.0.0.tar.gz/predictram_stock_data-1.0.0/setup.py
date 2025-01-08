from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="predictram_stock_data",
    version="1.0.0",
    description="The `predictram_stock_data` package provides functionality to load and process stock data and economic indicators such as the Index of Industrial Production (IIP). The package includes functions to retrieve stock data for specific stocks, filter by date range, and load IIP data.",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    author="PredictRam",
    author_email="support@predictram.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl"
    ],
    include_package_data=True,
)
