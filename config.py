import os

class Config(object):
  WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or 'nice-try'
  LONGITUDE = os.environ.get('LONGITUDE') or -73.9976
  LATITUDE = os.environ.get('LATITUDE') or 40.9622