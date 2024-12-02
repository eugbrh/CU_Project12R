import requests

class Weather:
    def __init__(self, loc_key, accu_api_key):
        self.api_key = accu_api_key
        self.loc_key = loc_key
        self.weather = {}
        self.data = {}
    
    def get_current_weather_data(self):
        '''
        Получает погодные данные по location key
        '''
        params = {
        'apikey': self.api_key,
        'language': 'ru',
        'details': 'true'
        }
        response = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/{self.loc_key}", params=params)
        data = response.json()
        if data:
            self.weather['temperature'] = data[0]['Temperature']['Metric']['Value']
            self.weather['humidity'] = data[0]['RelativeHumidity']
            self.weather['wind_speed'] = data[0]['Wind']['Speed']['Metric']['Value']
            
            return data
        else:
            return None
        
    def get_forecast_data(self):
        params = {
        'apikey': self.api_key,
        'language': 'ru',
        'details': 'true',
        'metric': 'true'
        }
        response = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{self.loc_key}", params=params)
        data = response.json()
        if data:
            self.weather['precipitation_prob'] = data['DailyForecasts'][0]['Day']['PrecipitationProbability']
            return data
        else:
            return None
    
    def get_weather(self):
        self.get_current_weather_data()
        self.get_forecast_data()
        return self.weather
    
    def check_bad_weather(self):
        ''' 
        Функция для оценки неблагоприятных погодных условий 
        '''
        weather = self.weather
        warnings = []

        if weather['temperature'] < 0 or weather['temperature'] > 35:
            warnings.append("Неприятная температура.")
        if weather['wind_speed'] > 50:
            warnings.append("Сильный ветер.")
        if weather['precipitation_prob'] > 70:
            warnings.append("Высокая вероятность осадков.")

        if warnings:
            return "Неблагоприятные погодные условия: " + " ".join(warnings)
        else:
            return "Погодные условия благоприятные."