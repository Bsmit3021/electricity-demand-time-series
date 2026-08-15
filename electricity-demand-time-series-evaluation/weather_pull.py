import csv
import json
import os
import ssl
import urllib.parse
import urllib.request

# Base Configuration — Open-Meteo Historical Weather API (no key required)
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
OUTPUT_CSV = "data/atlanta_hourly_weather_2years.csv"

# Atlanta / KATL coordinates
LATITUDE = 33.7490
LONGITUDE = -84.3880

# Same 2-year window as the demand pull (2024-05-01 to 2026-05-01)
START_DATE = "2024-05-01"
END_DATE = "2026-04-30"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": (
        "temperature_2m,"
        "apparent_temperature,"
        "dew_point_2m,"
        "relative_humidity_2m,"
        "precipitation,"
        "cloud_cover,"
        "wind_speed_10m"
    ),
    "temperature_unit": "fahrenheit",
    "precipitation_unit": "inch",
    "wind_speed_unit": "mph",
    "timezone": "UTC",  # IMPORTANT: matches EIA-930's UTC timestamps
}

url_mod = f"{BASE_URL}?{urllib.parse.urlencode(params)}"

context = ssl.create_default_context()

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

print(f"Fetching weather data for Atlanta from {START_DATE} to {END_DATE}...")

try:
    with urllib.request.urlopen(url_mod, context=context) as response:
        raw_data = json.loads(response.read().decode())

    hourly = raw_data["hourly"]
    timestamps = hourly["time"]
    temperature = hourly["temperature_2m"]
    apparent_temperature = hourly["apparent_temperature"]
    dew_point = hourly["dew_point_2m"]
    humidity = hourly["relative_humidity_2m"]
    precipitation = hourly["precipitation"]
    cloud_cover = hourly["cloud_cover"]
    wind_speed = hourly["wind_speed_10m"]

    row_count = len(timestamps)
    print(f"Retrieved {row_count} hourly records.")

    # Inclusive range: 730 days × 24 hours = 17,520 rows
    expected = 17520
    if row_count != expected:
        print(f"WARNING: expected {expected} rows, got {row_count} — check for gaps or date-range mismatch.")

    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "period",
            "temperature_f",
            "apparent_temperature_f",
            "dew_point_f",
            "relative_humidity_pct",
            "precipitation_in",
            "cloud_cover_pct",
            "wind_speed_mph",
        ])
        for i in range(row_count):
            writer.writerow([
                timestamps[i],
                temperature[i],
                apparent_temperature[i],
                dew_point[i],
                humidity[i],
                precipitation[i],
                cloud_cover[i],
                wind_speed[i],
            ])
    print(f"Success! File saved to: {OUTPUT_CSV}")

except Exception as e:
    print(f"An error occurred: {e}")
