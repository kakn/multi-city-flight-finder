# multi-city-flight-finder
multi-city-flight-finder is a proof of concept that finds the cheapest flights for travelers from different cities who need to reach a common destination. It considers all options, including flying directly to each other or meeting at an intermediate location, to minimize total cost.

## Features
- Optimizes flight costs for multiple travelers from different origins.
- Evaluates all possible meeting points, not just direct routes.
- Ensures reasonable arrival time synchronization.
```
python flight_finder.py origin1 origin2 [originN] [num_days]
```
* `origin1 origin2 ...` → Departure cities.

* `[num_days] (optional)` → Search duration (default: 30 days).

Requires a CSV file with flight data (FLIGHT_DATA_FILE env variable or flight_data.csv), as public flight APIs are expensive.
The initial plan was to add Google Flights web scraping, but the project idea has already been implemented elsewhere.