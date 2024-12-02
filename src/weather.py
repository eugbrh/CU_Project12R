import requests

class Weather:
    def __init__(self, api_key, key):
        self.api_key_weather = api_key
        self.loc_key = key
    
    def get_weather_data(self):
        pass