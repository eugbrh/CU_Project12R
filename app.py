from src.location import Location
from src.weather import Weather

city = 'Москва'
accu_api_key = ''
ya_api_key = ''
loc = Location(city, accu_api_key, ya_api_key)
key = str(loc.get_key())
wthr = Weather(key, accu_api_key)
wthr.get_weather()
print(wthr.check_bad_weather())