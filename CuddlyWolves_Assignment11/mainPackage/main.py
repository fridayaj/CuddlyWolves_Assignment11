# Name: Aidan Friday
# email:  fridayaj@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:   10/21/24
# Course #/Section:   IS 4010
# Semester/Year:   Spring 24
# Brief Description of the assignment:  Use ChatGPT to create a data analysis program

# Brief Description of what this module does. This is the main
# Citations: ChatGPT, Professor Nicholson
# Anything else that's relevant:

# main.py

import os
from srcPackage.data_cleaner import DataCleaner

if __name__ == "__main__":
    # Define base_dir as the directory containing your script (main.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the path to the input file relative to the base directory
    input_file = os.path.join(base_dir, "..", "Data", "fuelPurchaseData.csv")  # Adjust to correct relative path

    print("Starting data processing...")
    
    # Instantiate the DataCleaner class and process the data
    cleaner = DataCleaner(input_file)
    cleaner.process_data()
    
    print("Data processing is complete.")

