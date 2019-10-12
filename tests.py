import unittest
import requests
from app import app, db
from app.models import User

class UserModelCase(unittest.TestCase):
  def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

  def tearDown(self):
      db.session.remove()
      db.drop_all()

  def test_password_hashing(self):
    user = User(username='dave')
    user.set_password('dog')
    self.assertFalse(user.check_password('cat'))
    self.assertTrue(user.check_password('dog'))    

  def test_verify_token(self):
    user = User(id=0)
    token = user.get_email_token()
    valid_token = user.verify_email_token(token)    
    self.assertEqual(user.id, valid_token)

class TestAPIRequests(unittest.TestCase):
  def test_stock_request(self):
    STOCKS_URL = "https://cloud.iexapis.com/v1/stock/market/batch?types=chart&symbols=aapl,goog,fb&token={0}".format(
      app.config['STOCKS_API_KEY']
    )
    stockRes = requests.get(STOCKS_URL)
    self.assertEqual(stockRes.status_code, 200)
  
  def test_weather_request(self):
    user = User(latitude=0,longitude=2)
    WEATHER_URL = "https://api.darksky.net/forecast/{0}/{1},{2}".format(
        app.config['WEATHER_API_KEY'], user.latitude, user.longitude)
    weatherRes = requests.get(WEATHER_URL)
    self.assertEqual(weatherRes.status_code, 200)

if __name__ == '__main__':
  unittest.main(verbosity=2)