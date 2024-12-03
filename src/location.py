import requests
from src.weather import Weather

class Location:
    def __init__(self, accu_api_key, ya_api_key):
        self.accu = accu_api_key
        self.ya = ya_api_key
        self.lat = ''
        self.lon = ''
    
    def ya_request(self, city: str):
        params = {'apikey': self.ya,
                  'geocode': city,
                  'lang': 'ru_RU',
                  'kind': 'locality',
                  'format': 'json'}
        
        response = requests.get('https://geocode-maps.yandex.ru/1.x', params=params)

        if response.status_code != 200:
            print('Ошибка при получении данных:', response.json())
            return None

        return response.json()
    
    def get_coords(self, city: str):
        '''
        Возвращает координаты города
        '''
        data = self.ya_request(city)

        if data:
            try:
                coords = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                lon, lat = coords.split(' ')
                self.lat = lat
                self.lon = lon
                return str(lon), str(lat)
            except KeyError:
                print('Не удалось получить координаты')
                return None, None
        return None, None
    
    def get_key(self, city: str):
        '''
        Возвращает location key по координатам
        '''
        self.get_coords(city)
        params = {'apikey': self.accu,
                  'q': f'{self.lat},{self.lon}'}
        response = requests.get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search', params = params)

        if response.status_code != 200 and response.status_code != 201:
            print('Ошибка при получении данных:', response.json())
            return
        
        return response.json()['Key']
    
    def get_weather(self, city: str):
        '''
        Возвращает комментарий о погодных условиях и погодные условия в городе
        '''
        key = self.get_key(city)
        point = Weather(key, self.accu)
        data = point.get_weather()
        comment = point.check_bad_weather()
        return (comment, data)