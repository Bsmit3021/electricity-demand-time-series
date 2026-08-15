import csv
import json
import os
import ssl
import time
import urllib.parse
import urllib.request

# Base Configuration
API_KEY = "xxxxxxxxxxx" # API Key
BASE_URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
OUTPUT_CSV = "data/soco_hourly_demand_2years.csv" # name of new file created for 2-year data pull

# Set a 2-year window May 2024 to May 2026 for data pull
START_DATE = "2024-05-01T00"
END_DATE = "2026-04-30T23"

# Initial Query Parameters
PAGE_SIZE = 5000 # max rows per page for EIA API
params = { # creating dictionary
    "api_key": API_KEY, # Sends API key for authentication
    "frequency": "hourly", # request hourly data
    "data[0]": "value", # request value field from API
    "facets[respondent][]": "SOCO", # filter data so only SOCO (Southern Company) are returned
    "start": START_DATE, # start date and time may 2024 12:00 AM
    "end": END_DATE, # end date and time may 2026 11:00 PM
    # Total time 2 years X 365 days X 24 hours = 17,520 hours return value
    "sort[0][column]": "period", # sort order by timestamp
    "sort[0][direction]": "asc", # sort in ascending order
    "length": str(PAGE_SIZE), # max rows per page for EIA API
}

all_records = []
offset = 0
has_more_data = True

# Use a verified SSL context when possible
context = ssl.create_default_context()
# Create data/raw if it does not exist

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

print(f"Starting data pull for SOCO from {START_DATE} to {END_DATE}...")

# Loop to download API data in pages until all data is retrieved one page at a time
while has_more_data:
    params["offset"] = str(offset) # API knows which record to start from for the next page of data
    url_mod = f"{BASE_URL}?{urllib.parse.urlencode(params)}" # Converts the dictionary to a URL query string and appends it to the base URL

    try: # try to download the pages
        print(f"Fetching rows {offset} to {offset + PAGE_SIZE}...") # print for progress
        with urllib.request.urlopen(url_mod, context=context) as response:
            raw_data = json.loads(response.read().decode()) # read JSON data from the API response and decode it into a Python dictionary

            data_page = raw_data["response"]["data"]

            if not data_page:
                has_more_data = False
                break

            # Filter for just 'Demand' (type 'D') to avoid mixing with generation/interchange
            demand_only = [row for row in data_page if row.get("type") == "D"]
            all_records.extend(demand_only)

            # Move window forward
            offset += PAGE_SIZE

            # A pause to avoid spamming the government server
            time.sleep(0.5)

    except Exception as e:
        print(f"Error encountered at offset {offset}: {e}")
        break

print(f"\nData harvest complete. Total hourly demand rows captured: {len(all_records)}")

# Export to CSV
if all_records:
    # Extract keys for the CSV header based on the first record
    headers = [
        "period",
        "respondent",
        "respondent-name",
        "type-name",
        "value",
        "value-units",
    ]

    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for row in all_records:
            # write only the columns
            writer.writerow({k: row.get(k, "") for k in headers})

    print(f"Success! File saved to your directory as: {OUTPUT_CSV}")
else:
    print("No data records were compiled. CSV file not created.")