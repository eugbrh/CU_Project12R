import requests

class Location:
    def __init__(self, city, accu_api_key, ya_api_key):
        self.city = city
        self.accu = accu_api_key
        self.ya = ya_api_key
        self.lat = str()
        self.lon = str()
    
    def ya_request(self, city: str):
        params = {'apikey': self.ya,
                  'geocode': city,
                  'lang': 'ru_RU',
                  'format': 'json'}
        
        response = requests.get('https://geocode-maps.yandex.ru/1.x', params=params)

        if response.status_code != 200:
            print('Ошибка при получении данных:', response.json())
            return None

        return response.json()
    
    def get_coords(self):
        '''
        Возвращает координаты города
        '''
        data = self.ya_request(self.city)

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
    
    def get_key(self):
        '''
        Возвращает location key по координатам
        '''
        params = {'apikey': self.accu,
                  'q': f'{self.lat},{self.lon}'}
        response = requests.get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search', params = params)

        if response.status_code != 200 and response.status_code != 201:
            print('Ошибка при получении данных:', response.json())
            return
        
        return response.json()['Key']