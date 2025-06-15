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
        self.site_id = "740000001"  # Ålidhem Centrum, Umeå
        
        # Headers for the API request
        self.headers = {
            'accept': 'application/json'
        }

    def get_departures(self):
        """Get departures from Ålidhem Centrum."""
        try:
            logging.info("Hämtar avgångar från Ålidhem Centrum...")
            
            # Construct the URL with site ID and API key
            url = f"{self.base_url}/{self.site_id}?key={self.api_key}"
            
            logging.info(f"Skickar API-anrop till {url}")
            
            # Make the API request
            response = requests.get(
                url,
                headers=self.headers
            )

            # Log the response status
            logging.info(f"API-svar status: {response.status_code}")
            
            # Check if the request was successful
            response.raise_for_status()

            # Parse the response
            data = response.json()
            logging.info("Fick svar från API och parsade det")
            
            # Process and format the data
            departures = self._process_departures(data)
            
            # Save the data
            self._save_data(departures)
            
            return departures

        except requests.exceptions.RequestException as e:
            logging.error(f"API-anrop misslyckades: {str(e)}")
            if hasattr(e.response, 'text'):
                logging.error(f"Svar från API: {e.response.text}")
            return None
        except Exception as e:
            logging.error(f"Fel vid hämtning av avgångar: {str(e)}")
            return None

    def _process_departures(self, data):
        """Process the raw API response into a structured format."""
        try:
            processed_data = {
                "hållplats": "Ålidhem Centrum",
                "tidpunkt": datetime.now().isoformat(),
                "avgångar": []
            }
            
            # Process each departure in the response
            if 'departures' in data:
                for departure in data['departures']:
                    departure_info = {
                        "linje": departure.get('line', ''),
                        "destination": departure.get('destination', ''),
                        "avgångstid": departure.get('time', ''),
                        "spår": departure.get('track', ''),
                        "realtid": departure.get('realtime', False),
                        "inställd": departure.get('cancelled', False)
                    }
                    processed_data["avgångar"].append(departure_info)
                logging.info(f"Processade {len(processed_data['avgångar'])} avgångar")
            else:
                logging.warning("Inga avgångar hittades i svaret")
            
            return processed_data
            
        except Exception as e:
            logging.error(f"Fel vid bearbetning av avgångar: {str(e)}")
            return None

    def _save_data(self, data):
        """Save the processed data to a JSON file."""
        if not data:
            return
            
        filename = f"avgångar_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"Data sparad till {filename}")
        except Exception as e:
            logging.error(f"Fel vid sparande av data: {str(e)}")

def main():
    """Main function to fetch bus times."""
    try:
        fetcher = BusTimesFetcher()
        fetcher.get_departures()
    except Exception as e:
        logging.error(f"Ett oväntat fel uppstod: {str(e)}")

if __name__ == "__main__":
    main() 