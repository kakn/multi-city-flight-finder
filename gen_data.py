import csv
import random
from datetime import datetime, timedelta, time

# define the list of cities
cities = ['Bangkok', 'Dubai', 'Paris', 'London', 'New York City', 
          'Kuala Lumpur', 'Istanbul', 'Tokyo', 'Antalya', 'Seoul', 
          'Phuket', 'Mecca', 'Hong Kong', 'Milan', 'Barcelona', 
          'Pattaya', 'Bali', 'Osaka', 'Rome', 'Taipei', 'Shenzhen', 
          'Vienna', 'Prague', 'Dublin', 'Mumbai', 'Amsterdam', 
          'Ho Chi Minh City', 'Berlin', 'Moscow', 'Munich', 'Madrid', 
          'Beijing', 'Toronto', 'Zurich', 'Vancouver', 'Los Angeles', 
          'Miami', 'San Francisco', 'Sydney', 'Athens', 'Melbourne', 
          'Edinburgh', 'Florence', 'Krakow', 'Budapest', 'Cairo', 
          'Lisbon', 'Brussels', 'Copenhagen', 'Stockholm', 'Helsinki']

def generate_flight_data(num_rows: int = 100000, output_file: str = "data/flight_data.csv"):
    """
    Generates random flight data and writes it to a CSV file.

    Parameters:
        num_rows (int): The number of rows of flight data to generate.
        output_file (str): The name of the output file.
    """
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)

        # write the header row
        writer.writerow([
            "Date_of_Journey",
            "Source",
            "Destination",
            "Dep_Time",
            "Arrival_Time",
            "Duration",
            "Price"
        ])

        # generate random flight data
        for i in range(num_rows):
            # choose a random source and destination
            source, dest = random.sample(cities, 2)

            # generate a random date and time for departure
            dep_date = datetime.now() + timedelta(days=random.randint(1, 365))
            dep_time = time(random.randint(0, 23), random.randint(0, 59))
            dep_datetime = datetime.combine(dep_date, dep_time)

            # generate a random duration for the flight
            base_duration = random.randint(60, 600)
            duration_fluctuation = random.randint(-30, 30)  # +/- 30 minutes fluctuation
            duration = timedelta(minutes=base_duration + duration_fluctuation)

            # calculate the arrival time
            arrival_datetime = dep_datetime + duration

            # generate a random price for the flight and add fluctuations based on duration
            base_price = random.randint(50, 500)
            price_fluctuation = int(base_price * (duration_fluctuation / 600))
            price = base_price + price_fluctuation

            # write the row to the CSV file
            writer.writerow([
                dep_datetime.strftime("%Y-%m-%d"),
                source,
                dest,
                dep_datetime.strftime("%H:%M"),
                arrival_datetime.strftime("%H:%M"),
                str(duration),
                str(price)
            ])

def main():
    generate_flight_data()

if __name__ == "__main__":
    main()