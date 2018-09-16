from flask import render_template, jsonify
from app import app
import requests

WEATHER_URL = "https://api.darksky.net/forecast/{0}/{1},{2}".format(app.config['WEATHER_API_KEY'], app.config['LATITUDE'], app.config['LONGITUDE'])

@app.route('/')
def index():
  weatherRes = requests.get(WEATHER_URL)    
  weatherJson = weatherRes.json()
  
  return render_template('index.html', weatherData=weatherJson)