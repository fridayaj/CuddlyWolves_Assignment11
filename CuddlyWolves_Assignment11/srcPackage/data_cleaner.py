# data_cleaner.py


import csv
from srcPackage.utils import round_price, write_csv
from srcPackage.api_handler import fetch_zip_code

class DataCleaner:
    def __init__(self, filename):
        self.filename = filename
        self.anomalies = []
        self.zip_code_cache = {}

    def clean_row(self, row):
        """Clean each row by ensuring pricing format, handling anomalies, and fetching zip codes."""
        try:
            # Ensure Gross Price has 2 decimal places
            if "Gross Price" in row:
                row["Gross Price"] = round_price(row["Gross Price"])

            # Handle "Pepsi" anomalies
            if "Fuel Type" in row and row["Fuel Type"].lower() == "pepsi":
                self.anomalies.append(row)
                return None  # Skip this row

            # Handle missing Zip Code
            if "Full Address" in row and ("Zip Code" not in row or not row["Zip Code"]):
                self.add_zip_code(row)

            return row
        except Exception as e:
            print(f"Error cleaning row {row}: {e}")
            return None  # Return None if row cannot be cleaned successfully
