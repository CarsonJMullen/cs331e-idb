import requests
import urllib3
import json
# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

access_token = "RG6h6rMnrdbhkrcBT88Wfcn2xUeu"
headers = {'Authorization': f'Bearer {access_token}'}



url = 'https://test.api.amadeus.com/v1//shopping/activities'

cities = {
    "austin": {'latitude': 30.2672, 'longitude': -97.7431},
    "dallas": {'latitude': 32.7767, 'longitude': -96.7970},
    "bangalore": {'latitude': 12.9716, 'longitude': 77.5946},
    "barcelona": {'latitude': 41.3874, 'longitude': 2.1686},
    "berlin": {'latitude': 52.5200, 'longitude': 13.4050},
    "london": {'latitude': 51.5072, 'longitude': -0.1276},
    "new_york": {'latitude': 40.7306, 'longitude': -73.9352},
    "paris": {'latitude': 48.8566, 'longitude': 2.3522},
    "san_francisco": {'latitude': 37.7749, 'longitude': -122.4194}
}

def get_data(city_name):
    global cities
    response = requests.get(url, params=cities[city_name], headers=headers, verify=False)
    response_json = response.json()

    file_path = f'data/tours_and_activities_{city_name}.json'

    # Write the JSON data to the file
    with open(file_path, 'w') as file:
        json.dump(response_json, file, indent=4)

    print(f"JSON data saved to {file_path}")

#get_data("austin")
get_data("dallas")