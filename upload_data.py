
import json
import requests
import time

# Load collected data
with open('collected_members_full_20250706_162026.json', 'r') as f:
    members = json.load(f)

# Upload to production API
production_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

# Trigger member update to ensure fresh data
print("Triggering production member update...")
response = requests.post(f"{production_url}/api/v1/update/members", json={"force_refresh": True})
print(f"Update response: {response.status_code} - {response.text}")

# Wait for processing
time.sleep(60)

# Check final stats
response = requests.get(f"{production_url}/api/v1/stats/database")
if response.status_code == 200:
    stats = response.json()
    print(f"Final database stats: {stats}")
else:
    print(f"Error getting stats: {response.text}")
