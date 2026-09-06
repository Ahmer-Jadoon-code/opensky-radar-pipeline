import requests
import json
import os
from dotenv import load_dotenv

# .env file se variables load karein
load_dotenv()

def fetch_live_flights():
    # Credentials ko variables mein store karein
    username = os.getenv("OPENSKY_USERNAME")
    password = os.getenv("OPENSKY_PASSWORD")
    
    url = "https://opensky-network.org/api/states/all"
    print(f"Fetching live data from {url}...\n")
    
    try:
        # requests.get mein auth parameter add kar diya hai
        if username and password:
            print("Using authenticated access...")
            response = requests.get(url, auth=(username, password), timeout=10)
        else:
            print("Using anonymous access (No credentials found)...")
            response = requests.get(url, timeout=10)
            
        response.raise_for_status() 
        
        data = response.json()
        states = data.get('states', [])
        
        if states:
            print(f"✅ Success! Retrieved live data for {len(states)} flights.")
            print("-" * 50)
            print("Sample data for the very first flight in the list:")
            print(json.dumps(states[0], indent=4))
        else:
            print("API hit successful, but no flight states returned.")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")

if __name__ == "__main__":
    fetch_live_flights()