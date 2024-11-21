# Name: Kayla Wilson, Adian Friday, Alexis Tipkemper-Sparks, Jared Rababy
# email:  wilso5ky@mail.uc.edu, fridayaj@mail.uc.edu, rababyjd@mail.uc.edu, tipkemam@mail.uc.edu
# Assignment Number: Assignment 11  
# Due Date:   11/21/24
# Course #/Section:   IS4010
# Semester/Year:   Fall 2024
# Brief Description of the assignment: Torture 
# Brief Description of what this module does: Learning to use api and connecting to CSV files 
# Citations: Chatgpt 
# Anything else that's relevant: Naur 

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
 
    def add_zip_code(self, row):
        """Fetch zip code for missing zip codes using a cache to speed up the process."""
        try:
            full_address = row.get("Full Address", "")
            if not full_address:
                return

            # Split the full address into parts
            address_parts = [part.strip() for part in full_address.split(",")]

            if len(address_parts) >= 3:
                city = address_parts[1].strip().rstrip(',')  # Remove trailing comma if present
                state_zip = address_parts[2].strip()

                # Extract state and zip code (if available)
                state_zip_parts = state_zip.split(" ")
                row["State"] = state_zip_parts[0]

                # Check cache first before making API call
                cache_key = f"{city},{row['State']}"
                if cache_key in self.zip_code_cache:
                    row["Zip Code"] = self.zip_code_cache[cache_key]
                else:
                    if len(state_zip_parts) > 1:
                        row["Zip Code"] = state_zip_parts[1]
                    else:
                        # Fetch zip code from the API
                        zip_code = fetch_zip_code(city, row["State"])
                        self.zip_code_cache[cache_key] = zip_code  # Cache the result
                        row["Zip Code"] = zip_code

                row["City"] = city

        except Exception as e:
            print(f"Error adding zip code for row {row}: {e}")

    def process_data(self):
        """Process the CSV file by reading, cleaning rows, removing duplicates, and handling errors."""
        try:
            with open(self.filename, mode='r', encoding='ISO-8859-1', errors='ignore') as file:
                reader = csv.DictReader(file)

                if not reader:
                    print("No data found in the CSV file.")
                    return

                print("Processing rows...")

                # Ensure that 'Zip Code', 'State', 'City' are in fieldnames
                fieldnames = reader.fieldnames + ['Zip Code', 'State', 'City']  # Add any additional fields here

                # Open output files for cleaned data and anomalies
                with open("Data/cleanedData.csv", mode='w', newline='', encoding='utf-8') as cleaned_file, \
                        open("Data/dataAnomalies.csv", mode='w', newline='', encoding='utf-8') as anomalies_file:

                    cleaned_writer = csv.DictWriter(cleaned_file, fieldnames=fieldnames)
                    anomalies_writer = csv.DictWriter(anomalies_file, fieldnames=fieldnames)

                    # Write headers to the output files
                    cleaned_writer.writeheader()
                    anomalies_writer.writeheader()

                    # Process rows and write to the appropriate files
                    for row in reader:
                        cleaned_row = self.clean_row(row)
                        if cleaned_row:
                            cleaned_writer.writerow(cleaned_row)
                        else:
                            anomalies_writer.writerow(row)

            print("Data processing is complete.")

        except Exception as e:
            print(f"An error occurred while processing data: {e}")