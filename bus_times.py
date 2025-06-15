import os
import json
import logging
from datetime import datetime
import requests
from dotenv import load_dotenv

# Configure logging
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
        self.api_key = os.getenv('TRAFIKLAB_API_KEY')
        if not self.api_key:
            raise ValueError("TRAFIKLAB_API_KEY not found in .env file")
        
        # Load settings
        self.load_settings()
        
        # Prepare headers for API request
        self.headers = {
            'Accept': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key
        }

    def load_settings(self):
        """Load settings from settings.txt file."""
        try:
            with open('settings.txt', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=')
                        if key == 'SITE_ID':
                            self.site_id = value
                            break
            if not hasattr(self, 'site_id'):
                raise ValueError("SITE_ID not found in settings.txt")
        except FileNotFoundError:
            raise FileNotFoundError("settings.txt not found")
        except Exception as e:
            raise ValueError(f"Error reading settings.txt: {e}")

    def get_departures(self):
        """Fetch departures from the API."""
        try:
            # Log the start of the process
            logging.info(f"Fetching departures from Ålidhem Centrum...")
            
            # Construct the API URL
            url = f"https://realtime-api.trafiklab.se/v1/departures/{self.site_id}"
            logging.info(f"Sending API request to {url}")
            
            # Make the API request
            response = requests.get(url, headers=self.headers)
            logging.info(f"API response status: {response.status_code}")
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            logging.info("Received and parsed API response")
            
            # Save raw data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            raw_filename = f"departures_{timestamp}.json"
            with open(raw_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"Raw data saved to {raw_filename}")
            
            # Save processed data
            processed_filename = f"processed_departures_{timestamp}.json"
            with open(processed_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"Processed data saved to {processed_filename}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching departures: {e}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing API response: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

def main():
    try:
        fetcher = BusTimesFetcher()
        fetcher.get_departures()
    except Exception as e:
        logging.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    main() 