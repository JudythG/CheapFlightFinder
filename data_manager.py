import requests
import os


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    # https://docs.google.com/spreadsheets/d/1yTkIwqWyMFzKOfweSYqSxYkZO-qb7YZJTehMMsZJ5RQ/edit#gid=0

    def __init__(self):
        self.sheety_endpoint = "https://api.sheety.co"
        self.sheety_key = os.environ.get("SHEETY_KEY")

    def get_to_visit_data(self):
        endpoint = f"{self.sheety_endpoint}/{self.sheety_key}/flightDeals/prices"
        response = requests.get(url=endpoint)
        response.raise_for_status()
        return response.json()['prices']

    def set_iata(self, id, iata_code):
        endpoint = f"{self.sheety_endpoint}/{self.sheety_key}/flightDeals/prices/{id}"
        body = {
            "price": {
                "iataCode": iata_code
            }
        }
        response = requests.put(url=endpoint, json=body)
        response.raise_for_status()

    def set_price(self, id, price):
        endpoint = f"{self.sheety_endpoint}/{self.sheety_key}/flightDeals/prices/{id}"
        body = {
            "price": {
                "lowest_price": price
            }
        }
        response = requests.put(url=endpoint, json=body)
        response.raise_for_status()
