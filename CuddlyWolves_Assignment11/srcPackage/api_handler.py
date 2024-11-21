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


import requests
import time

API_KEY = "fa5dc4f0-a7a3-11ef-810a-575df598337c"
BASE_URL = "https://app.zipcodebase.com/api/v1/code/city"

def fetch_zip_code(city, state):
    """Fetches the ZIP code for a given city and state using the API."""
    if not city or not state:
        print(f"City or State is empty or invalid. Cannot fetch zip code.")
        return "ZIP_NOT_FOUND"

    city = city.strip().title()  # Normalize city name (capitalize)
    state = state.strip().upper()  # Normalize state (uppercase)
    
    params = {"apikey": API_KEY, "city": city, "state_name": state, "country": "us"}

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(BASE_URL, headers={"apikey": API_KEY}, params=params)
            response.raise_for_status()  # Check for HTTP errors

            data = response.json()

            if "results" in data and city.lower() in data["results"]:
                zip_codes = data["results"][city.lower()]
                if zip_codes:
                    return zip_codes[0]  # Return the first ZIP code in the list
            print(f"No zip code found for city: {city}, state: {state}")
            return "ZIP_NOT_FOUND"

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error fetching zip code (attempt {attempt + 1}/3): {e}")
            if response.status_code == 500:
                time.sleep(2)  # Retry after short delay
            else:
                break
        except Exception as e:
            print(f"Unexpected error fetching zip code: {e}")
            break

    print(f"Failed to fetch zip code after 3 attempts for city: {city}, state: {state}")
    return "ZIP_NOT_FOUND"

