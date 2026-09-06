import os
import json
import time
from datetime import datetime
import requests
import boto3
from dotenv import load_dotenv

# .env file se variables load karein
load_dotenv()

def fetch_and_upload_to_s3():
    # Credentials
    username = os.getenv("OPENSKY_USERNAME")
    password = os.getenv("OPENSKY_PASSWORD")
    bucket_name = os.getenv("S3_BUCKET_NAME")
    
    url = "https://opensky-network.org/api/states/all"
    print("Fetching live data from OpenSky API...")
    
    try:
        # 1. Fetch Data
        if username and password:
            response = requests.get(url, auth=(username, password), timeout=15)
        else:
            response = requests.get(url, timeout=15)
            
        response.raise_for_status()
        data = response.json()
        
        # 2. Connect to S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )
        
        # 3. Create Partitioned Path (Medallion Architecture standard)
        now = datetime.utcnow()
        folder_path = f"raw/opensky/year={now.year}/month={now.month:02d}/day={now.day:02d}/hour={now.hour:02d}"
        file_name = f"states_{int(time.time())}.json"
        s3_key = f"{folder_path}/{file_name}"
        
        # 4. Upload to S3
        print(f"Uploading data to S3 bucket '{bucket_name}'...")
        print(f"Path: {s3_key}")
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        
        print("✅ Success! Raw data saved to Bronze Landing Zone.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_upload_to_s3()