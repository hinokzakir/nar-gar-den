# NärGårDen?

A real-time bus departure display system using the Trafiklab API. This application can display departures for any station supported by the Trafiklab API.

## Features

- Real-time bus departure information
- Support for any station in the Trafiklab API
- Automatic data refresh every 10 minutes
- Pixelated Minecraft-style display
- Full-screen mode
- Countdown timers for each departure

## Setup

1. Create a `.env` file in the project root with your Trafiklab API key:
```
TRAFIKLAB_API_KEY=your_api_key_here
```

2. Create a `settings.txt` file with your station ID:
```
# Trafiklab API Settings
SITE_ID=your_station_id_here
```

You can find your station ID by:
1. Going to [Trafiklab's API documentation](https://www.trafiklab.se/api)
2. Looking up your station in their station list
3. Using the station's ID in the settings file

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
