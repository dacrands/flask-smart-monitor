from flask import render_template, jsonify
from app import app
import requests
from xml.etree import ElementTree

WEATHER_URL = "https://api.darksky.net/forecast/{0}/{1},{2}".format(app.config['WEATHER_API_KEY'], app.config['LATITUDE'], app.config['LONGITUDE'])
STOCKS_URL = "https://api.iextrading.com/1.0/stock/market/batch?symbols=f,fb,aapl,vt,siri,amd,fit&types=quote,news,chart&range=1m&last=10"

@app.route('/')
def index():
  weatherRes = requests.get(WEATHER_URL)    
  weatherJson = weatherRes.json()

  stocksRes = requests.get(STOCKS_URL)
  stocksJson = stocksRes.json()

  return render_template('index.html', weatherData=weatherJson, stocksData=stocksJson)