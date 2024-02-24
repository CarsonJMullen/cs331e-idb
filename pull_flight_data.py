import datetime
import requests
from dotenv import load_dotenv
import os

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
    return response


