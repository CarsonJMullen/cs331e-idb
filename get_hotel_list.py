import requests
import json

url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
api_key = 'IkqtmH4eNAbWiMzGwRxW1iHH3uwpyYxK'
api_secret = 'YGzAk2eZS3PrvR7k'

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
        'city': 'Berlin',
        'iataCode': 'BER'
    },
    {
        'city': 'New York',
        'iataCode': 'NYC'
    },
    {
        'city': 'Paris',
        'iataCode': 'PAR'
    },
    {
        'city': 'Rome',
        'iataCode': 'ROM'
    },
    {
        'city': 'London',
        'iataCode': 'LON'
    },
    {
        'city': 'Cape Town',
        'iataCode': 'CPT'
    },
    {
        'city': 'Sydney',
        'iataCode': 'SYD'
    },
    {
        'city': 'Amsterdam',
        'iataCode': 'AMS'
    },
    {
        'city': 'Barcelona',
        'iataCode': 'BCN'
    },
    {
        'city': 'Mexico',
        'iataCode': 'MEX'
    },
    {
        'city': 'Marseille',
        'iataCode': 'MRS'
    },
    {
        'city': 'Madrid',
        'iataCode': 'MAD'
    }
]

final = {'data': []}
for i in cities: #[0:1]:
    # Parameters to be included in the request
    params = {
        'cityCode': i['iataCode'],
        'radius': '25',  # Radius in kilometers
        'radiusUnit': 'KM',
        'amenities': 'AIR_CONDITIONING, WIFI, ROOM_SERVICE',
        'ratings': '3,4,5',
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()['data']

    for j in data:
        j['city'] = i['city']
        j['iataCode'] = i['iataCode']
        final['data'].append(j)

    print(i['iataCode'], 'done')


file_path = 'webpage/static/data/hotels/hotel_list.json'

# Write the JSON data to the file
with open(file_path, 'w') as file:
    json.dump(final, file, indent=4)

print(f"JSON data saved to {file_path}")