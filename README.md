# NärGårDen?

A real-time bus departure display system using the Trafiklab API. This application can display departures for any station supported by the Trafiklab API.

## Features

- Real-time bus departure information
- Support for any station in the Trafiklab API
- Automatic data refresh every 10 minutes
- Full-screen mode
- Countdown timers for each departure

## Setup

1. Create a `.env` file in the project root with your Trafiklab API key:
```
TRAFIKLAB_API_KEY=your_api_key_here
```
You get this by visiting the [Trafiklab's developer website](https://developer.trafiklab.se/)
and signing up a developer account.

2. Create a `settings.txt` file with your station ID and how many departures you want displayed:
```
# Trafiklab API Settings
SITE_ID=your_station_id_here
DEPARTURES_TO_SHOW=XX
```

You can find your station ID by:
1. Going to [Trafiklab's API documentation](https://www.trafiklab.se/api/our-apis/trafiklab-realtime-apis/openapi-specification/#/Stop%20lookup/get_stops_name__searchValue_)
2. Use their get stops lookup function.
3. Enter your api-key and your station and it will search for it.
4. Hopefully, you will have it by now.

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Run the display:
```bash
python bus_display.py
```

The display will automatically:
- Fetch initial data
- Update every 10 minutes
- Show countdown timers
- Display the next 3 departures for each platform

## Controls

- Press `ESC` to exit the display

## Files

- `bus_times.py`: Fetches data from the Trafiklab API
- `process_departures.py`: Processes the raw API data
- `bus_display.py`: Displays the departures in a visual interface
- `settings.txt`: Configuration file for station ID
- `.env`: Contains your Trafiklab API key

## Data Files

The application creates several JSON files:
- `departures_*.json`: Raw API response
- `processed_departures_*.json`: Processed departure data
- `departure_lists/platform_departures.json`: Platform-specific departure lists

## License

MIT License
