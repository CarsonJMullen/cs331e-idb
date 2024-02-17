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
cities = [
    {
        'city': 'Bangalore',
        'latitude': '12.9716',
        'longitude': '77.5946'
    },
    {
        'city': 'Barcelona',
        'latitude': '41.3874',
        'longitude': '2.1686'
    },
    {
        'city': 'Berlin',
        'latitude': '52.5200',
        'longitude': '13.4050'
    },
    {
        'city': 'Dallas',
        'latitude': '32.7767',
        'longitude': '-96.7970'
    },
    {
        'city': 'London',
        'latitude': '51.5072',
        'longitude': '-0.1276'
    },
    {
        'city': 'New York',
        'latitude': '40.7306',
        'longitude': '-73.9352'
    },
    {
        'city': 'Paris',
        'latitude': '48.8566',
        'longitude': '2.3522'
    },
    {
        'city': 'San Francisco',
        'latitude': '37.7749',
        'longitude': '-122.4194'
    }
]

# Filter to remove activities with no price or review
def filterMissing(n):
    try:
        if n['price']['amount'] == "0.0":
            return False
        else:
            p = n['rating']
            return True
    except:
        return False

final = {'data': []}
for i in cities: #[0:1]:
    # Parameters to be included in the request
    params = {
        'latitude': i['latitude'],  # Latitude for New York City
        'longitude': i['longitude'],  # Longitude for New York City
        'radius': '20',  # Radius in kilometers
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()['data']

    data = filter(filterMissing, data)

    for j in data:
        j['city'] = i['city']
        final['data'].append(j)

    print(i['city'], 'done')


file_path = 'data/activities_multiple_cities.json'

# Write the JSON data to the file
with open(file_path, 'w') as file:
    json.dump(final, file, indent=4)

print(f"JSON data saved to {file_path}")
