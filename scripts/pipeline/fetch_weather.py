import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import time

API_KEY = "745266e7a2224532b54174149262504"
LOCATION = "Bangalore"
START_DATE = "2021-01-03" # Aligning with our Week 1
END_DATE = "2023-12-31"

def fetch_weather():
    start_dt = datetime.strptime(START_DATE, "%Y-%m-%d")
    end_dt = datetime.strptime(END_DATE, "%Y-%m-%d")
    
    current_dt = start_dt
    weather_records = []
    
    print(f"Fetching weather data from weatherapi.com for {LOCATION}...", flush=True)
    
    while current_dt <= end_dt:
        date_str = current_dt.strftime("%Y-%m-%d")
        url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={LOCATION}&dt={date_str}"
        
        success = False
        for attempt in range(3):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    day_data = data['forecast']['forecastday'][0]['day']
                    weather_records.append({
                        'ds': date_str,
                        'temp': day_data['avgtemp_c'],
                        'rain': day_data['totalprecip_mm']
                    })
                    if len(weather_records) % 30 == 0:
                        print(f"Progress: Fetched {len(weather_records)} days...", flush=True)
                    success = True
                    break
                else:
                    print(f"Error on {date_str} (Attempt {attempt+1}): {response.status_code} - {response.text}", flush=True)
                    if response.status_code == 400: # Limit reached
                        break
            except Exception as e:
                print(f"Attempt {attempt+1} failed on {date_str}: {e}", flush=True)
                time.sleep(1) # Wait before retry
        
        if not success and response.status_code == 400:
            print("Stopping due to API limits or range error.", flush=True)
            break
            
        current_dt += timedelta(days=1)
        # Sleep slightly to be polite to API
        time.sleep(0.01)

    if weather_records:
        df = pd.DataFrame(weather_records)
        output_path = os.path.join("data", "processed", "weather_data.csv")
        df.to_csv(output_path, index=False)
        print(f"Successfully saved {len(df)} days of weather data to {output_path}")
    else:
        print("No weather data fetched.")

if __name__ == "__main__":
    if not os.path.exists(os.path.join("data", "processed")):
        os.makedirs(os.path.join("data", "processed"))
    fetch_weather()
