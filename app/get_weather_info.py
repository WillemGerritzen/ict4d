import requests

BASE_URL = "https://www.metaweather.com/api/"
LOCATION_SEARCH_URL = BASE_URL + "location/search/"
WEATHER_INFO_URL = BASE_URL + "location/{}/"


def get_location_id(query):
    """
    get location id
    """
    r = requests.get(LOCATION_SEARCH_URL, params={'query': query})
    data = r.json()
    if len(data):
        return data[0]['woeid']


def get_weather(query, days=1):
    """
	get weather data
	"""
    location_id = get_location_id(query)
    if location_id is None:
        return "Location not found."
    r = requests.get(WEATHER_INFO_URL.format(location_id))
    data = r.json()
    result = {}
    result['location'] = data['title']
    result['weather'] = []
    for day_weather in data['consolidated_weather'][:days]:
        result['weather'].append({
            'date': day_weather['applicable_date'],
            'the_temp': round(day_weather['the_temp'], 2),
            'weather_state_name': day_weather['weather_state_name'],
            'wind_spped': round(day_weather['wind_speed'], 2),
            'wind_direction': day_weather['wind_direction_compass'],
            'humidity': round(day_weather['humidity'], 2)
        })
    return result


def print_weather_details(data):
    """
    print weather details
    """
    print("Location:", data['location'], end='\n\n')
    for row in data['weather']:
        print("Date:", row['date'])
        print("Weather Type:", row['weather_state_name'])
        print("Min Temp.:", row['min_temp'])
        print("Max Temp.:", row['max_temp'])
        print()


if __name__ == '__main__':
	a = get_weather('delhi', 4)
	print(a)
