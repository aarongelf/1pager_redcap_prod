from redcap import Project
import os
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

REDCAP_URL = os.getenv("REDCAP_URL")
project_id = ["PID_001", "PID_002"] # Change for appropriate PID

for pid in project_id:
    API_TOKEN = os.getenv(f"{pid}_TOKEN")
    if not API_TOKEN:
        print(f"No API token found for {pid}. Skipping.")
        continue

    print(f"Fetching data for {pid}...")

    project = Project(REDCAP_URL, API_TOKEN)

    try:
        records = project.export_records()
        df = pd.DataFrame(records)

        df.to_json(f"../data/{pid.lower()}_data.json", indent=2)
        df.to_csv(f"../data/{pid.lower()}_data.csv", index=False)

        print(f"Fetched and saved data for {pid}")
    except Exception as e:
        print(f"Failed to fetch {pid}: {e}")