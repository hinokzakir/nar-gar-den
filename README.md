# NärGårDen?

A Python script that fetches real-time bus departure information from Ålidhem Centrum in Umeå using the Trafiklab API. Meant for displaying on a screen in your room.

## Requirements

- Python 3.8 or higher
- Trafiklab API key
- Internet connection

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Trafiklab API key:
```
TRAFIKLAB_API_KEY=your_api_key_here
```

## Usage

Run the script:
```bash
python bus_times.py
```

The script will:
- Fetch current departures from Ålidhem Centrum
- Save the information in a timestamped JSON file
- Create a log file (bus_times.log) with information about the execution

## Output

The script creates JSON files with the following naming convention:
`avgångar_YYYYMMDD_HHMM.json`

Each file contains:
- Stop name
- Timestamp of data retrieval
- List of departures including:
  - Line number
  - Destination
  - Departure time
  - Track
  - Real-time information
  - Cancelled departures

## Logging

The script logs all operations to both:
- Console output
- `bus_times.log` file

## Note

This script uses the Trafiklab API. Please respect their terms of service and rate limits.
