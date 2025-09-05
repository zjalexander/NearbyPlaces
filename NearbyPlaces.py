import requests
import json
import time
from typing import List, Dict, Optional

class GooglePlacesNearbySearch:
    def __init__(self, api_key: str):
        """
        Initialize the Google Places API client
        
        Args:
            api_key (str): Your Google Maps API key
        """
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    def search_nearby(self, 
                     latitude: float, 
                     longitude: float, 
                     radius: int = 2650,
                     place_type: Optional[str] = None,
                     keyword: Optional[str] = None,
                     min_price: Optional[int] = None,
                     max_price: Optional[int] = None,
                     open_now: bool = False) -> List[Dict]:
        """
        Search for places near a specific location
        
        Args:
            latitude (float): Latitude of the center point
            longitude (float): Longitude of the center point
            radius (int): Search radius in meters (max 50000)
            place_type (str, optional): Type of place (e.g., 'restaurant', 'store', 'gas_station')
            keyword (str, optional): Additional keyword to filter results
            min_price (int, optional): Minimum price level (0-4)
            max_price (int, optional): Maximum price level (0-4)
            open_now (bool): Only return places that are open now
            
        Returns:
            List[Dict]: List of places found
        """
        
        # Build parameters
        params = {
            'location': f"{latitude},{longitude}",
            'radius': radius,
            'key': self.api_key
        }
        
        # Add optional parameters
        if place_type:
            params['type'] = place_type
        if keyword:
            params['keyword'] = keyword
        if min_price is not None:
            params['minprice'] = min_price
        if max_price is not None:
            params['maxprice'] = max_price
        if open_now:
            params['opennow'] = 'true'
        
        all_results = []
        next_page_token = None
        
        while True:
            # Add page token if we have one
            if next_page_token:
                params['pagetoken'] = next_page_token
                # Google requires a short delay before using page token
                time.sleep(2)
            
            try:
                # Make the API request
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Check if request was successful
                if data['status'] != 'OK' and data['status'] != 'ZERO_RESULTS':
                    print(f"API Error: {data['status']}")
                    if 'error_message' in data:
                        print(f"Error message: {data['error_message']}")
                    break
                
                # Add results to our list
                if 'results' in data:
                    all_results.extend(data['results'])
                    print(f"Found {len(data['results'])} places in this batch")
                
                # Check for more pages
                next_page_token = data.get('next_page_token')
                if not next_page_token:
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {e}")
                break
        
        return all_results
    
    def format_place_info(self, place: Dict) -> Dict:
        """
        Extract and format key information from a place result
        
        Args:
            place (Dict): Raw place data from API
            
        Returns:
            Dict: Formatted place information
        """
        return {
            'name': place.get('name', 'N/A'),
            'place_id': place.get('place_id', 'N/A'),
            'rating': place.get('rating', 'N/A'),
            'user_ratings_total': place.get('user_ratings_total', 0),
            'price_level': place.get('price_level', 'N/A'),
            'types': place.get('types', []),
            'vicinity': place.get('vicinity', 'N/A'),
            'geometry': {
                'lat': place.get('geometry', {}).get('location', {}).get('lat', 'N/A'),
                'lng': place.get('geometry', {}).get('location', {}).get('lng', 'N/A')
            },
            'open_now': place.get('opening_hours', {}).get('open_now', 'Unknown'),
            'photos': len(place.get('photos', [])) > 0
        }

def main():
    # Configuration
    with open("google_api_key.txt", "r") as key_file:
        API_KEY = key_file.read().strip()
    
    # Search parameters
    latitude = 47.685141048898465  
    longitude = -122.35545207468901
    radius = 807.72 
    #place_type = "restaurant"  # You can try: restaurant, store, gas_station, etc.
    keyword = None  # Optional: "pizza", "coffee", etc.
    
    # Initialize the API client
    places_api = GooglePlacesNearbySearch(API_KEY)
    
    print(f"Searching  within {radius}m of ({latitude}, {longitude})")
    print("-" * 60)
    
    # Perform the search
    results = places_api.search_nearby(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        #place_type=place_type,
        keyword=keyword,
        open_now=False  # Set to True to only find places open now
    )
    
    print(f"\nFound {len(results)} total places!")
    print("-" * 60)
    
    # Process and display results
    for i, place in enumerate(results[:10], 1):  # Show first 10 results
        formatted_place = places_api.format_place_info(place)
        
        print(f"{i}. {formatted_place['name']}")
        print(f"   Rating: {formatted_place['rating']} ({formatted_place['user_ratings_total']} reviews)")
        print(f"   Address: {formatted_place['vicinity']}")
        print(f"   Types: {', '.join(formatted_place['types'][:3])}")  # Show first 3 types
        print(f"   Coordinates: {formatted_place['geometry']['lat']}, {formatted_place['geometry']['lng']}")
        if formatted_place['open_now'] != 'Unknown':
            print(f"   Open now: {formatted_place['open_now']}")
        print()
    
    # Save results to JSON file
    with open('nearby_places.json', 'w', encoding='utf-8') as f:
        json.dump([places_api.format_place_info(place) for place in results], f, indent=2, ensure_ascii=False)
    
    print(f"All {len(results)} results saved to 'nearby_places.json'")

if __name__ == "__main__":
    main()