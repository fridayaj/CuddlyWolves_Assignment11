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

# utils.py

import csv

def round_price(price):
    """Rounds the price to 2 decimal places."""
    try:
        # Attempt to convert the price to a float and format it to 2 decimal places.
        return f"{float(price):.2f}"
    except (ValueError, TypeError):
        # If the price is not a valid number, return "0.00".
        # This could happen for invalid or missing data (e.g., 'N/A' or empty strings).
        # Consider logging or tracking invalid price values for review.
        return "0.00"

def remove_duplicates(rows):
    """Removes duplicate rows based on the 'Transaction Number'."""
    seen = set() # Set to keep track of unique transaction numbers
    unique_rows = [] # List to store rows with unique transaction numbers
    for row in rows:
        # Check if the 'Transaction Number' is valid (not empty or None)
        if row["Transaction Number"] not in seen:
            unique_rows.append(row)
            seen.add(row["Transaction Number"])
    return unique_rows

def write_csv(filepath, data):
    """Writes data to a CSV file."""
    if data:
        with open(filepath, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
