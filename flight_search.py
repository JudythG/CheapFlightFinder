import requests
import os
from datetime import date, timedelta
from flight_data import FlightData


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.api_key = os.environ.get("TEQUILA_API_KEY")
        self.tequila_url = "https://tequila-api.kiwi.com"
        self.header = {
            "apikey": self.api_key
        }
        self.date_format = "%d/%m/%Y"

    def get_iata(self, city):
        endpoint = f"{self.tequila_url}/locations/query"
        parameters = {
            "term": city,
            "locale": "en-US",
            "location_types": "city",
            "active_only": "true",
        }
        response = requests.get(url=endpoint, params=parameters, headers=self.header)
        response.raise_for_status()
        if len(response.json()['locations']):
            return response.json()['locations'][0]['code']
        else:
            return None

    def get_flights(self, fly_to, fly_from):
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(weeks=24)
        endpoint = f"{self.tequila_url}/v2/search"
        parameters = {
            "fly_from": f"city:{fly_from}",
            "fly_to": f"city:{fly_to}",
            "date_from": start_date.strftime(self.date_format),
            "date_to": end_date.strftime(self.date_format),
            "only_working_days": "false",
            "only_weekends": "false",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=endpoint, params=parameters, headers=self.header)
        response.raise_for_status()
        flights = [FlightData(data['price'], data['cityFrom'], data['flyFrom'], data['cityTo'],
                   data['flyTo'], data['local_arrival'], data['local_departure']) for data in
                   response.json()['data']]
        return flights
