import requests
import json

url = "https://test.api.amadeus.com/v1/shopping/activities"
api_key = 'e5pd5XDbDysJaKQ7si7sGgUKndrJEWtG'
api_secret = 'CeP96YiqKm8WA7fr'

# Request an access token
token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
token_data = {
    'client_id': api_key,
    'client_secret': api_secret,
    'grant_type': 'client_credentials'
}

token_response = requests.post(token_url, data=token_data)
access_token = token_response.json()['access_token']

# Make the request to the API using the access token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Cities
cities = {
    'BER': {'latitude': '52.5200', 'longitude': '13.4050', 'city': 'Berlin'},
    'NYC': {'latitude': '40.7306', 'longitude': '-73.9352', 'city': 'New York'},
    'PAR': {'latitude': '48.8566', 'longitude': '2.3522', 'city': 'Paris'},
    'ROM': {'latitude': '41.9028', 'longitude': '12.4964', 'city': 'Rome'},
    'CPT': {'latitude': '-33.9249', 'longitude': '18.4241', 'city': 'Cape Town'},
    'SYD': {'latitude': '-33.8688', 'longitude': '151.2093', 'city': 'Sydney'},
    'AMS': {'latitude': '52.3676', 'longitude': '4.9041', 'city': 'Amsterdam'},
    "LON": {'latitude': '51.5072', 'longitude': '-0.1276', 'city': 'London'},
    "BCN": {'latitude': '41.3874', 'longitude': '2.1686', 'city': 'Barcelona'},
    'MEX': {'latitude': '19.4326', 'longitude': '-99.1332', 'city': 'Mexico City'},
    'MRS': {'latitude': '43.2965', 'longitude': '5.3698', 'city': 'Marseille'},
    'MAD': {'latitude': '40.4168', 'longitude': '-3.7038', 'city': 'Madrid'},
}

# Filter to remove activities with no price or review
def filterMissing(n):
    try:
        if n['price']['amount'] == "0.0":
            return False
        elif "my tests in different languages" in n['name']:
            return False
    except:
        return False
    return True

total = 0
final = {'data': []}
for i in cities: #[0:1]:
    # Parameters to be included in the request
    params = {
        'latitude': cities[i]['latitude'],  # Latitude for New York City
        'longitude': cities[i]['longitude'],  # Longitude for New York City
        'radius': '20',  # Radius in kilometers
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()['data']

    data = filter(filterMissing, data)

    added = 0
    for j in data:
        j['city'] = cities[i]['city']
        j['iataCode'] = i
        final['data'].append(j)
        added += 1
        total += 1

    if added:
        print(cities[i]['city'], 'done', added)

print(total)

file_path = 'static/data/activities/activity_list.json'

# Write the JSON data to the file
with open(file_path, 'w') as file:
    json.dump(final, file, indent=4)

print(f"JSON data saved to {file_path}")
