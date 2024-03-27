import datetime
import requests
from dotenv import load_dotenv
import os
import json

def configure():
    load_dotenv()

def get_flight_data(destination, start = "AUS", date = datetime.date.today().strftime("%Y-%m-%d")):
    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={start}&destinationLocationCode={destination}&departureDate={date}&adults=1&nonStop=false&max=250"

    # Request an access token
    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    token_data = {
        'client_id': os.getenv('api_key'),
        'client_secret': os.getenv('api_secret'),
        'grant_type': 'client_credentials'
    }

    token_response = requests.post(token_url, data=token_data)
    access_token = token_response.json()['access_token']

    # Make the request to the API using the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    return response.json()

cities = {
    'BER': {'latitude': '52.5200', 'longitude': '13.4050', 'city': 'Berlin'},
    'NYC': {'latitude': '40.7306', 'longitude': '-73.9352', 'city': 'New York'},
    'PAR': {'latitude': '48.8566', 'longitude': '2.3522', 'city': 'Paris'},
    'FCO': {'latitude': '41.9028', 'longitude': '12.4964', 'city': 'Rome'},
    'CPT': {'latitude': '-33.9249', 'longitude': '18.4241', 'city': 'Cape Town'},
    'SYD': {'latitude': '-33.8688', 'longitude': '151.2093', 'city': 'Sydney'},
    'AMS': {'latitude': '52.3676', 'longitude': '4.9041', 'city': 'Amsterdam'},
    "LON": {'latitude': '51.5072', 'longitude': '-0.1276', 'city': 'London'},
    "BCN": {'latitude': '41.3874', 'longitude': '2.1686', 'city': 'Barcelona'},
    'MEX': {'latitude': '19.4326', 'longitude': '-99.1332', 'city': 'Mexico City'},
    'MRS': {'latitude': '43.2965', 'longitude': '5.3698', 'city': 'Marseille'},
    'MAD': {'latitude': '40.4168', 'longitude': '-3.7038', 'city': 'Madrid'},
}

for city in cities.keys():
    data = get_flight_data(city, "AUS", date='2024-05-13')
    date = '2024-05-13'
    file_path = os.path.join('webpage', 'static', 'data', 'flights', city + '-' + date + ".json")
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


