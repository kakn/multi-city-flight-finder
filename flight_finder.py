import sys
import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict
from itertools import product
from gen_data import cities

class FlightFinder:
    def __init__(self, flight_data_file):
        self.flights = self._load_flight_data(flight_data_file)
        self.dep_date = datetime.now() + timedelta(days=30)
        self.max_wait_time = timedelta(hours=2)

    @staticmethod
    def _load_flight_data(filename):
        flights = defaultdict(list)
        try:
            with open(filename, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    flights[(row["Source"], row["Destination"])].append(row)
        except Exception as e:
            print(f"Error reading flight data: {e}")
            sys.exit(1)
        return flights

    @staticmethod
    def _combine_date_time(date, time):
        return datetime.combine(date.date(), datetime.strptime(time, "%H:%M").time())

    def find_cheapest_combination(self, traveler_origins, travelers_flights):
        cheapest_combination = {"Flights": [None] * len(travelers_flights), "Price": float('inf')}

        for flights_combination in product(*travelers_flights):
            arrival_times = []
            total_price = 0
            omitted_price = 0
            omitted_index = -1

            for i, (traveler_origin, flight) in enumerate(zip(traveler_origins, flights_combination)):
                if traveler_origin != flight["Destination"]:
                    arrival_time = self._combine_date_time(self.dep_date, flight["Arrival_Time"])
                    arrival_times.append(arrival_time)
                    total_price += int(flight["Price"])
                else:
                    arrival_times.append(None)
                    omitted_price = int(flight["Price"])
                    omitted_index = i

            if len(traveler_origins) == 1 or all(arrival_time is None or arrival_time.date() == self.dep_date.date() for arrival_time in arrival_times):
                non_none_arrival_times = [arrival_time for arrival_time in arrival_times if arrival_time is not None]

                if non_none_arrival_times:
                    max_arrival_time = max(non_none_arrival_times)
                    min_arrival_time = min(non_none_arrival_times)
                    time_diff = max_arrival_time - min_arrival_time

                    if len(traveler_origins) == 1 or (timedelta(0) <= time_diff <= self.max_wait_time) and total_price - omitted_price < cheapest_combination["Price"]:
                        cheapest_combination = {
                            "Flights": flights_combination,
                            "Price": total_price - omitted_price,
                            "OmittedIndex": omitted_index,
                            "DepDate": self.dep_date
                        }

        return None if cheapest_combination["Price"] == float('inf') else cheapest_combination

    def find_cheapest_vacations(self, traveler_origins, num_days):
        cheapest_vacations = []
        start_date = datetime.now()
        end_date = start_date + timedelta(days=num_days)

        for dep_date in (start_date + timedelta(days=n) for n in range(num_days)):
            self.dep_date = dep_date
            added_destinations = set()

            for dest in cities:
                travelers_flights = [self.flights[(origin, dest)] for origin in traveler_origins]
                cheapest_combination = self.find_cheapest_combination(traveler_origins, travelers_flights)

                if cheapest_combination is not None:
                    if (dest, self.dep_date.date()) in added_destinations:
                        continue
                    added_destinations.add((dest, self.dep_date.date()))

                    cheapest_vacations.append({
                        "Destination": dest,
                        "Flights": cheapest_combination["Flights"],
                        "Price": cheapest_combination["Price"],
                        "DepDate": cheapest_combination["DepDate"]
                    })
        return sorted(cheapest_vacations, key=lambda v: v["Price"])

    def display_cheapest_vacations(self, cheapest_vacations, num_results=10):
        if len(cheapest_vacations) > 0:
            print("Cheapest vacations for the travelers:")
            print("-" * 80)
            for vacation in cheapest_vacations[:num_results]:
                print(f"Destination: {vacation['Destination']}")
                print(f"Total price for all travelers: {vacation['Price']}")

                for i, flight in enumerate(vacation["Flights"]):
                    print(f"\nTraveler {i + 1}:")
                    if flight is None:
                        print(f"  No flight needed, already in the destination city.")
                        print(f"  Price: 0")
                    else:
                        print(f"  Flight: {flight['Source']} to {flight['Destination']}")
                        print(f"  Departure date: {vacation['DepDate'].date()}")
                        print(f"  Departure time: {flight['Dep_Time']}")
                        print(f"  Arrival time: {flight['Arrival_Time']}")
                        print(f"  Price: {flight['Price']}")
                print("-" * 80)
        else:
            print("No vacations found.")


if __name__ == "__main__":
    # Check for environment variable for flight data file or default to "flight_data.csv"
    flight_data_file = os.environ.get("FLIGHT_DATA_FILE", "data/flight_data.csv")

    # Create FlightFinder instance
    finder = FlightFinder(flight_data_file)

    # Get traveler origin cities from command-line arguments
    if len(sys.argv) < 2:
        print("Please provide at least one origin city as a command-line argument.")
        sys.exit(1)

    # Assuming the last argument could be num_days
    try:
        num_days = int(sys.argv[-1])
        traveler_origins = sys.argv[1:-1]  # All arguments except the last one
    except ValueError:
        num_days = 30  # Default value if last argument is not a number
        traveler_origins = sys.argv[1:]  # All arguments
    
    cheapest_vacations = finder.find_cheapest_vacations(traveler_origins, num_days)
    finder.display_cheapest_vacations(cheapest_vacations)
