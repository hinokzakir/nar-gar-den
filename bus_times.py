import os
import json
import logging
from datetime import datetime
import requests
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bus_times.log'),
        logging.StreamHandler()
    ]
)

class BusTimesFetcher:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment variable
        self.api_key = os.getenv('TRAFIKLAB_API_KEY')
        if not self.api_key:
            raise ValueError("TRAFIKLAB_API_KEY not found in environment variables")
        
        # Base URL for the Trafiklab API
        self.base_url = "https://realtime-api.trafiklab.se/v1/departures"
        
        # Site ID for Ålidhem Centrum in Umeå
        self.site_id = "740023156"  # Ålidhem Centrum, Umeå
        
        # Headers for the API request
        self.headers = {
            'accept': 'application/json'
        }

    def get_departures(self):
        """Get departures from Ålidhem Centrum."""
        try:
            logging.info("Fetching departures from Ålidhem Centrum...")
            
            # Construct the URL with site ID and API key
            url = f"{self.base_url}/{self.site_id}?key={self.api_key}"
            
            logging.info(f"Sending API request to {url}")
            
            # Make the API request
            response = requests.get(
                url,
                headers=self.headers
            )

            # Log the response status
            logging.info(f"API response status: {response.status_code}")
            
            # Check if the request was successful
            response.raise_for_status()

            # Parse the response
            data = response.json()
            logging.info("Received and parsed API response")
            
            # Save the raw data
            self._save_data(data)
            
            # Create processed data
            self._create_processed_data(data)
            
            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            if hasattr(e.response, 'text'):
                logging.error(f"API response: {e.response.text}")
            return None
        except Exception as e:
            logging.error(f"Error fetching departures: {str(e)}")
            return None

    def _save_data(self, data):
        """Save the raw API response to a JSON file."""
        if not data:
            return
            
        filename = f"departures_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"Raw data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving raw data: {str(e)}")

    def _create_processed_data(self, raw_data):
        """Create a new JSON file with processed departure information."""
        if not raw_data or 'departures' not in raw_data:
            return

        processed_data = {
            "timestamp": datetime.now().isoformat(),
            "departures": []
        }

        for departure in raw_data['departures']:
            departure_info = {
                "scheduled_time": departure.get('scheduled', ''),
                "cancelled": departure.get('cancelled', False),
                "route_designation": departure.get('route', {}).get('designation', ''),
                "platform_designation": departure.get('realtime_platform', {}).get('designation', '')
            }
            processed_data["departures"].append(departure_info)

        filename = f"processed_departures_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
            logging.info(f"Processed data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving processed data: {str(e)}")

def main():
    """Main function to fetch bus times."""
    try:
        fetcher = BusTimesFetcher()
        fetcher.get_departures()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main() 