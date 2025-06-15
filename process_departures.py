import os
import json
from datetime import datetime
import glob

def get_latest_processed_file():
    """Get the most recent processed departures file."""
    files = glob.glob('processed_departures_*.json')
    if not files:
        raise FileNotFoundError('No processed departures files found')
    
    # Sort files by name (which includes timestamp) in descending order
    files.sort(reverse=True)
    return files[0]

def create_platform_lists(departures):
    """Create departure lists for each platform."""
    # Create a dictionary to store departures by platform
    platform_map = {}

    # Group departures by platform
    for departure in departures:
        if departure.get('cancelled'):
            continue  # Skip cancelled departures

        platform = departure.get('platform_designation', 'Unknown')
        if platform not in platform_map:
            platform_map[platform] = []

        platform_map[platform].append({
            'route': departure['route_designation'],
            'time': departure['scheduled_time'],
            'direction': departure['direction']
        })

    # Sort departures by time for each platform
    for platform in platform_map:
        platform_map[platform].sort(key=lambda x: x['time'])

    return platform_map

def process_latest_departures():
    """Process the latest departures file and create platform-specific lists."""
    try:
        # Get the latest file
        latest_file = get_latest_processed_file()
        print(f"Processing file: {latest_file}")

        # Read and parse the JSON file
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Create the platform lists
        platform_lists = create_platform_lists(data['departures'])

        # Create output directory if it doesn't exist
        os.makedirs('departure_lists', exist_ok=True)

        # Save the platform lists
        output = {
            'timestamp': data['timestamp'],
            'platforms': platform_lists
        }

        output_file = 'departure_lists/platform_departures.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Created platform departures file: {output_file}")

        # Print the lists in a readable format
        print('\nNext departures:')
        for platform, departures in platform_lists.items():
            print(f"\nPlatform {platform}:")
            for dep in departures:
                print(f"{dep['route']}: {dep['time']}")

    except Exception as error:
        print(f"Error processing departures: {error}")

if __name__ == "__main__":
    process_latest_departures() 