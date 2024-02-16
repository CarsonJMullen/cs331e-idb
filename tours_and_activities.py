import requests
import urllib3
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


url = 'https://test.api.amadeus.com/v1//shopping/activities'
params = {'latitude': 30.2672, 'longitude': -97.7431}
headers = {'Authorization': 'Bearer 1BBevbGfPFULnhklLRcEvAxB8J0D'}

response = requests.get(url, params=params, headers=headers, verify=False)



response_json = response.json()


file_path = 'data/Tours_and_Activities.json'

# Write the JSON data to the file
with open(file_path, 'w') as file:
    json.dump(response_json, file, indent=4)

print(f"JSON data saved to {file_path}")