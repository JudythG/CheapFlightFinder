from data_manager import DataManager
from flight_search import FlightSearch
from text_manager import TextManager

flight_searcher = FlightSearch()
doc_manager = DataManager()
places_to_visit = doc_manager.get_to_visit_data()
places_dict = {place['city']: place for place in places_to_visit}

for location in places_to_visit:
    if not location['iataCode']:
        iata = flight_searcher.get_iata(location['city'])
        if iata:
            doc_manager.set_iata(location['id'], iata)
            location['iataCode'] = iata

text_message = ""
all_iata_codes = ','.join([f"{location['iataCode']}" for location in places_to_visit])
if all_iata_codes:
    flights = flight_searcher.get_flights(all_iata_codes, "LON")
    for flight in flights:
        if flight.price < places_dict[flight.destination_city]['lowestPrice']:
            text_message += f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-" \
                            f"{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport} " \
                            f"from {flight.out_date} to {flight.return_date}\n\n"

if text_message:
    texter = TextManager()
    texter.send_message(text_message)
