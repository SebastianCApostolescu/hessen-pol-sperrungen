import requests
from datetime import datetime
import pytz

def fetch_traffic_info():
    url = "https://webapi.polizei.hessen.de/api/traffic/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def format_date(date_str):
    if not date_str:
        return "Not specified"
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        german_tz = pytz.timezone('Europe/Berlin')
        dt = dt.astimezone(german_tz)
        return dt.strftime('%d.%m.%Y %H:%M')
    except ValueError:
        return date_str

def get_time_value(duration_dict, key):
    if not duration_dict:
        return ''
    time_dict = duration_dict.get(key, {})
    if isinstance(time_dict, dict):
        return time_dict.get('value', '')
    return ''

def display_traffic_info():
    data = fetch_traffic_info()
    if not data or 'data' not in data:
        print("No traffic data available")
        return

    print("\n=== Closed Roads in Hessen ===\n")
    
    found_closures = False
    for item in data['data']:
        descriptions = item.get('description', [])
        if not descriptions:
            continue

        desc = descriptions[0].get('value', '')
        
        # Check specifically for road closures (gesperrt/sperrung)
        if any(keyword in desc.lower() for keyword in ['gesperrt', 'sperrung']):
            location = item.get('location', {}).get('description', 'Location not specified')
            
            duration = item.get('duration', {})
            start_time = get_time_value(duration, 'startTime')
            end_time = get_time_value(duration, 'endTime')
            
            print(f"Location: {location}")
            print(f"Description: {desc}")
            print(f"Start: {format_date(start_time)}")
            print(f"End: {format_date(end_time)}")
            print("-" * 80 + "\n")
            found_closures = True
    
    if not found_closures:
        print("No road closures found at the moment.")

if __name__ == "__main__":
    display_traffic_info() 